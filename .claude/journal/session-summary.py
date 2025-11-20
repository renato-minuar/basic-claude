#!/usr/bin/env python3
"""
Generate session summary from journal database
Queries all entries for current session and creates a concise summary
"""

import sqlite3
import sys
import json
from datetime import datetime
from pathlib import Path

def get_most_recent_session_id():
    """Get the most recent session_id from database"""
    db_path = Path(__file__).parent / 'journal.db'

    if not db_path.exists():
        return None

    conn = sqlite3.connect(str(db_path))
    cursor = conn.execute(
        "SELECT session_id FROM journal ORDER BY timestamp DESC LIMIT 1"
    )
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None

def get_session_entries(session_id):
    """Get all journal entries for a specific session"""
    db_path = Path(__file__).parent / 'journal.db'

    if not db_path.exists():
        return []

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    cursor = conn.execute(
        "SELECT * FROM journal WHERE session_id = ? ORDER BY timestamp ASC",
        (session_id,)
    )
    entries = cursor.fetchall()
    conn.close()

    return [dict(entry) for entry in entries]

def generate_summary(entries):
    """Generate a concise summary from session entries"""
    if not entries:
        return "No activity recorded in this session."

    # Extract key information
    topics = []
    tools = set()

    for entry in entries:
        # Add brief description from summary (first sentence or 100 chars)
        summary = entry['summary']
        if summary and summary != 'No response recorded':
            # Take first sentence or first 100 chars
            first_sentence = summary.split('.')[0][:100]
            if first_sentence and first_sentence not in topics:
                topics.append(first_sentence)

        # Collect tools used
        if entry['tools_used']:
            try:
                entry_tools = json.loads(entry['tools_used'])
                tools.update(entry_tools)
            except:
                pass

    # Create summary
    summary_parts = []

    if topics:
        # Combine topics into narrative
        summary_parts.append('. '.join(topics[:5]))  # Max 5 topics

    # Add tools context if significant
    if len(tools) > 3:
        summary_parts.append(f"Used {len(tools)} different tools")

    return '. '.join(summary_parts) + '.'

def append_to_journal_md(session_date, summary):
    """Append session summary to journal.md"""
    journal_path = Path(__file__).parent / 'journal.md'

    # Create journal.md if it doesn't exist
    if not journal_path.exists():
        with open(journal_path, 'w') as f:
            f.write("# Development Journal\n\n")
            f.write("*Session summaries generated automatically*\n\n")
            f.write("---\n\n")

    # Append session summary
    with open(journal_path, 'a') as f:
        f.write(f"## {session_date}\n\n")
        f.write(f"{summary}\n\n")

def main():
    # Get session_id from stdin (passed by /end command)
    try:
        hook_data = json.load(sys.stdin)
        session_id = hook_data.get('session_id')
    except (json.JSONDecodeError, EOFError):
        # If no stdin or invalid JSON, use most recent session
        session_id = None

    # If session_id is "current" or not provided, get most recent
    if not session_id or session_id == "current":
        session_id = get_most_recent_session_id()
        if not session_id:
            print("Error: No sessions found in database", file=sys.stderr)
            sys.exit(1)

    # Get all entries for this session
    entries = get_session_entries(session_id)

    if not entries:
        print("No entries found for this session.")
        sys.exit(0)

    # Generate summary
    session_date = datetime.now().strftime('%Y-%m-%d')
    summary = generate_summary(entries)

    # Append to journal.md
    append_to_journal_md(session_date, summary)

    # Output summary to user
    print(f"\n📝 Session Summary ({len(entries)} interactions):\n")
    print(summary)
    print(f"\nSaved to journal.md")

    sys.exit(0)

if __name__ == '__main__':
    main()
