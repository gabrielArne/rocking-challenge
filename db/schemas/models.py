from __future__ import annotations

from datetime import date

from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base declarativa para todos los modelos."""


movie_directors = Table(
    "movie_directors",
    Base.metadata,
    Column(
        "movie_id",
        ForeignKey("movies.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "director_id",
        ForeignKey("directors.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Index("ix_movie_directors_movie_id", "movie_id"),
    Index("ix_movie_directors_director_id", "director_id"),
)

movie_actors = Table(
    "movie_actors",
    Base.metadata,
    Column(
        "movie_id",
        ForeignKey("movies.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "actor_id",
        ForeignKey("actors.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Index("ix_movie_actors_movie_id", "movie_id"),
    Index("ix_movie_actors_actor_id", "actor_id"),
)

movie_countries = Table(
    "movie_countries",
    Base.metadata,
    Column(
        "movie_id",
        ForeignKey("movies.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "country_id",
        ForeignKey("countries.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Index("ix_movie_countries_movie_id", "movie_id"),
    Index("ix_movie_countries_country_id", "country_id"),
)

movie_categories = Table(
    "movie_categories",
    Base.metadata,
    Column(
        "movie_id",
        ForeignKey("movies.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "category_id",
        ForeignKey("categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Index("ix_movie_categories_movie_id", "movie_id"),
    Index("ix_movie_categories_category_id", "category_id"),
)


class ContentType(Base):
    __tablename__ = "content_types"
    __table_args__ = (UniqueConstraint("name", name="uq_content_types_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    movies: Mapped[list["Movie"]] = relationship(back_populates="content_type")


class Director(Base):
    __tablename__ = "directors"
    __table_args__ = (UniqueConstraint("name", name="uq_directors_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary=movie_directors,
        back_populates="directors",
    )


class Actor(Base):
    __tablename__ = "actors"
    __table_args__ = (UniqueConstraint("name", name="uq_actors_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary=movie_actors,
        back_populates="actors",
    )


class Country(Base):
    __tablename__ = "countries"
    __table_args__ = (UniqueConstraint("name", name="uq_countries_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary=movie_countries,
        back_populates="countries",
    )


class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (UniqueConstraint("code", name="uq_ratings_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    movies: Mapped[list["Movie"]] = relationship(back_populates="rating")


class DurationType(Base):
    __tablename__ = "duration_types"
    __table_args__ = (UniqueConstraint("name", name="uq_duration_types_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    movies: Mapped[list["Movie"]] = relationship(back_populates="duration_type")


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("name", name="uq_categories_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)

    movies: Mapped[list["Movie"]] = relationship(
        secondary=movie_categories,
        back_populates="categories",
    )


class Platform(Base):
    __tablename__ = "platforms"
    __table_args__ = (UniqueConstraint("name", name="uq_platforms_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    movies: Mapped[list["Movie"]] = relationship(back_populates="platform")


class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (Index("ix_movies_title", "title"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    show_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(Text())
    date_added: Mapped[date | None] = mapped_column(Date)
    release_year: Mapped[int | None] = mapped_column(Integer)
    duration_int: Mapped[int | None] = mapped_column(Integer)

    content_type_id: Mapped[int] = mapped_column(
        ForeignKey("content_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    rating_id: Mapped[int | None] = mapped_column(
        ForeignKey("ratings.id", ondelete="RESTRICT"),
        index=True,
    )
    duration_type_id: Mapped[int | None] = mapped_column(
        ForeignKey("duration_types.id", ondelete="RESTRICT"),
        index=True,
    )
    platform_id: Mapped[int | None] = mapped_column(
        ForeignKey("platforms.id", ondelete="RESTRICT"),
        index=True,
    )

    content_type: Mapped[ContentType] = relationship(back_populates="movies")
    rating: Mapped[Rating | None] = relationship(back_populates="movies")
    duration_type: Mapped[DurationType | None] = relationship(back_populates="movies")
    platform: Mapped[Platform | None] = relationship(back_populates="movies")

    directors: Mapped[list[Director]] = relationship(
        secondary=movie_directors,
        back_populates="movies",
    )
    actors: Mapped[list[Actor]] = relationship(
        secondary=movie_actors,
        back_populates="movies",
    )
    countries: Mapped[list[Country]] = relationship(
        secondary=movie_countries,
        back_populates="movies",
    )
    categories: Mapped[list[Category]] = relationship(
        secondary=movie_categories,
        back_populates="movies",
    )
