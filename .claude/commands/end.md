---
description: End session and generate journal summary
---

Generate session summary from all interactions in this session and append to .claude/journal/journal.md.

**How it works:**
- The stop hook has been logging every interaction to .claude/journal/journal.db
- Now you will read all entries, analyze them, and write a comprehensive summary

**Instructions:**

**Phase 1: Gather session data**
1. Run: `python3 .claude/journal/get-session-entries.py` to retrieve all entries for today's sessions
   - Uses smart session detection: finds all sessions with `/start` commands (works for in-progress sessions)
   - 5am cutoff: sessions starting before 5am belong to previous day
   - Handles multiple sessions per day (e.g., 11:00-16:00, then 22:00-01:00)
   - Handles late-night sessions (e.g., 22:00 → 01:00 belongs to day it started)
   - Shows session boundaries when switching between sessions
   - **Outputs git log command** with exact time range from sessions
2. Gather recent git commits for additional context:
   - **Use the git log command provided by the script above** (uses MIN/MAX timestamps from ALL of today's sessions)
   - This captures ONLY commits made during actual working time (no arbitrary windows)
   - If no sessions found, fallback to: `git log --since="24 hours ago" --until="now" --pretty=format:"%h - %s%n%b" --stat`
   - Shows: commit hashes, messages, descriptions, and files changed
   - Use this to understand WHAT was actually committed (complements session log about what was discussed)
3. Read through all the entries and commits to understand what was accomplished
4. **Check if documentation needs updating:**
   - Review today's work and determine if any of these need updates:
     - **ROADMAP.md** - If completed milestones, infrastructure changes, or roadmap shifts
     - **CLAUDE.md** - If new critical patterns, architectural changes, or developer workflows
     - **.claude/context/*.md** - If new patterns worth documenting (API, components, architecture, etc.)
   - If documentation needs updating:
     - Update the relevant files with today's changes
     - Commit changes: `git add -A && git commit -m "Update documentation: [brief description]"`
     - Push changes: `git push origin main`
   - If no documentation updates needed, proceed to next phase

**Phase 2: Switch to main branch (automatic conflict prevention)**
3. Save current branch: Run `git rev-parse --abbrev-ref HEAD` to get current branch name
4. Check for uncommitted changes: Run `git status --porcelain`
5. If NOT on main branch:
   - If there are uncommitted changes: Run `git stash push -m "Auto-stash for journal update"`
   - Switch to main: Run `git checkout main`
6. Fetch latest and update journal.md atomically (prevents race condition):
   - Run: `git fetch origin && git checkout origin/main -- .claude/journal/journal.md`
   - This ensures you get the absolute latest journal.md, even if brother pushed seconds ago
   - Only journal.md is updated, all other files untouched

**Phase 3: Update journal**
7. Read .claude/journal/journal.md to check if today's date already has an entry
8. If today's date exists: UPDATE that entry by merging new work with existing content (combine Workflow/Front/Backend items)
9. If today's date doesn't exist: ADD NEW entry at the top (after the --- separator)
10. Write summary following this template (be CONCISE, text-first, avoid long bullet lists)
11. **IMPORTANT - Title comes LAST**: First write the full summary (What & Why, Changes, Important Decisions). Read what you wrote to understand what actually happened.
12. **After writing and reading summary**: Create a CREATIVE, ACCURATE title:
    - Title must reflect actual work done (read the content first!)
    - NOT technical/boring (❌ "Documentation Overhaul & Infrastructure Setup")
    - NOT false claims (❌ "Zero to Complete" when work is ongoing)
    - Creative, captures the essence, can lean on humor (✓ "The Great Documentation Spring Cleaning")
    - Short and punchy (3-8 words ideal)
    - Examples: "When Documentation Met Reality", "The Day We Stopped Repeating Ourselves", "Breaking Things to Fix Them"
13. Update the `##` heading with: `## YYYY-MM-DD - [Your Creative Title]`

**Phase 4: Commit and push journal**
13. Run: `git add .claude/journal/journal.md`
14. Run: `git commit -m "Update journal: [Brief description of today's work]"`
15. Try to push: Run `git push origin main`
16. If push fails (local main behind origin/main in other files):
    - Try rebase with error handling:
      ```bash
      if ! git pull origin main --rebase; then
        echo "⚠️  Rebase failed. Attempting merge instead..."
        git rebase --abort
        if ! git pull origin main --no-rebase; then
          echo "❌ Both rebase and merge failed. Manual intervention needed:"
          echo "  1. Check conflicts: git status"
          echo "  2. Resolve conflicts in journal.md"
          echo "  3. Run: git add .claude/journal/journal.md"
          echo "  4. Run: git rebase --continue (or git merge --continue)"
          echo "  5. Run: git push origin main"
          exit 1
        fi
      fi
      git push origin main
      ```

**Phase 5: Return to original branch**
17. If you switched branches in Phase 2:
    - Run: `git checkout [original-branch-name]`
    - If you stashed changes: Try to restore them with error handling:
      ```bash
      if ! git stash pop; then
        echo "⚠️  Warning: Stash pop failed (likely conflicts with recent changes)"
        echo "Your work is safe in the stash. To resolve:"
        echo "  1. Run: git status (to see conflicts)"
        echo "  2. Resolve conflicts manually"
        echo "  3. Run: git add <resolved-files>"
        echo "  4. Run: git stash drop (to clean up)"
        exit 1
      fi
      ```
18. Confirm: "✅ Journal updated on main and pushed. You're back on [branch-name]."

```markdown
## YYYY-MM-DD - [Creative, Memorable Title]

### What & Why
[1-2 sentences: what was done and business/user motivation]

Example title styles:
- Playful: "The Great Documentation Spring Cleaning"
- Reference: "When Documentation Met Reality"
- Achievement: "The Day We Stopped Repeating Ourselves"
- Dramatic: "Breaking Things to Fix Them"

### Major Changes

**Workflow:**
- [Documentation/tooling/strategy/infrastructure changes]

**Front:**
- [UI/UX/components/styling work]

**Backend:**
- [API/database/server logic/data models]

[Split work into these 3 categories when possible. If only 1-2 categories have work, that's fine - just include the relevant ones. Keep each category to 2-4 bullets max.]

### Important Decisions
- [Decision made]: [Rationale - why this choice over alternatives]
- [Pattern established]: [Why this approach]
[Only include decisions with lasting impact]

### Gotchas
[Optional section - only if there are tricky implementation details or known issues]
- [Thing to watch out for]

### Context from Previous Session
[Optional - if this continues work from another session]
```

**IMPORTANT GUIDELINES:**
- **Be CONCISE**: Text-first, avoid long lists of files/features. Group related items.
- **Use git commits**: Commit messages show WHAT was done, session log shows WHY. Combine both for complete picture.
- **Write for HUMANS**: Journal is for the dev team, not for AI. Skip implementation details that only matter to you (import syntax, package names, etc.)
- **NO code snippets**: Code is in the files
- **NO exhaustive file lists**: Just mention the key areas changed (e.g., "7 focused context files" not listing all 7 names)
- **Focus on WHY**: Decisions and rationale, not HOW they were implemented
- **Skip "Gotchas" for technical details**: Only include gotchas that affect user experience or business logic, not AI implementation details
- **Precise language**: Not everything is "major" - use "changes" for routine work, "major" for significant milestones
- **Avoid repetition**: Don't repeat the same point across sections (e.g., if you mention ThumbmarkJS swap in What & Why, don't repeat it in Changes AND Important Decisions - pick the most relevant section)
- **Check for duplicates**: If today's date exists, merge/update instead of creating duplicate entry
- Remember: /start loads CLAUDE.md, project.md, and all code files
- **Commit context**: If commits show iteration (e.g., multiple fixes to same file), mention learnings not individual commits
- **Commits != work intensity**: 50 commits doesn't mean more work than 5 commits. Focus on impact and complexity, not commit count

After completing all phases, confirm to the user:
1. ✅ Journal entry created/updated in .claude/journal/journal.md
2. ✅ Committed and pushed to main branch automatically
3. ✅ Returned to original branch (if you were on a feature branch)
4. No manual git operations needed - everything was handled automatically!
