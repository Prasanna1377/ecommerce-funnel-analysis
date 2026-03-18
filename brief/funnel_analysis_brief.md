# Ecommerce Funnel Analysis
**Dataset:** REES46 Multi-Category Store, October 2019 (42M events)  
**Author:** [Your name]  
**Date:** March 2026

---

## What I was trying to answer
I wanted to understand where users drop off in the purchase funnel of a 
multi-category ecommerce store, which product categories and brands convert 
best, and where the biggest opportunities to improve conversion actually are.

---

## What I found

### Electronics is carrying the whole store
Electronics makes up 56% of all traffic and converts at 3.18% — almost double 
every other category. It's not just the biggest category, it's also the 
healthiest one. If I were setting conversion targets for this team, I'd use 
electronics as the benchmark, not the blended site average which flatters 
everything else.

### Apparel has a real problem
14,000+ views, barely any purchases. The view-to-purchase rate sits at 0.48% 
which is the worst of any major category by a wide margin. Something is broken 
between the product page and checkout for apparel specifically — my best guess 
is missing size/fit information or weak trust signals, but this needs session 
recordings and user interviews to diagnose properly. Of everything in this 
analysis, this is the one I'd bring to a PM first thing Monday morning.

### People who shop by brand already know what they want
Samsung and Apple both convert above 4%. Apple does it at an average order 
value of $868 — more than 2.5x Samsung's $334 — with almost identical 
conversion. These users arrive ready to buy. The store doesn't need to 
convince them, it just needs to get out of their way. Smaller brands sit 
between 1-2% regardless of price, which tells me brand recognition is doing 
more work here than price point.

### Nobody is coming back to finish their purchase
The median time from first view to purchase is 2.4 minutes. 94% of people 
who buy do it within the same hour they started browsing. This was the finding 
that surprised me most and it changes how I'd think about the whole growth 
strategy for this store. Retargeting campaigns, abandoned cart emails, 
re-engagement flows — these are probably wasted budget here. The decision 
happens in session or not at all. That means the highest leverage thing the 
team can do is ruthlessly remove friction from the in-session experience.

---

## What I'd recommend

**Fix apparel first.** Even getting it to 1.5% conversion (from 0.48% today) 
would generate roughly 145 incremental purchases per 500k event window. That's 
a meaningful number and the category has the most obvious room to improve.

**Audit the checkout flow for unnecessary steps.** Given how fast purchase 
decisions happen, mandatory account creation, extra confirmation screens, or 
slow page loads are directly costing conversions. This is the kind of change 
that is easy to A/B test and compounds across every category.

**Surface top brands more prominently in search and navigation.** Samsung, 
Apple, Xiaomi and Huawei are self-converting — users who find them buy them. 
More prominent placement costs nothing and should move both conversion rate 
and average order value.

**Look into the direct-to-purchase pattern.** A handful of brands (Elenberg, 
Lucente, Dauscher) show purchases with zero cart events in the data — people 
seem to be skipping the cart entirely. That could be a bug, or it could be a 
faster checkout path that's worth understanding and potentially replicating.

---

## What I'd dig into next with more time
- Weekly purchase patterns and day-of-week effects (the sample only covered 
  one day so this needs the full dataset)
- Whether there's a price threshold above which conversion drops sharply 
  in each category
- Sub-category breakdowns — `electronics.smartphone` and `electronics.audio` 
  probably look very different from each other
- Which specific products get added to cart but never purchased

---

*Full analysis in `notebooks/01_setup_exploration.ipynb`. 
SQL translation in `sql/funnel_analysis.sql`.*