---
name: seo-onpage
description: Add on-page SEO to a Next.js site — title/meta, Open Graph, canonical, structured data (schema.org JSON-LD), and sitemap/robots. Use when building or auditing pages for search visibility and link previews.
---

# seo-onpage

## Per page
- **Unique `<title>`** (≤ 60 chars) and **meta description** (≤ 155 chars). In Next.js App Router use the
  `metadata` export or `generateMetadata`.
- **Open Graph + Twitter** tags: `og:title`, `og:description`, `og:image` (1200×630), `og:url`, `twitter:card`.
- **Canonical URL** to avoid duplicate-content splits.
- **One `<h1>`** per page; headings in order.

## Site-wide
- `app/sitemap.ts` and `app/robots.ts` (Next.js generate these natively).
- **Structured data** (JSON-LD) for the page type: `Organization`, `LocalBusiness`, `Product`, `Article`,
  `BreadcrumbList`. Hand off complex schemas to a schema-markup skill if available.
- Descriptive, keyword-aware URLs; no `?id=` for primary pages.

## Output
- The `metadata`/`generateMetadata` block per page.
- `sitemap.ts` + `robots.ts`.
- JSON-LD `<script type="application/ld+json">` for the right type.

## Guardrails
- Don't keyword-stuff. One clear topic per page.
- `og:image` must be an absolute URL. Verify the preview actually renders (don't assume).
