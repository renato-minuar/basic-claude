---
description: Run comprehensive UI design review
---

Launch the design-review agent to systematically evaluate UI changes across all quality dimensions.

**Prerequisites:**
- Development server should be running on http://localhost:3000
- Changes should be committed or clearly identified

**What it does:**
1. Analyzes changed files
2. Tests interactions with Playwright
3. Checks responsiveness across viewports
4. Verifies accessibility (WCAG 2.1 AA)
5. Assesses visual polish and consistency
6. Tests edge cases and error states
7. Reviews code quality

**Output:**
Structured markdown report with findings categorized by severity:
- 🔴 Blockers (must fix)
- 🟠 High-Priority (should fix)
- 🟡 Medium-Priority (nice to fix)
- 🔵 Nitpicks (optional)

**Usage:**
Just type `/design-review` and the agent will handle the rest.

The agent will use Playwright to interact with the live application and generate screenshots of any issues found.
