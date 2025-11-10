-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.actors (
  id integer NOT NULL DEFAULT nextval('actors_id_seq'::regclass),
  name character varying NOT NULL UNIQUE,
  CONSTRAINT actors_pkey PRIMARY KEY (id)
);
CREATE TABLE public.categories (
  id integer NOT NULL DEFAULT nextval('categories_id_seq'::regclass),
  name character varying NOT NULL UNIQUE,
  CONSTRAINT categories_pkey PRIMARY KEY (id)
);
CREATE TABLE public.content_types (
  id integer NOT NULL DEFAULT nextval('content_types_id_seq'::regclass),
  name character varying NOT NULL UNIQUE,
  CONSTRAINT content_types_pkey PRIMARY KEY (id)
);
CREATE TABLE public.countries (
  id integer NOT NULL DEFAULT nextval('countries_id_seq'::regclass),
  name character varying NOT NULL UNIQUE,
  CONSTRAINT countries_pkey PRIMARY KEY (id)
);
CREATE TABLE public.directors (
  id integer NOT NULL DEFAULT nextval('directors_id_seq'::regclass),
  name character varying NOT NULL UNIQUE,
  CONSTRAINT directors_pkey PRIMARY KEY (id)
);
CREATE TABLE public.duration_types (
  id integer NOT NULL DEFAULT nextval('duration_types_id_seq'::regclass),
  name character varying NOT NULL UNIQUE,
  CONSTRAINT duration_types_pkey PRIMARY KEY (id)
);
CREATE TABLE public.movie_actors (
  movie_id integer NOT NULL,
  actor_id integer NOT NULL,
  CONSTRAINT movie_actors_pkey PRIMARY KEY (movie_id, actor_id),
  CONSTRAINT movie_actors_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id),
  CONSTRAINT movie_actors_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actors(id)
);
CREATE TABLE public.movie_categories (
  movie_id integer NOT NULL,
  category_id integer NOT NULL,
  CONSTRAINT movie_categories_pkey PRIMARY KEY (movie_id, category_id),
  CONSTRAINT movie_categories_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id),
  CONSTRAINT movie_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id)
);
CREATE TABLE public.movie_countries (
  movie_id integer NOT NULL,
  country_id integer NOT NULL,
  CONSTRAINT movie_countries_pkey PRIMARY KEY (movie_id, country_id),
  CONSTRAINT movie_countries_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id),
  CONSTRAINT movie_countries_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.countries(id)
);
CREATE TABLE public.movie_directors (
  movie_id integer NOT NULL,
  director_id integer NOT NULL,
  CONSTRAINT movie_directors_pkey PRIMARY KEY (movie_id, director_id),
  CONSTRAINT movie_directors_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id),
  CONSTRAINT movie_directors_director_id_fkey FOREIGN KEY (director_id) REFERENCES public.directors(id)
);
CREATE TABLE public.movies (
  id integer NOT NULL DEFAULT nextval('movies_id_seq'::regclass),
  show_code character varying NOT NULL,
  title character varying NOT NULL,
  description text,
  date_added date,
  release_year integer,
  duration_int integer,
  content_type_id integer NOT NULL,
  rating_id integer,
  duration_type_id integer,
  platform_id integer,
  CONSTRAINT movies_pkey PRIMARY KEY (id),
  CONSTRAINT movies_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES public.content_types(id),
  CONSTRAINT movies_rating_id_fkey FOREIGN KEY (rating_id) REFERENCES public.ratings(id),
  CONSTRAINT movies_duration_type_id_fkey FOREIGN KEY (duration_type_id) REFERENCES public.duration_types(id),
  CONSTRAINT movies_platform_id_fkey FOREIGN KEY (platform_id) REFERENCES public.platforms(id)
);
CREATE TABLE public.platforms (
  id integer NOT NULL DEFAULT nextval('platforms_id_seq'::regclass),
  name character varying NOT NULL UNIQUE,
  CONSTRAINT platforms_pkey PRIMARY KEY (id)
);
CREATE TABLE public.ratings (
  id integer NOT NULL DEFAULT nextval('ratings_id_seq'::regclass),
  code character varying NOT NULL UNIQUE,
  CONSTRAINT ratings_pkey PRIMARY KEY (id)
);