---
name: storage-upload
description: Handle file uploads with Supabase Storage in Next.js — buckets, RLS on objects, signed URLs, image handling, and size/type validation. Use when adding avatars, portfolio images, document uploads, or any user file.
---

# storage-upload

User files are untrusted input. Validate, scope access, and never expose a writable public bucket.

## Process
1. **Bucket per purpose, private by default.** Public bucket only for genuinely public assets. Set
   `fileSizeLimit` and `allowedMimeTypes` on the bucket.
2. **RLS on `storage.objects`:** users may only write/read paths they own — e.g. key prefixed with their
   `auth.uid()`. Policies mirror the `rls-policy` skill (using + with check).
3. **Validate before upload:** size and MIME on the client for UX, and again server-side / via bucket limits
   for safety. Reject executables and oversized files.
4. **Serve privately via signed URLs:** `createSignedUrl(path, expiresIn)` with a short TTL. Don't hand out
   permanent public URLs for private content.
5. **Images:** store an original; render through `next/image` (or a transform) — sized to avoid CLS.
   Strip EXIF if privacy matters.

## Output
- Bucket config, the storage RLS policies, the upload handler (with validation), and how files are served
  (signed URL vs public).

## Guardrails
- Never make a user-writable bucket public-read without considering what else lands in it.
- Path scoping by `auth.uid()` is mandatory for private user files.
- Size/type limits enforced server-side (bucket), not just in the UI.
