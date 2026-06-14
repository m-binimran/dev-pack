## Stack lock

- The stack is **Next.js + Supabase (Postgres)**. Don't introduce a different framework, ORM, or DB
  mid-project without the user agreeing first.
- Don't add a dependency when the stack already covers it (e.g. don't pull in a date library for one format call).
- Pin versions in `package.json`. No silent major-version bumps.
- One state-management approach per project — don't mix three.
