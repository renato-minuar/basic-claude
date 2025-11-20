#!/usr/bin/env python3
"""
Claude Code Stop Hook - Automatically logs interactions to journal database
"""

import json
import sqlite3
import sys
import time
import os
from datetime import datetime
from pathlib import Path

def parse_transcript(transcript_path):
    """Parse JSONL transcript and extract latest user-assistant exchange"""
    try:
        with open(transcript_path, 'r') as f:
            lines = f.readlines()

        # Parse all messages
        messages = [json.loads(line) for line in lines if line.strip()]

        # Find the last user message and subsequent assistant messages
        user_prompt = None
        assistant_content = []
        tools_used = set()

        # Iterate backwards to get the most recent exchange
        for i in range(len(messages) - 1, -1, -1):
            msg = messages[i]

            # Extract role - it can be at top level 'type' or inside 'message.role'
            role = msg.get('type')
            if not role:
                role = msg.get('message', {}).get('role')

            if role == 'assistant' and user_prompt is None:
                # Collect assistant messages (going backwards)
                message_obj = msg.get('message', msg)
                content = message_obj.get('content', [])
                for item in content:
                    if isinstance(item, dict):
                        if item.get('type') == 'text':
                            assistant_content.insert(0, item.get('text', ''))
                        elif item.get('type') == 'tool_use':
                            tools_used.add(item.get('name', 'unknown'))

            elif role == 'user':
                # Found the user prompt for this exchange
                # Check if this has the original user text (not tool results)
                message_obj = msg.get('message', msg)
                content = message_obj.get('content', [])

                # Skip if this is just tool results
                if isinstance(content, list):
                    has_text = any(
                        isinstance(item, dict) and item.get('type') == 'text'
                        for item in content
                    )
                    if not has_text:
                        continue

                if isinstance(content, str):
                    user_prompt = content
                elif isinstance(content, list):
                    # Extract text from content blocks
                    text_parts = [
                        item.get('text', '')
                        for item in content
                        if isinstance(item, dict) and item.get('type') == 'text'
                    ]
                    user_prompt = ' '.join(text_parts).strip()

                if user_prompt:
                    break

        # Generate intelligent summary from assistant content
        summary = generate_intelligent_summary(
            user_prompt or 'No prompt found',
            assistant_content,
            tools_used
        )

        return {
            'user_prompt': user_prompt or 'No prompt found',
            'summary': summary,
            'tools_used': list(tools_used)
        }

    except Exception as e:
        print(f"Error parsing transcript: {e}", file=sys.stderr)
        return None

def load_env_file():
    """Load environment variables from .env file in journal directory"""
    try:
        # Load from .claude/journal/.env (journal-specific config)
        env_file = Path(__file__).parent / '.env'

        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Remove quotes if present
                        value = value.strip().strip('"').strip("'")
                        os.environ[key.strip()] = value
    except Exception as e:
        # Silently fail - not critical
        pass

def generate_intelligent_summary(user_prompt, assistant_content, tools_used):
    """Generate an intelligent summary using Ollama (local LLM)"""
    if not assistant_content:
        return 'No response recorded'

    full_text = ' '.join(assistant_content)

    # Try to use Ollama for summarization
    try:
        import requests

        # Call Ollama API (local) to generate summary
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2:1b',
                'prompt': f'''Summarize what was accomplished in this response. Write ONLY the summary - do NOT include any preamble like "Here is a summary" or "What was accomplished". Start directly with the action.

{full_text[:4000]}

Examples (notice they start directly with the action):
- "Fixed database locking error by adding retry logic with exponential backoff."
- "Updated documentation: corrected API routes structure, added Tier 3 layout patterns, and updated project status dates."
- "Completed terms system with basic/custom options in event form, created terms display page with markdown rendering, and implemented terms cascade (event → client → platform)."

Summary:''',
                'stream': False
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            summary = data['response'].strip()
            return summary
        else:
            # Fallback on API error
            return full_text[:300] + '...' if len(full_text) > 300 else full_text

    except Exception as e:
        # Fallback on any error (Ollama not running, etc.)
        print(f"Warning: Could not generate AI summary: {e}", file=sys.stderr)
        return full_text[:300] + '...' if len(full_text) > 300 else full_text

def save_to_journal(session_id, interaction):
    """Save interaction to SQLite journal with retry logic for database locks"""
    db_path = Path(__file__).parent / 'journal.db'
    schema_path = Path(__file__).parent / 'schema.sql'

    max_retries = 5
    retry_delay = 0.1  # 100ms

    for attempt in range(max_retries):
        try:
            # Set timeout to 5 seconds for lock acquisition
            conn = sqlite3.connect(str(db_path), timeout=5.0)

            # Initialize schema
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    conn.executescript(f.read())

            # Insert journal entry
            conn.execute(
                '''INSERT INTO journal (timestamp, session_id, user_prompt, summary, tools_used)
                   VALUES (?, ?, ?, ?, ?)''',
                (
                    datetime.now().isoformat(),
                    session_id,
                    interaction['user_prompt'],
                    interaction['summary'],
                    json.dumps(interaction['tools_used'])
                )
            )

            conn.commit()
            conn.close()
            return  # Success, exit function

        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < max_retries - 1:
                # Database is locked, retry after delay
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
                continue
            else:
                # Max retries reached or different error
                print(f"Warning: Could not save to journal: {e}", file=sys.stderr)
                return  # Exit gracefully

        except Exception as e:
            print(f"Warning: Error saving to journal: {e}", file=sys.stderr)
            return  # Exit gracefully

def main():
    try:
        # Read hook input from stdin
        hook_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError) as e:
        print(f"Warning: No valid JSON input from hook: {e}", file=sys.stderr)
        sys.exit(0)  # Exit gracefully

    session_id = hook_data.get('session_id')
    transcript_path = hook_data.get('transcript_path')

    if not transcript_path:
        print("Warning: No transcript path provided in hook data", file=sys.stderr)
        sys.exit(0)  # Exit gracefully

    # Parse transcript
    interaction = parse_transcript(transcript_path)

    if interaction:
        # Check if user wants to skip journaling
        user_prompt = interaction.get('user_prompt', '')
        if '--sj' in user_prompt:
            print("⊘ Skipping journal (--sj flag detected)")
            sys.exit(0)

        # Save to database
        save_to_journal(session_id, interaction)
        print(f"✓ Journal updated: {interaction['user_prompt'][:50]}...")
    else:
        print("Warning: Failed to parse transcript", file=sys.stderr)

    # Exit 0 to allow session to continue normally
    sys.exit(0)

if __name__ == '__main__':
    main()
