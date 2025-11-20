# Architecture Patterns

High-level architecture documentation for the project.

<!-- TODO: Document your project's architecture patterns -->

---

## Application Structure

<!-- TODO: Describe your app's structure -->
<!-- Example:
### Route Structure
- `/admin/*` - Admin panel (internal tools)
- `/dashboard/*` - User dashboard
- `/api/*` - API routes
-->

---

## Layout Patterns

<!-- TODO: Document your layout patterns -->
<!-- Example:
### Shared Layout
Admin pages use a shared layout that provides the header.
Pages should NOT include their own header.

### Per-Page Layout
Dashboard pages manage their own branded header.
Each page must include AppHeader component.
-->

---

## Authentication System

<!-- TODO: Document your auth patterns -->
<!-- Example:
### Admin/User Auth (NextAuth)
- Session-based authentication
- Role checking in middleware or pages
- Credentials provider for email/password

### API Auth (JWT)
- JWT tokens for API-only clients
- Store in httpOnly cookies
- Separate from NextAuth sessions
-->

---

## Database Patterns

<!-- TODO: Document database patterns -->
<!-- Example:
### Prisma Usage
- Use `select` to limit fields returned
- Use `include` for relations
- Paginate large lists

### Common Queries
```typescript
// Get with relations
const user = await prisma.user.findUnique({
  where: { id },
  include: { posts: true }
});

// Paginated list
const posts = await prisma.post.findMany({
  take: 20,
  skip: page * 20,
  orderBy: { createdAt: 'desc' }
});
```
-->

---

## State Management

<!-- TODO: Document state patterns -->
<!-- Example:
### Server State
Use React Server Components for data fetching.
Minimize client-side state.

### Client State
- Form state: React Hook Form
- Global state: Context API (avoid Redux for MVP)
- Server cache: SWR or React Query
-->

---

## Error Handling

<!-- TODO: Document error patterns -->
<!-- Example:
### API Routes
Return consistent error format:
```typescript
return NextResponse.json(
  { error: "Message" },
  { status: 400 }
);
```

### Client Components
Use error boundaries for graceful degradation.
Show user-friendly error messages.
-->

---

## Related Documentation

- **Workflow:** `development-workflow.md` - Step-by-step guides
- **API:** `api-patterns.md` - API route patterns
- **Components:** `component-patterns.md` - UI patterns
- **Standards:** `coding-standards.md` - Code quality
