

-- Top 10 actores por participaciones en el año actual (Netflix y Disney+)
WITH current_year_movies AS (
    SELECT m.id
    FROM public.movies AS m
    JOIN public.platforms AS p ON p.id = m.platform_id
    WHERE m.release_year = EXTRACT(YEAR FROM CURRENT_DATE) -- no devuelve nada porque no hay pelis del 2025, modificar por ejemplo current_date - 1800 para obtener resultado
      AND p.name IN ('Netflix', 'Disney+')
)
SELECT a.name AS nombre_actor,
       COUNT(*) AS ctd_apariciones
FROM current_year_movies AS cym
JOIN public.movie_actors AS ma ON ma.movie_id = cym.id
JOIN public.actors AS a ON a.id = ma.actor_id
GROUP BY a.name
ORDER BY ctd_apariciones DESC, nombre_actor ASC
LIMIT 10;
