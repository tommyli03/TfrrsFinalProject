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

SELECT * 
FROM top_performers
ORDER BY race_year DESC, CAST(place AS UNSIGNED) ASC;

