## Web (Next.js)

- **Accessibility:** WCAG 2.2 AA. Semantic HTML, labelled inputs, alt text, visible focus, keyboard-navigable.
- **Responsive:** works at 375px width minimum. Test mobile before calling a layout done.
- **SEO basics:** unique `<title>` + meta description per page, Open Graph tags, canonical URL, sitemap.
- **Performance budget:** Core Web Vitals — LCP < 2.5s, CLS < 0.1, INP < 200ms. Lazy-load below-the-fold images.
- **No secrets in client code.** Anything in a Next.js client component or `NEXT_PUBLIC_*` is public.
- **Server components by default;** add `"use client"` only where interactivity needs it.
- **Validate input at the boundary** (server actions / route handlers), not just in the UI.
