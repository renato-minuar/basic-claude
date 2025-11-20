# CLAUDE.md

Quick reference for development. For detailed patterns, see `.claude/context/*.md` files.

---

## Quick Start (example)

**Essential Commands:**
```bash
npm run dev              # Dev server (localhost:3000)
npm test                 # Run tests
npm run build            # Production build
```

<!-- TODO: Add project-specific commands -->
<!-- Example for Prisma projects:
npx prisma studio        # Database GUI
npm run db:seed          # Reset DB with demo data
npx prisma generate      # After schema changes
npx prisma db push       # Apply schema changes
-->

**Demo Credentials:**
<!-- TODO: Add your test credentials -->
```
Admin: admin@example.com / admin123
User:  user@example.com / user123
```

---

## Project Overview

→ **For full context (business model, team, roadmap), see `.claude/project.md`**

### What This Is

<!-- TODO: Brief description of your project -->
[Brief description - what it does, who it's for]

**Tech Stack:**
<!-- TODO: Update with your stack -->
- Next.js 14 + TypeScript
- SQLite (dev) → PostgreSQL (prod)
- Prisma ORM
- NextAuth.js
- shadcn/ui + Tailwind CSS

---

## Critical Patterns

⚠️ **Architectural patterns that cause bugs if violated.**

→ **See `.claude/context/coding-standards.md` for:**
- Code quality principles (KISS, DRY, YAGNI)
- Git standards and commit format
- Testing strategy
- Performance and security standards

→ **See `.claude/context/design-principles.md` for:**
- S-Tier SaaS design checklist (Stripe/Airbnb/Linear inspired)
- Color, typography, spacing systems
- Component states and interactions
- Accessibility requirements

<!-- TODO: Add project-specific critical patterns -->
<!-- Example:
- **Layout Patterns** - Admin uses shared layout, Dashboard does not
- **Authentication** - Two separate auth providers
- **Database** - Model X has no direct relation to Y
-->

---

## Session Workflow

**Start session:**
```bash
/start
```
Loads project context, recent journal entries, and checks dev server.

**End session:**
```bash
/end
```
Generates session summary and appends to `.claude/journal/journal.md`.

**Toggle journal:**
```bash
/journal
```
Enable or disable journal system (files are preserved).

**Skip single interaction:** Add `--sj` to any prompt.

→ **For journal setup, see `.claude/journal/README.md`**

---

## Documentation Map

**Quick reference:** `CLAUDE.md` (this file)

### Project Context

| File | What | When to Use |
|------|------|-------------|
| `.claude/project.md` | Business model, team, tech stack, status | Onboarding, understanding strategic decisions |
| `.claude/ROADMAP.md` | Development phases, progress, next steps | Planning features, checking priorities |

### Technical Patterns

| File | What | When to Use |
|------|------|-------------|
| `.claude/context/coding-standards.md` | Code quality, git, testing, performance | Writing code, reviewing PRs, architectural decisions |
| `.claude/context/design-principles.md` | Visual design standards, UI checklist | Designing UI, improving polish, design review |

### Workflow

| File | What | When to Use |
|------|------|-------------|
| `.claude/journal/README.md` | Journal system setup and usage | Setting up session tracking, troubleshooting |
| `.claude/commands/start.md` | Session start command | Understanding what /start does |
| `.claude/commands/end.md` | Session end command | Understanding what /end does |

---

## Directory Structure

```
.claude/
├── project.md              # Project context
├── ROADMAP.md              # Development roadmap
├── settings.local.json     # Permissions, hooks
├── commands/
│   ├── first-time.md
│   ├── start.md
│   ├── end.md
│   └── journal.md
├── context/
│   ├── coding-standards.md
│   └── design-principles.md
└── journal/
    ├── README.md
    ├── stop-hook.py
    ├── get-session-entries.py
    ├── schema.sql
    └── journal.md
```

---

## First-Time Setup

When copying this boilerplate to a new project, run:

```bash
/first-time
```

This interactive wizard will:
- Configure journal system (hooks, paths)
- Fill in project info
- Make scripts executable
- Verify everything works

**Manual setup** (if you prefer):
- [ ] Copy settings: `cp .claude/settings.local.json.example .claude/settings.local.json`
- [ ] Update hook path in `.claude/settings.local.json`
- [ ] Make scripts executable: `chmod +x .claude/journal/*.py`
- [ ] Fill in TODOs in this file
- [ ] Fill in `.claude/project.md`
- [ ] Fill in `.claude/ROADMAP.md`

→ **For detailed setup, see `.claude/journal/README.md`**
