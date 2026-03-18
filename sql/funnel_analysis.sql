-- ============================================================
-- Ecommerce Funnel Analysis
-- Dataset: REES46 Multi-Category Store (Oct 2019)
-- Author: [Your name]
-- Purpose: Reproduce core funnel metrics from Python analysis
--          in warehouse-ready SQL (BigQuery / Redshift syntax)
-- ============================================================


-- ── CTE 1: Classify each event ──────────────────────────────
-- Pull the three event types we care about and parse
-- the category hierarchy from the dot-separated string

WITH events AS (
    SELECT
        user_id,
        user_session,
        product_id,
        event_type,
        event_time,
        price,
        brand,
        SPLIT_PART(category_code, '.', 1) AS cat_l1,
        SPLIT_PART(category_code, '.', 2) AS cat_l2
    FROM ecommerce_events
    WHERE event_type IN ('view', 'cart', 'purchase')
      AND category_code IS NOT NULL
),


-- ── CTE 2: Session-level funnel flags ───────────────────────
-- For each session, flag whether it contained a view,
-- cart, and/or purchase event. This is the correct way
-- to measure funnel conversion — at the session level,
-- not raw event counts which inflate denominators.

session_funnel AS (
    SELECT
        user_session,
        user_id,
        MAX(CASE WHEN event_type = 'view'     THEN 1 ELSE 0 END) AS had_view,
        MAX(CASE WHEN event_type = 'cart'     THEN 1 ELSE 0 END) AS had_cart,
        MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS had_purchase
    FROM events
    GROUP BY user_session, user_id
),


-- ── CTE 3: Overall funnel rates ─────────────────────────────
-- Aggregate session flags to get top-level conversion rates

overall_funnel AS (
    SELECT
        COUNT(*)                                    AS total_sessions,
        SUM(had_view)                               AS sessions_with_view,
        SUM(had_cart)                               AS sessions_with_cart,
        SUM(had_purchase)                           AS sessions_with_purchase,
        ROUND(SUM(had_cart)     * 100.0 
              / NULLIF(SUM(had_view), 0), 2)        AS view_to_cart_pct,
        ROUND(SUM(had_purchase) * 100.0 
              / NULLIF(SUM(had_cart), 0), 2)        AS cart_to_purchase_pct,
        ROUND(SUM(had_purchase) * 100.0 
              / NULLIF(SUM(had_view), 0), 2)        AS view_to_purchase_pct
    FROM session_funnel
),


-- ── CTE 4: Funnel by category ───────────────────────────────
-- Break down conversion rates by top-level category
-- to identify which categories leak most in the funnel

category_funnel AS (
    SELECT
        e.cat_l1,
        COUNT(DISTINCT e.user_session)              AS total_sessions,
        COUNT(DISTINCT CASE 
            WHEN e.event_type = 'view' 
            THEN e.user_session END)                AS sessions_with_view,
        COUNT(DISTINCT CASE 
            WHEN e.event_type = 'purchase' 
            THEN e.user_session END)                AS sessions_with_purchase,
        ROUND(COUNT(DISTINCT CASE 
            WHEN e.event_type = 'purchase' 
            THEN e.user_session END) * 100.0
            / NULLIF(COUNT(DISTINCT CASE 
            WHEN e.event_type = 'view' 
            THEN e.user_session END), 0), 2)        AS view_to_purchase_pct
    FROM events e
    GROUP BY e.cat_l1
    ORDER BY total_sessions DESC
)


-- ── Final output: overall funnel ────────────────────────────
SELECT * FROM overall_funnel;

-- To get category breakdown instead, swap the last line for:
-- SELECT * FROM category_funnel;