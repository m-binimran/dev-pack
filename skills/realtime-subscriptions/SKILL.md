---
name: realtime-subscriptions
description: Add Supabase Realtime to a Next.js app — Postgres Changes, Broadcast, and Presence — with proper cleanup and RLS-aware channels. Use when building live updates, presence indicators, or collaborative features.
---

# realtime-subscriptions

Live data is a client concern (it needs a persistent connection). Wire it carefully and always clean up.

## Pick the mechanism
| Need | Use |
|------|-----|
| React to DB inserts/updates/deletes | **Postgres Changes** |
| Ephemeral messages (cursors, typing) | **Broadcast** |
| Who's online / shared state | **Presence** |

## Process
1. **Subscribe in a client component**, inside `useEffect`. Realtime can't live in a server component.
2. **Always unsubscribe** in the effect cleanup (`supabase.removeChannel(channel)`) — leaked channels pile up
   and cause duplicate handlers.
3. **RLS applies to Realtime.** A client only receives change events for rows it's allowed to read. Enable
   Realtime on the table and confirm the policies.
4. **Reconcile with your cache:** on an event, update the query cache (`state-architect`) rather than keeping a
   parallel copy. Handle reconnects (refetch on `SUBSCRIBED` after a drop).
5. **Don't over-subscribe:** scope channels narrowly (filter by id); a firehose channel is a performance and
   cost problem.

## Output
- The channel setup, the cleanup, the RLS/Realtime enablement note, and how events update the UI/cache.

## Guardrails
- Every subscription has a matching cleanup — no exceptions (memory + duplicate-event bugs).
- Realtime is not your security layer; RLS is. Don't broadcast data the user can't already read.
