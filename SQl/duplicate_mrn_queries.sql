-- ============================================
-- Duplicate MRN Analytics Platform
-- SQL Analysis Queries
-- Version 1: Flat File Analysis
-- ============================================

-- Total duplicate investigations

SELECT COUNT(*) AS total_duplicates
FROM duplicate_events;

------------------------------------------------

-- Duplicates by source

SELECT
    source,
    COUNT(*) AS duplicate_count
FROM duplicate_events
GROUP BY source
ORDER BY duplicate_count DESC;

------------------------------------------------

-- Duplicates by department

SELECT
    department_name,
    COUNT(*) AS duplicate_count
FROM duplicate_events
GROUP BY department_name
ORDER BY duplicate_count DESC;

------------------------------------------------

-- Duplicate investigations by source and status

SELECT
    source,
    status,
    COUNT(*) AS duplicate_count
FROM duplicate_events
GROUP BY source, status
ORDER BY source, status;

------------------------------------------------

-- KND investigations by department

SELECT
    department_name,
    COUNT(*) AS KND_count
FROM duplicate_events
WHERE resolution_type = 'KND'
GROUP BY department_name
ORDER BY KND_count DESC;

------------------------------------------------

-- Monthly duplicate trend

SELECT
    strftime('%Y-%m', event_date) AS month,
    COUNT(*) AS duplicate_count
FROM duplicate_events
GROUP BY month
ORDER BY month;

------------------------------------------------

-- Contributing factor types

SELECT
    contributing_factor_types,
    COUNT(*) AS duplicate_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM duplicate_events),
        1
    ) AS percent_of_total
FROM duplicate_events
GROUP BY contributing_factor_types
ORDER BY duplicate_count DESC;

------------------------------------------------

-- Primary categories

SELECT
    primary_categories,
    COUNT(*) AS duplicate_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM duplicate_events),
        1
    ) AS percent_of_total
FROM duplicate_events
GROUP BY primary_categories
ORDER BY duplicate_count DESC;