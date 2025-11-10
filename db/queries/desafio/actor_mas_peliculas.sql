SELECT a.name AS nombre_actor,
       COUNT(*) AS ctd_peliculas
FROM public.movies AS m
JOIN public.platforms AS p ON p.id = m.platform_id
JOIN public.movie_actors AS ma ON ma.movie_id = m.id
JOIN public.actors AS a ON a.id = ma.actor_id
WHERE p.id = 2
GROUP BY a.name
ORDER BY ctd_peliculas DESC
LIMIT 1;
