# Coding Standards & Development Practices

## I. Working Principles

*   [ ] **Ask First, Code Second:** Clarify requirements before implementing. If ambiguous, ask questions. Propose solutions, don't assume.
*   [ ] **Proactive Quality:** Write tests as you build, not after. Test blocks incrementally. Catch bugs early when they're cheap to fix.
*   [ ] **Challenge Bad Ideas Respectfully:** If a requirement seems problematic, explain why and suggest alternatives with trade-offs.
*   [ ] **Document Decisions:** Why matters more than what. Use code comments for complex logic. Keep decision log in commits.
*   [ ] **Reusability by Default:** Design every piece of code for reuse from the start. Write components that accept props, not tightly coupled to specific contexts.

## II. Code Quality Fundamentals

### A. Core Principles

*   [ ] **KISS (Keep It Simple):** First implementation should be the simplest that works. Add complexity only when needed. Prefer clear code over clever code.
*   [ ] **YAGNI (You Aren't Gonna Need It):** Don't build features "just in case." Add fields/features when you have a concrete use case. Easier to add later than maintain unused code.
*   [ ] **DRY (Don't Repeat Yourself):** Apply the Rule of Three - first time write it, second time notice duplication, third time refactor to shared utility.
*   [ ] **Single Responsibility:** Each function/component does one thing well. Target 20-30 lines per function (excluding JSX structure).

### B. Naming Conventions

*   [ ] **Functions:** Verb + noun (`fetchUser`, `createEvent`, `validateEmail`)
*   [ ] **Booleans:** `is`, `has`, `should` prefix (`isLoading`, `hasChanges`, `shouldRedirect`)
*   [ ] **Constants:** `UPPER_SNAKE_CASE` for true constants
*   [ ] **Components:** `PascalCase` (`UserMenu`, `EventForm`)
*   [ ] **Variables:** Descriptive names that reveal intent. Avoid abbreviations and single letters (except loop counters).

### C. Function Design

*   [ ] **Small & Focused:** Keep functions under 30 lines. Extract helpers for complex logic.
*   [ ] **Clear Parameters:** Use descriptive parameter names. Prefer objects for 3+ parameters.
*   [ ] **Predictable Returns:** Consistent return types. Document edge cases.
*   [ ] **No Side Effects:** Pure functions where possible. Isolate side effects (API calls, state mutations).

## III. TypeScript Standards

*   [ ] **Strict Mode:** Enable strict TypeScript. Fix all type errors, don't suppress with `any`.
*   [ ] **Explicit Types:** Define interfaces for data structures. Use union types for states.
*   [ ] **Type Inference:** Let TypeScript infer when obvious. Explicit when it adds clarity.
*   [ ] **Avoid `any`:** Use `unknown` if type is truly unknown. Create proper types for API responses.
*   [ ] **Discriminated Unions:** Use for state management (`{ status: "loading" } | { status: "success", data: T } | { status: "error", error: string }`)

## IV. Git Standards

### A. Commit Messages

*   [ ] **Format:** `<type>: <subject>` with optional body explaining WHY
*   [ ] **Types:** `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `style`, `chore`
*   [ ] **Subject:** Clear, concise (< 72 chars), imperative mood ("Add feature" not "Added feature")
*   [ ] **Body:** Explains reasoning, not implementation (code shows what)
*   [ ] **References:** Include issue/ticket numbers when applicable

### B. Branch Strategy

*   [ ] **Naming:** `feature/description`, `fix/description`, `refactor/description`
*   [ ] **From Main:** Always branch from latest `main`
*   [ ] **Small Commits:** Atomic, complete, reversible
*   [ ] **Frequent Commits:** After logical unit of work, before switching tasks, before experiments

### C. When to Commit

*   [ ] After completing a logical unit of work
*   [ ] Before switching to a different task
*   [ ] Before trying experimental changes
*   [ ] At end of work session
*   [ ] When tests pass (never commit broken code)

## V. Testing Standards

### A. Test Philosophy

*   [ ] **Test Behavior:** Test what users see, not implementation details.
*   [ ] **Arrange-Act-Assert:** Clear structure in every test.
*   [ ] **Descriptive Names:** Test names describe the scenario and expected outcome.
*   [ ] **Independence:** Tests don't depend on each other or external state.

### B. Test Pyramid

*   [ ] **Unit Tests (Many):** Fast, cheap, test individual functions/components
*   [ ] **Integration Tests (Some):** Test API routes, database operations
*   [ ] **E2E Tests (Few):** Critical user flows, expensive but high confidence

### C. What to Test

*   [ ] Happy path (expected usage)
*   [ ] Edge cases (empty states, boundaries)
*   [ ] Error states (invalid input, network failures)
*   [ ] Loading states
*   [ ] Accessibility (keyboard nav, ARIA)

## VI. Performance Standards

### A. Code Performance

*   [ ] **Memoization:** Use `useMemo` for expensive calculations, `useCallback` for callbacks passed as props
*   [ ] **Code Splitting:** Lazy load non-critical components with `dynamic()`
*   [ ] **Bundle Size:** Monitor and minimize. Remove unused dependencies.

### B. Data Performance

*   [ ] **Pagination:** Paginate large lists (20-50 items per page)
*   [ ] **Select Fields:** Only fetch needed fields from database
*   [ ] **Caching:** Cache expensive queries. Use SWR/React Query for server state.

### C. UI Performance

*   [ ] **Image Optimization:** Use Next.js Image component. Appropriate sizes and formats.
*   [ ] **Loading States:** Skeleton screens for page loads, spinners for actions
*   [ ] **Optimistic Updates:** Update UI immediately, rollback on error

## VII. Security Standards

*   [ ] **Input Validation:** Validate all user input on server. Never trust client.
*   [ ] **Authentication:** Check auth on every protected route. Verify permissions.
*   [ ] **Secrets:** Never commit secrets. Use environment variables. Add to .gitignore.
*   [ ] **SQL Injection:** Use parameterized queries (Prisma handles this).
*   [ ] **XSS Prevention:** Sanitize user content. Use React's built-in escaping.

## VIII. Code Review Checklist

### Before Submitting PR:

**Functionality:**
*   [ ] Feature works as expected
*   [ ] Edge cases handled (empty states, errors, loading)
*   [ ] No console errors or warnings

**Code Quality:**
*   [ ] Follows DRY, KISS, YAGNI
*   [ ] Functions are small and focused
*   [ ] Variables have meaningful names
*   [ ] No commented-out code (delete it)

**Testing:**
*   [ ] Unit tests for new components
*   [ ] Integration tests for new API routes
*   [ ] Manual testing done (including mobile)

**Performance:**
*   [ ] No unnecessary re-renders
*   [ ] Images optimized
*   [ ] Database queries efficient

**Security:**
*   [ ] Input validated on server
*   [ ] Auth checked on protected routes
*   [ ] No secrets in code

**Git:**
*   [ ] Commit messages follow standards
*   [ ] No sensitive data committed
*   [ ] Branch is up to date with main

## IX. Remember

**Good Code is:**
*   ✅ Simple (easy to understand)
*   ✅ Tested (confidence to change)
*   ✅ Consistent (follows patterns)
*   ✅ Performant (fast for users)
*   ✅ Maintainable (future you will thank you)

**When in doubt:**
1. Ask before implementing
2. Keep it simple
3. Write the test first
4. Look at existing code for patterns
5. Document why, not what
