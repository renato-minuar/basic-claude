# Claude Code Journal System

Automated development journal for tracking work across Claude Code sessions.

## Features

- **Automatic logging**: Stop hook captures every interaction to SQLite database
- **AI summaries**: Uses Ollama (local LLM) to generate intelligent summaries - zero cost, offline-capable
- **Session summaries**: `/end` command creates human-readable session summaries with creative titles
- **Organized by category**: Work automatically split into Workflow/Front/Backend for easy scanning
- **Team collaboration**: Journal tracked in git so all developers see progress
- **Duplicate prevention**: Multiple `/end` calls same day update existing entry instead of duplicating
- **Skip flag**: Add `--sj` to any prompt to skip journaling that interaction
- **Persistent memory**: Load context with `/start` command at session beginning

## Setup

### 1. Install Ollama (for AI summaries)

```bash
# Install Ollama (https://ollama.ai)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the model used for summaries
ollama pull llama3.2:1b

# Start Ollama (runs in background)
ollama serve
```

**Without Ollama:** Summaries are first 300 chars of response (fallback mode)
**With Ollama:** Concise, intelligent AI-generated summaries at zero cost

### 2. Configure the Stop Hook

**IMPORTANT:** You must update the hook path to your project's absolute path.

**Option 1: Using /hooks command (Recommended)**

1. Run `/hooks` in Claude Code
2. Select **Stop** event
3. Choose "Add new hook"
4. Type: **command**
5. Command: `/absolute/path/to/your/project/.claude/journal/stop-hook.py`
6. Save to **Project settings** or **User settings**

**Option 2: Manual Configuration**

Edit `.claude/settings.local.json` and replace `REPLACE_WITH_ABSOLUTE_PATH`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/your/project/.claude/journal/stop-hook.py"
          }
        ]
      }
    ]
  }
}
```

### 3. Make Script Executable

```bash
chmod +x .claude/journal/stop-hook.py
chmod +x .claude/journal/get-session-entries.py
```

### Verify Setup

After configuring:
1. Have a conversation with Claude
2. Check if `.claude/journal/journal.db` was created
3. Run: `sqlite3 .claude/journal/journal.db "SELECT COUNT(*) FROM journal;"`
4. Should see a count > 0

## Usage

### Daily Workflow

```bash
# At session start
/start              # Load journal context

# During session
# Work normally - interactions are logged automatically
# Add --sj to skip logging: "do something --sj"

# At session end
/end                # Generate session summary
```

### Commands

- **`/start`** - Loads recent session summaries and project context
- **`/end`** - Queries database for current session, generates summary, appends to `journal.md`
- **`--sj` flag** - Add to any prompt to skip journaling (e.g., "quick test --sj")

### Viewing Journal

```bash
# View recent summaries
cat .claude/journal/journal.md

# Query database directly
python3 .claude/journal/get-session-entries.py
```

## Files

```
.claude/journal/
├── stop-hook.py              # Automatic logging hook
├── get-session-entries.py    # Query utility
├── schema.sql                # Database schema
├── .env                      # Ollama config (gitignored)
├── .env.example              # Template
├── journal.db                # SQLite database (gitignored)
├── journal.md                # Session summaries (tracked in git for team)
└── README.md                 # This file
```

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS journal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    session_id TEXT NOT NULL,
    user_prompt TEXT NOT NULL,
    summary TEXT NOT NULL,
    tools_used TEXT
);
```

## Troubleshooting

**Hook not running?**
- Verify absolute path in settings (use `/hooks` command)
- Check file is executable: `ls -la .claude/journal/stop-hook.py`
- Restart Claude Code after changing settings

**No AI summaries?**
- Check if Ollama is running: `ollama list`
- Start Ollama if needed: `ollama serve`
- Verify model is installed: `ollama list` (should show llama3.2:1b)
- Journal works without Ollama (uses truncated text fallback)

**Database locked errors?**
- Hook retries with exponential backoff (5 attempts, 5s timeout)
- Only one Claude Code session should access journal.db at a time

## Privacy & Team Collaboration

**Local data (gitignored):**
- `journal.db` - Full interaction history with all prompts/responses
- `.env` - Ollama configuration

**Shared with team (tracked in git):**
- `journal.md` - Session summaries (safe to share, no sensitive data)
  - Contains what was done, why, and key decisions
  - Creative titles and organized categories (Workflow/Front/Backend)
  - Helps team stay in sync on progress

The journal scripts and summaries are committed to git for team collaboration, but the raw database with full conversation history stays local and private.
