---
description: Enable or disable the journal system
---

# Journal Toggle

Allow the user to enable or disable the journal system. Files are preserved - only the hook is toggled.

## Instructions

1. **Check current status** by reading `.claude/settings.local.json`:
   - Look for the Stop hook with `stop-hook.py`
   - If present → journal is ENABLED
   - If absent → journal is DISABLED

2. **Show current status** and ask what they want to do:

   Use AskUserQuestion with:
   - Question: "Journal is currently [ENABLED/DISABLED]. What would you like to do?"
   - Options:
     - Enable journal (if currently disabled)
     - Disable journal (if currently enabled)
     - Keep current setting

3. **If enabling:**

   a. Get project path (current working directory)

   b. Update `.claude/settings.local.json` to add the Stop hook:
   ```json
   {
     "hooks": {
       "Stop": [
         {
           "matcher": "",
           "hooks": [
             {
               "type": "command",
               "command": "[PROJECT_PATH]/.claude/journal/stop-hook.py"
             }
           ]
         }
       ]
     }
   }
   ```

   c. Ensure scripts are executable:
   ```bash
   chmod +x .claude/journal/stop-hook.py
   chmod +x .claude/journal/get-session-entries.py
   ```

   d. Confirm with restart warning:
   ```
   ✅ Journal enabled!

   ⚠️  IMPORTANT: Restart Claude Code for this to take effect!
   Press Ctrl+C to exit, then run `claude` again.

   Interactions will be logged to `.claude/journal/journal.db`
   ```

4. **If disabling:**

   a. Update `.claude/settings.local.json` to remove the Stop hook (set hooks to empty or remove the Stop key)

   b. Confirm with restart warning:
   ```
   ✅ Journal disabled!

   ⚠️  Restart Claude Code for this to take effect.

   Your journal files are preserved - you can re-enable anytime with `/journal`
   ```

5. **Remind about Ollama** (if enabling):
   - "Note: For AI-generated summaries, make sure Ollama is running with `ollama serve`"
   - "Without Ollama, summaries will be truncated text (still works, just less intelligent)"

## Notes

- Never delete journal files (journal.db, journal.md, scripts)
- Only modify the hooks section in settings.local.json
- Preserve other settings (permissions, enabledMcpjsonServers, etc.)
