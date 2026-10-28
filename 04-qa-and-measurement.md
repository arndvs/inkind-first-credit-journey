# 04 — QA, Shipping, and Measurement

Success is a higher first-purchase rate within 7 days of entry than the 10% control group.

---

## 1. Before launch

### Who can receive it

- [ ] Canvas built and tested in a Braze dev workspace before it exists in production
- [ ] Test sends go only to an internal seed group
- [ ] Each message step checks that channel's subscription state, so an unsubscribed user who is in the Canvas still gets nothing on that channel
- [ ] Audience previewed against known test users (opted in, opted out, unsubscribed) before launch
- [ ] Braze audience count is at or below the warehouse SQL count, and the gap matches users with no push or email permission
- [ ] Send time resolves to the user's local time; quiet hours respected
- [ ] A second person reviews the Canvas and audience before it goes live

### What they see

- [ ] Test profile shows each event and attribute with the right type (User Search, event user log)
- [ ] Liquid preview for six test users: saved restaurant found in the Catalog, saved ID missing from the Catalog, nothing saved, nothing saved with the recommendations endpoint down, zero balance, no balance attribute (last two abort)
- [ ] Rendered push has no leading or trailing blank lines, shows "$25" and "$12.50" correctly, and stays under the push length limit with three long restaurant names
- [ ] Cloud Data Ingestion sync run shows the expected row count, and a test user's `wallet_balance` updates after a change in Snowflake
- [ ] Links are tracked and deep-link into the app; email renders in Gmail, Outlook, and Apple Mail
- [ ] A test purchase removes the test user from the Canvas

---

## 2. How I'd ship it

- Add the `restaurant_saved` event and the `saved_restaurants` update to the Rails backend, sent to `/users/track` from a background job so the request path never waits on Braze
- Run it locally against Postgres and the Braze dev workspace, then check the test profile in User Search
- Open a PR with the payload change and a test for the event shape
- Turn on the Canvas in production only after the checks in section 1 pass

---

## 3. After launch

| Metric | Type |
|---|---|
| First purchase within 7 days, journey vs. control | Primary |
| Credit redemption rate | Secondary |
| Days from signup to first purchase | Secondary |
| Results by signup-week cohort, journey vs. control | Secondary |
| Unsubscribes and push opt-outs | Guardrail |

---

## 4. What I'd confirm first

| Question | Why it matters |
|---|---|
| Are browse and save events already reaching Braze, or only transactions? | Decides whether this is a data gap or a journey gap |
| Is wallet balance on the profile, and how often does it sync? | A stale balance means the wrong message, or a send to someone with nothing to spend |
| How does the wallet change at payment (credit applied, cash back earned)? | Decides what the purchase event and balance update look like, and whether the message should mention earning, not just spending |
| What share of new users allow push? | Decides how much email has to carry |
| Does an existing referral or onboarding Canvas overlap with this one? | Avoids double messaging; may mean extending a Canvas instead of adding one |
