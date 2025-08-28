# Prompt 7: Hydration Error Fix

**User Request:**
```
excellent. before moving on, lets clear up a few small issues in the frontend: In HTML, <div> cannot be a descendant of <p>.
This will cause a hydration error.
```

**Context:** User identified React hydration error caused by invalid HTML nesting - specifically `<div>` elements (Badge components) being nested inside `<p>` elements (CardDescription components).

**Assistant Response:** Fixed HTML nesting issues by:
1. Changing CardDescription from `<p>` to `<div>` element
2. Ensuring proper semantic HTML structure
3. Maintaining styling consistency

**Outcome:** Resolved hydration errors and invalid HTML nesting issues.