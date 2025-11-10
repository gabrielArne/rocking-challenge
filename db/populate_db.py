from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from schemas.models import (
    Actor,
    Category,
    ContentType,
    Country,
    Director,
    DurationType,
    Movie,
    Platform,
    Rating,
)

CSV_PATH = Path("data/raw/combined.csv")


def normalize(value) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    return text or None


def read_dataset() -> pd.DataFrame:
    if not CSV_PATH.is_file():
        raise FileNotFoundError(f"No se encontró el archivo {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    df["date_added"] = pd.to_datetime(
        df["date_added"], format="%B %d, %Y", errors="coerce"
    )
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
    df["duration_int"] = pd.to_numeric(df["duration_int"], errors="coerce")
    return df


def unique_values(series: pd.Series, *, split: bool = False) -> set[str]:
    values: set[str] = set()
    for item in series.dropna():
        if split:
            tokens = (normalize(token) for token in str(item).split(","))
        else:
            tokens = [normalize(item)]
        for token in tokens:
            if token:
                values.add(token)
    return values


def create_dimension(
    session: Session,
    values: set[str],
    model,
    *,
    attr: str = "name",
) -> dict[str, object]:
    mapping: dict[str, object] = {}
    values = {value for value in values if value}
    if not values:
        return mapping

    column_attr = getattr(model, attr)

    existing_stmt = select(model).where(column_attr.in_(values))
    for obj in session.scalars(existing_stmt):
        mapping[getattr(obj, attr)] = obj

    new_values = sorted(values - mapping.keys())
    for value in new_values:
        obj = model(**{attr: value})
        session.add(obj)
        mapping[value] = obj

    if new_values:
        session.commit()
    return mapping


def load_env() -> str:
    load_dotenv(override=True)
    db_uri = os.getenv("DB_URI")
    if not db_uri:
        raise RuntimeError("DB_URI no está definida en el entorno/.env")
    return db_uri


def assign_dimensions(session: Session, df: pd.DataFrame):
    type_map = create_dimension(session, unique_values(df["type"]), ContentType)
    rating_map = create_dimension(
        session, unique_values(df["rating"]), Rating, attr="code"
    )
    duration_type_map = create_dimension(
        session, unique_values(df["duration_type"]), DurationType
    )
    platform_map = create_dimension(
        session, unique_values(df["platform"]), Platform
    )
    director_map = create_dimension(
        session, unique_values(df["director"], split=True), Director
    )
    actor_map = create_dimension(
        session, unique_values(df["cast"], split=True), Actor
    )
    country_map = create_dimension(
        session, unique_values(df["country"], split=True), Country
    )
    category_map = create_dimension(
        session, unique_values(df["listed_in"], split=True), Category
    )

    return {
        "type": type_map,
        "rating": rating_map,
        "duration_type": duration_type_map,
        "platform": platform_map,
        "director": director_map,
        "actor": actor_map,
        "country": country_map,
        "category": category_map,
    }


def split_list(text) -> list[str]:
    if pd.isna(text):
        return []
    return [token for token in (normalize(p) for p in str(text).split(",")) if token]


def populate_movies(session: Session, df: pd.DataFrame, maps: dict[str, dict[str, object]]):
    inserted = 0
    for _, row in df.iterrows():
        show_code = normalize(row["show_id"])
        content_type_key = normalize(row["type"])
        if not show_code or not content_type_key:
            continue

        movie = Movie(
            show_code=show_code,
            title=normalize(row["title"]) or "Untitled",
            description=normalize(row["description"]),
            date_added=None
            if pd.isna(row["date_added"])
            else row["date_added"].date(),
            release_year=None
            if pd.isna(row["release_year"])
            else int(row["release_year"]),
            duration_int=None
            if pd.isna(row["duration_int"])
            else int(row["duration_int"]),
            content_type=maps["type"][content_type_key],
            rating=maps["rating"].get(normalize(row["rating"])),
            duration_type=maps["duration_type"].get(normalize(row["duration_type"])),
            platform=maps["platform"].get(normalize(row["platform"])),
        )

        movie.directors = [
            maps["director"][value]
            for value in split_list(row["director"])
            if value in maps["director"]
        ]
        movie.actors = [
            maps["actor"][value]
            for value in split_list(row["cast"])
            if value in maps["actor"]
        ]
        movie.countries = [
            maps["country"][value]
            for value in split_list(row["country"])
            if value in maps["country"]
        ]
        movie.categories = [
            maps["category"][value]
            for value in split_list(row["listed_in"])
            if value in maps["category"]
        ]

        session.add(movie)
        inserted += 1

    session.commit()
    print(f"Películas insertadas: {inserted}")


def main():
    db_uri = load_env()
    df = read_dataset()
    engine = create_engine(db_uri, future=True)
    with Session(engine) as session:
        maps = assign_dimensions(session, df)
        populate_movies(session, df, maps)
    print("Carga de datos finalizada.")


if __name__ == "__main__":
    main()
