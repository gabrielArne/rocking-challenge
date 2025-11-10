CREATE OR REPLACE PROCEDURE public.sp_get_top5_pelis_largas(
    IN p_year INT,
    INOUT ref refcursor DEFAULT 'top5_pelis_largas'
)
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN ref FOR
        SELECT m.show_code,
               m.title,
               m.duration_int AS duration_minutes,
               m.release_year,
               p.name AS platform
        FROM public.movies AS m
        LEFT JOIN public.platforms AS p ON p.id = m.platform_id
        LEFT JOIN public.duration_types AS dt ON dt.id = m.duration_type_id
        WHERE m.release_year = p_year
          AND m.duration_int IS NOT NULL
          AND dt.name ='min'
        ORDER BY m.duration_int DESC, m.title ASC
        LIMIT 5;
END;
$$;



-- EJEMPLO DE USO 

-- CALL public.sp_get_top5_pelis_largas(2019, 'cur'); FETCH ALL FROM cur;