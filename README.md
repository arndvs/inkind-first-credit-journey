# Spectator to Diner: First-Credit Journey

Implementation sketch · Aaron Davis · October 2026

How I'd build one Braze journey end to end: get browse intent and credit onto the profile, then send a pre-dinner nudge to referred users who haven't made a first purchase.

**Why this one:** I signed up through a referral in October with $25 in credit. Over a couple of weekends I browsed the map, looked through different kinds of restaurants, and saved two. Then one Saturday my wife and I were deciding what's for dinner, and inKind didn't come to mind. It wasn't a lack of interest; nothing reminded me. The few emails I got were general brand messages.

The message I expected was simple: you saved these restaurants, your $25 is waiting, here's one near you tonight. Everything it needs was already in my account: the restaurants I saved and the credit I hadn't spent. This repo is how I'd get those signals onto the Braze profile and act on them. It's the same idea behind the recency and frequency segments I've built before: message people based on what they've done and what they haven't.

---

## What's built here

| File | What it contains |
|---|---|
| [`01-data-contract.md`](./01-data-contract.md) | The profile fields, two sync paths (real-time `/users/track` for events, Snowflake Cloud Data Ingestion for computed attributes), sample payloads, the sync view, sync rules |
| [`02-journey.md`](./02-journey.md) | Audience rules, audience SQL, the Canvas flow |
| [`03-message.liquid`](./03-message.liquid) | The template: saved-restaurant personalization from a Catalog, a Connected Content call for nearby picks with its own fallback, and an abort when there's no credit |
| [`04-qa-and-measurement.md`](./04-qa-and-measurement.md) | Pre-launch send-safety and rendering checks, how I'd ship the backend change, metrics by cohort, what I'd confirm first |

With only a few minutes, start with the "Who can receive it" checks in [`04-qa-and-measurement.md`](./04-qa-and-measurement.md). They decide who can get a message before anything sends.

---

## Conventions

- **Every event, attribute, table, endpoint, and threshold name is illustrative**, to be mapped to inKind's existing schema. I don't have access to inKind's data model, so this is a best guess built from the public Braze docs and my experience as one new user. [`04-qa-and-measurement.md`](./04-qa-and-measurement.md) lists what I'd confirm first.
- Timings (4:30 PM send, 48-hour wait, 30-day re-entry) are starting points to test, not conclusions.
