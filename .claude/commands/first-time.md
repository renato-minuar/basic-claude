---
description: Interactive setup wizard for new projects
---

# First-Time Setup Wizard

Guide the user through initial project setup. This command should be run once when copying this boilerplate to a new project.

## Instructions

You are a setup wizard. Guide the user through each step, ask questions using the AskUserQuestion tool, and update files automatically.

### Step 1: Detect Project Path

1. Get the current working directory
2. Confirm with user: "I detected your project path as: `/path/to/project`. Is this correct?"
3. Store this as `PROJECT_PATH`

### Step 2: Choose Features

Ask the user which features they want to enable:

**Question: Journal System**
- "Do you want to enable the session journal? This tracks your work and generates AI summaries."
- Options: Yes (recommended), No

### Step 3: Configure Journal (if enabled)

If user chose journal:

1. Update `.claude/settings.local.json`:
   - Replace `REPLACE_WITH_ABSOLUTE_PATH` with `PROJECT_PATH`

2. Make scripts executable:
   ```bash
   chmod +x .claude/journal/stop-hook.py
   chmod +x .claude/journal/get-session-entries.py
   ```

3. Ask about Ollama:
   - "Do you have Ollama installed for AI summaries? (If not, journal will use truncated text)"
   - Options: Yes, No, Install it for me

   If "Install it for me":
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama pull llama3.2:1b
   ```

### Step 4: Project Info

Ask for basic project info to fill in templates:

1. "What's the project name?"
2. "Brief description (one sentence):"
3. "Tech stack? (e.g., Next.js, Python/Django, etc.)"

Update `CLAUDE.md` and `.claude/project.md` with this info.

### Step 5: Verify Setup

Run verification:

1. Check if settings.local.json has correct path (if journal enabled)
2. Check if scripts are executable (if journal enabled)
3. List any remaining TODOs

### Step 6: Summary

Print a summary:

If journal was enabled:
```
✅ Setup Complete!

Enabled features:
- [x] Journal system (hook configured at PROJECT_PATH/.claude/journal/stop-hook.py)

⚠️  IMPORTANT: Restart Claude Code for journal to work!
The hook settings won't take effect until you restart.
Press Ctrl+C to exit, then run `claude` again.

Next steps:
1. Restart Claude Code (required for journal)
2. Fill in remaining TODOs in CLAUDE.md
3. Start your first session with /start

Your project is ready to go!
```

If journal was disabled:
```
✅ Setup Complete!

Journal system is disabled. You can enable it anytime with /journal

Next steps:
1. Fill in remaining TODOs in CLAUDE.md
2. Start working on your project

Your project is ready to go!
```

## Important Notes

- Use AskUserQuestion tool for all user input
- Edit files directly with the Edit tool
- Be friendly and explain what each step does
- If something fails, explain how to fix it manually
- Don't skip steps even if user seems experienced
