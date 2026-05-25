# Isaac & Elijah's Car Wash — Marketing Kit

Everything in this folder is ready to use. The visual system is documented in `design-philosophy.md` ("Driveway Sunlight") and rendered by `build_assets.py` — re-run that script any time the photo, phone number, or QR target changes.

---

## The audience

Queen Creek Villages homeowners. Average lot ~2,000 sq ft. Mostly working parents, kids at home, two cars in the driveway, weekends spoken for. The decision happens at the front door in under 30 seconds.

They are *not* deciding whether $20 is fair — they're deciding whether *these two kids* are trustworthy and whether *now* is the right time. Lead with faces, neighborhood, price up front. Pay buys time back.

---

## The assets

| File | Use | Notes |
|---|---|---|
| `flyer-print-letter.pdf` | Leave-behind one-pager | US Letter, 200 DPI. Print on cream or white cardstock if possible. |
| `flyer-print-letter.png` | Same as the PDF | Use if a printer prefers PNG. |
| `social-instagram-1080.png` | Instagram feed post | 1080×1080. |
| `social-facebook-1200x630.png` | Facebook post / link preview | 1200×630. Also works for Nextdoor. |
| `../images/qr-site.png` | The QR code itself | Already embedded in the flyer and on the live site. |

---

## The print flyer

**When to use:** the homeowner says "Not today, but maybe later" or "Let me think." Hand them the flyer instead of disappearing.

**Printing tips:**

- Print at 100% scale (do NOT "fit to page" — it will shrink the margins).
- Cream or natural-white 80–100 lb cardstock looks like real artisan signage and signals quality at a glance. Plain copy paper is fine too.
- One sheet folded in thirds also works as a small leave-behind if you want to slip it under a doormat.

**Quantity for one Saturday:** print 40–60. They cost pennies and give a graceful exit when someone passes.

---

## SMS — copy-paste templates

These are written for SMS specifically: short, no slang, no emoji overload, the link as the last thing so previews look clean. The site URL `https://isaac-elijah-carwash.vercel.app` will auto-expand into a tappable preview card on most phones.

### 1. Cold neighbor blast — "we're new, here's what we do"

> Hi! Isaac & Elijah here — Queen Creek Villages neighbors. We're hand-washing cars this summer to save up for a real business idea. Full exterior, hand-scrubbed, brake-dust gone — $20 flat. Want one? Text this number with your car, date, and a good time.
>
> https://isaac-elijah-carwash.vercel.app

*Why it works:* names + neighborhood in the first 7 words → not a scam. Specific offer + specific price → no ambiguity. "Save up for a real business idea" → the working-parent hook. Ends with a clear ask.

### 2. After-the-knock follow-up — they said "maybe"

> Thanks for chatting earlier — this is Isaac & Elijah. Here's our site if you want to look later: https://isaac-elijah-carwash.vercel.app — we can usually do same-day or weekend. Just text us back when you're ready. 🚗

*Why it works:* references the in-person moment. Removes friction. Reassures availability. Single emoji is friendly without trying too hard.

### 3. Forwardable share — for a happy neighbor to send to friends

> If anyone in the Villages needs a car wash this summer — these two neighborhood teens (Isaac & Elijah) did a great job on ours. $20, hand-washed, even got the brake dust off the wheels. Text (480) 853-8729 — or see https://isaac-elijah-carwash.vercel.app

*Why it works:* written in a parent's voice, third-person endorsement. Lists the specific result that made them happy (brake dust). Both contact methods included.

### 4. Group chat / Nextdoor short version

> Local kids hand-washing cars — Isaac & Elijah from QC Villages. $20 flat, brake dust removal included. (480) 853-8729 · isaac-elijah-carwash.vercel.app

*Use this when:* posting to a neighborhood Slack/Discord/Nextdoor/Facebook group where char count matters.

### 5. Booking confirmation — Isaac & Elijah send this back

> Got it! Confirming a wash for [CAR] on [DATE] around [TIME]. We'll knock when we're there. $20, Zelle (this number) or cash works. — Isaac & Elijah

*Use this:* every single time, so the customer has a record of what they agreed to.

---

## Social posts

### Instagram (1080×1080)

Suggested caption:

> Hi neighbors 👋 We're Isaac & Elijah, two Queen Creek Villages teens hand-washing cars this summer to save up for a real business idea.
>
> $20 flat. Full exterior. Brake-dust decon on the wheels. Hand-dried so you don't get water spots. We walk to you.
>
> Text us: (480) 853-8729
> Zelle (same number) or cash.
>
> #queencreek #queencreekvillages #carwash #localkids #shoplocal

### Facebook (1200×630)

Suggested post text:

> Hand car wash by your neighbors. Two Queen Creek Villages teens (Isaac & Elijah) are saving up for a summer business — and giving you the cleanest car on the cul-de-sac while they do it.
>
> $20 flat, exterior. Brake dust off the wheels. Hand-dried, no water spots. We walk to you anywhere in QC Villages.
>
> 📱 Text (480) 853-8729 — Zelle to the same number or cash.
> 🌐 isaac-elijah-carwash.vercel.app

### Nextdoor

Use the Facebook post above — Nextdoor's audience is the exact same person, just with their guard up about "is this a scam?" so the neighborhood name in the first sentence is doing real work.

---

## What to do at the door

A quick script that matches the tone of the site and the flyer:

1. **Hand them the phone, open to the site.** Don't pitch. Let the page do it. Say: *"Hi, I'm Isaac and this is my brother Elijah. We live a couple streets over. Our site explains what we do — mind taking a look?"*
2. **Wait quietly.** Let them scroll. The hero, price chips, and portrait do the work in about 15 seconds.
3. **If they say yes:** ask car, date, time. Confirm in the SMS template above.
4. **If they say maybe:** hand them the printed flyer. Say: *"No worries — here's a little flyer with our number and a QR code. Text us whenever."*
5. **If they say no:** thank them politely, move on. The next door might say yes.

---

## A note on the design

The visual system is called **Driveway Sunlight** — the philosophy is in `design-philosophy.md`. The short version: deep navy + warm cream + one bright sun-yellow accent. Big confident type. Photo of the boys is the centerpiece every time. No clip-art, no cartoon bubbles, no Comic Sans. The whole thing should feel like *small honest commerce* — the lemonade stand grown up.

If you ever need to refresh the kit (new photo, different phone number, new offer), edit the top of `build_assets.py` and re-run it. Everything regenerates in under a second.
