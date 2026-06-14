## Token budget

- Grep/glob before reading. Read line-ranges, not whole files, once you know where to look.
- Don't re-read a file you just edited to "verify" — the edit tool already confirmed it.
- Don't dump large outputs back to the user; summarize and keep the raw output in a tool result.
- Reuse what's already in context. Don't re-derive facts already established.
- For web lookups, fetch the specific page, not a broad crawl.
- Suggest `/clear` when switching to an unrelated task so old context stops costing tokens.
