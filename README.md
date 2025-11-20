# Claude Code Boilerplate

A starter template for Claude Code projects with session tracking, documentation structure, and development workflows.

**Version:** 0.1.1 (Work in Progress)

---

## What This Is

A ready-to-use folder structure for Claude Code projects that includes:

- **Session Journal** - Automatic logging of your work with AI-generated summaries
- **Documentation Structure** - Organized context files for consistent Claude interactions
- **Slash Commands** - `/start`, `/end`, `/first-time`, `/journal` for common workflows
- **Quality Standards** - Coding standards and design principles checklists

## Quick Start

### 1. Copy the boilerplate

```bash
# Clone or download this repo
git clone https://github.com/renato-minuar/basic-claude.git my-project
cd my-project

# Remove git history to start fresh
rm -rf .git
git init
```

### 2. Run the setup wizard

Open Claude Code in your project folder and run:

```bash
/first-time
```

This interactive wizard will:
- Configure the journal system
- Set up your project info
- Make scripts executable
- Guide you through remaining setup

### 3. Restart Claude Code

After setup, restart Claude Code for the journal hook to take effect:
- Press `Ctrl+C` to exit
- Run `claude` again

### 4. Start working

```bash
/start    # Begin a session (loads context)
# ... do your work ...
/end      # End session (generates summary)
```

## Features

### Session Journal

Automatically tracks your Claude Code interactions and generates AI summaries using Ollama (local LLM).

- **Zero cost** - Uses local Ollama, no API keys needed
- **Session summaries** - Human-readable summaries in `journal.md`
- **Skip flag** - Add `--sj` to any prompt to skip logging

**Requirements:** [Ollama](https://ollama.ai) with `llama3.2:1b` model (optional - works without it, just less intelligent summaries)

### Documentation Structure

```
CLAUDE.md                    # Quick reference (entry point)
.claude/
├── project.md               # Business context, team, stack
├── ROADMAP.md               # Development phases and progress
├── commands/                # Slash commands
│   ├── first-time.md        # Setup wizard
│   ├── start.md             # Session start
│   ├── end.md               # Session end
│   └── journal.md           # Toggle journal
└── context/                 # Pattern documentation
    ├── coding-standards.md  # Code quality checklist
    └── design-principles.md # UI/UX checklist
```

### Slash Commands

| Command | Description |
|---------|-------------|
| `/first-time` | Interactive setup wizard for new projects |
| `/start` | Load project context and recent work |
| `/end` | Generate session summary to journal |
| `/journal` | Enable or disable journal system |

### Agents

Custom agents for specialized tasks. Invoke with `@agent-name` or ask Claude to use them.

| Agent | Description |
|-------|-------------|
| `debugger` | Systematic debugging through evidence gathering and hypothesis testing |
| `designer` | Bold UI/UX designer who creates premium interfaces (Stripe/Linear quality) |
| `design-review` | Comprehensive UI review with prioritized findings |

**Example usage:**
```
@designer Review this component and suggest improvements
@debugger Help me find why this API call is failing
```

Agents are defined in `.claude/agents/` - you can customize them or create your own.

## Manual Setup

If you prefer not to use the wizard:

1. Copy the settings template:
   ```bash
   cp .claude/settings.local.json.example .claude/settings.local.json
   ```

2. Update hook path in `.claude/settings.local.json`:
   - Replace `REPLACE_WITH_ABSOLUTE_PATH` with your project's absolute path

3. Make scripts executable:
   ```bash
   chmod +x .claude/journal/*.py
   ```

4. (Optional) Install Ollama for AI summaries:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama pull llama3.2:1b
   ```

4. Restart Claude Code

5. Fill in TODOs in:
   - `CLAUDE.md`
   - `.claude/project.md`
   - `.claude/ROADMAP.md`

## Customization

### Adding Context Files

Create new files in `.claude/context/` for project-specific patterns:
- `api-patterns.md` - API conventions
- `architecture-patterns.md` - System architecture
- `component-patterns.md` - UI component patterns

### Adding Commands

Create new `.md` files in `.claude/commands/`:

```markdown
---
description: Brief description of command
---

Instructions for Claude to follow when this command is run.
```

## Requirements

- **Claude Code** - Anthropic's CLI for Claude
- **Python 3** - For journal scripts
- **Ollama** (optional) - For AI-generated summaries

## Contributing

This is a work in progress. Issues and PRs welcome!

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Note:** This boilerplate is designed for Claude Code workflows. It won't do anything useful without Claude Code installed.

---

<sub>Created by [@renato-minuar](https://github.com/renato-minuar)</sub>
