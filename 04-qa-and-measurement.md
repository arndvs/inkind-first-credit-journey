# 04 — QA and Measurement

Success is a higher first-purchase rate within 7 days of entry than the 10% control group.

---

## 1. Before launch

- [ ] Test profile shows each event and attribute with the right type (User Search, event user log)
- [ ] Liquid preview for five test users: saved restaurant, nothing saved, nothing saved with the recommendations endpoint down, zero balance, no balance attribute (last two abort)
- [ ] Cloud Data Ingestion sync run shows the expected row count, and a test user's `wallet_balance` updates after a change in Snowflake
- [ ] Braze audience count matches the warehouse SQL within an expected margin
- [ ] Send time resolves to the user's local time; quiet hours respected
- [ ] Links are tracked and deep-link into the app; email renders in Gmail, Outlook, and Apple Mail
- [ ] A test purchase removes the test user from the Canvas

## 2. After launch

| Metric | Type |
|---|---|
| First purchase within 7 days, journey vs. control | Primary |
| Credit redemption rate | Secondary |
| Days from signup to first purchase | Secondary |
| Results by signup-week cohort, journey vs. control | Secondary |
| Unsubscribes and push opt-outs | Guardrail |

---

## 3. What I'd confirm first

| Question | Why it matters |
|---|---|
| Are browse and save events already reaching Braze, or only transactions? | Decides whether this is a data gap or a journey gap |
| Is wallet balance on the profile, and how often does it sync? | A stale balance means the wrong message, or a send to someone with nothing to spend |
| How does the wallet change at payment (credit applied, cash back earned)? | Decides what the purchase event and balance update look like, and whether the message should mention earning, not just spending |
| What share of new users allow push? | Decides how much email has to carry |
| Does an existing referral or onboarding Canvas overlap with this one? | Avoids double messaging; may mean extending a Canvas instead of adding one |
