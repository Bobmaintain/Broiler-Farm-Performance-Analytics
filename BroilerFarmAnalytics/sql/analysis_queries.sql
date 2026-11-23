-- 1. Latest reported status for each flock
SELECT flock_id, MAX(date) AS latest_date,
       birds_placed, live_birds, avg_weight_kg
FROM daily_flock_records
GROUP BY flock_id;

-- 2. Daily feed consumption by flock
SELECT flock_id, date, feed_kg
FROM daily_flock_records
ORDER BY flock_id, date;

-- 3. Total recorded mortality by flock
SELECT flock_id, SUM(mortality_count) AS total_mortality
FROM daily_flock_records
GROUP BY flock_id;

-- 4. Total recorded costs by flock
SELECT flock_id,
       SUM(feed_cost_kwd) AS feed_cost_kwd,
       SUM(other_cost_kwd) AS other_cost_kwd
FROM daily_flock_records
GROUP BY flock_id;
