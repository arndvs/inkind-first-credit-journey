# Spectator to Diner: First-Credit Journey

Implementation sketch · Aaron Davis · October 2026

How I'd build one Braze journey end to end: get browse intent and the referral reward onto the profile, then send a pre-dinner nudge to referred users who haven't made a first purchase.

**Why this one:** I signed up through a referral on October 8 with a $25 reward toward my first $50+ meal. That first day I spent time in the app, zooming in and out of San Diego's neighborhoods. Then a few days went by with no messages from inKind. One random day I opened it again, searched a few neighborhoods, and saved a restaurant or two. After that I mostly forgot about it.

On Saturday, October 24, my wife and I were deciding on takeout. We'd already spent time on Google Maps looking for places to order, and inKind didn't come to mind. It wasn't a lack of interest. Nothing reminded me it was there.

I'd have used the reward if a message had reached me that Saturday night. One or two messages in the weeks before would have kept inKind top of mind when we started looking.

The message I'd have wanted was simple: you saved these restaurants, your $25 is waiting, here's one near you tonight. Everything it needed was already in my account: the restaurants I saved and the reward I hadn't used. This repo is how I'd get those signals onto the Braze profile, act on them, and time the messages so they arrive before someone is choosing dinner. It's the same idea behind the recency and frequency segments I've built before: message people based on what they've done and what they haven't.

---

## What's built here

| File | What it contains |
|---|---|
| [`01-data-contract.md`](./01-data-contract.md) | The profile fields, two sync paths (real-time `/users/track` for events, Snowflake Cloud Data Ingestion for computed attributes), sample payloads, the sync view, sync rules |
| [`02-journey.md`](./02-journey.md) | Audience rules, audience SQL, the Canvas flow, and a second Canvas for new users who browse without saving |
| [`03-message.liquid`](./03-message.liquid) | The template: saved-restaurant personalization from a Catalog, a Connected Content call for nearby picks with its own fallback, and an abort when there's no unused reward |
| [`04-qa-and-measurement.md`](./04-qa-and-measurement.md) | Pre-launch send-safety and rendering checks, how I'd ship the backend change, metrics by cohort, what I'd confirm first |

With only a few minutes, start with the "Who can receive it" checks in [`04-qa-and-measurement.md`](./04-qa-and-measurement.md). They decide who can get a message before anything sends.

---

## Conventions

- **Every event, attribute, table, endpoint, and threshold name is illustrative**, to be mapped to inKind's existing schema. I don't have access to inKind's data model, so this is a best guess built from the public Braze docs and my experience as one new user, including the reward terms shown in the app. [`04-qa-and-measurement.md`](./04-qa-and-measurement.md) lists what I'd confirm first.
- Timings and thresholds (4:30 PM send, 48-hour wait, 30-day re-entry, three sessions in 14 days) are starting points to test, not conclusions.
