# Spectator to Diner: First-Credit Journey

Implementation sketch · Aaron Davis · October 2026

How I'd build one Braze journey end to end: get browse intent and credit onto the profile, then send a pre-dinner nudge to referred users who haven't made a first purchase.

**Why this one:** I signed up through a referral earlier this month, opened the app several times, and saved two restaurants, but never used my $25 credit. Nothing I received reminded me of it, and one night I ordered dinner without inKind coming to mind.

---

## What's built here

| File | What it contains |
|---|---|
| [`01-data-contract.md`](./01-data-contract.md) | The profile fields, two sync paths (real-time `/users/track` for events, Snowflake Cloud Data Ingestion for computed attributes), sample payloads, the sync view, sync rules |
| [`02-journey.md`](./02-journey.md) | Audience rules, audience SQL, the Canvas flow |
| [`03-message.liquid`](./03-message.liquid) | The template: saved-restaurant personalization, a Connected Content call for nearby picks with its own fallback, and an abort when there's no credit |
| [`04-qa-and-measurement.md`](./04-qa-and-measurement.md) | Pre-launch QA, metrics by cohort, what I'd confirm first |

---

## Conventions

- **Every event, attribute, table, endpoint, and threshold name is illustrative**, to be mapped to inKind's existing schema. I don't have access to the real data model; this is a best guess built from the public Braze docs and my experience as one new user, and there's a lot about inKind's data and constraints I don't know. [`04-qa-and-measurement.md`](./04-qa-and-measurement.md) lists what I'd confirm first.
- Timings (4:30 PM send, 48-hour wait, 30-day re-entry) are starting points to test, not conclusions.
