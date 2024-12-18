-- Top Performers View computed from xc_nationals_results
CREATE OR REPLACE VIEW top_performers AS
SELECT 
    race_year,
    place,
    athlete_name,
    team,
    time_str,
    avg_mile
FROM xc_nationals_results
WHERE place > 0 AND place <= 10
ORDER BY race_year DESC, place ASC;

-- Querying top_performers
SELECT * 
FROM top_performers
ORDER BY race_year DESC, CAST(place AS UNSIGNED) ASC;

-- Team Rankings View for each year computed from xc_nationals_results
CREATE OR REPLACE VIEW xc_team_rankings AS
SELECT
    team_scores.race_year,
    team_scores.team,
    team_scores.total_score,
    RANK() OVER (PARTITION BY team_scores.race_year ORDER BY team_scores.total_score ASC) AS team_rank
FROM (
    SELECT
        race_year,
        team,
        SUM(CAST(score AS UNSIGNED)) AS total_score,
        COUNT(*) AS athlete_count
    FROM (
        SELECT
            race_year,
            team,
            score,
            ROW_NUMBER() OVER (
                PARTITION BY race_year, team
                ORDER BY CAST(score AS UNSIGNED) ASC
            ) AS rn
        FROM xc_nationals_results
        WHERE score IS NOT NULL AND CAST(score AS UNSIGNED) > 0
    ) AS ranked_athletes
    WHERE rn <= 5
    GROUP BY race_year, team
    HAVING COUNT(*) = 5  
) AS team_scores
ORDER BY team_scores.race_year DESC, team_rank ASC;

-- View for 5k analysis for 2024 nationals
CREATE OR REPLACE VIEW xc_2024_5k_analysis AS
SELECT
    xtr.team,
    xtr.team_rank AS meet_rank, 
    CONCAT(
        FLOOR(AVG(
            CAST(SUBSTRING_INDEX(xnr.fastest_5k, ':', 1) AS UNSIGNED) * 60 + 
            CAST(SUBSTRING_INDEX(xnr.fastest_5k, ':', -1) AS DECIMAL(10, 2))
        ) / 60), 
        ':', 
        LPAD(FORMAT(
            AVG(
                CAST(SUBSTRING_INDEX(xnr.fastest_5k, ':', 1) AS UNSIGNED) * 60 + 
                CAST(SUBSTRING_INDEX(xnr.fastest_5k, ':', -1) AS DECIMAL(10, 2))
            ) % 60, 
            2
        ), 5, '0')
    ) AS avg_5k_time_mm_ss,
    RANK() OVER (ORDER BY 
        AVG(
            CAST(SUBSTRING_INDEX(xnr.fastest_5k, ':', 1) AS UNSIGNED) * 60 + 
            CAST(SUBSTRING_INDEX(xnr.fastest_5k, ':', -1) AS DECIMAL(10, 2))
        )
    ) AS team_5k_rank
FROM
    xc_nationals_results xnr
INNER JOIN
    xc_team_rankings xtr
    ON xnr.race_year = xtr.race_year AND xnr.team = xtr.team
WHERE
    xnr.race_year = 2024
    AND xnr.fastest_5k IS NOT NULL 
GROUP BY
    xtr.team, xtr.team_rank 
ORDER BY
    team_5k_rank; 

