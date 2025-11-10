import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from schemas.models import Base


def get_db_uri() -> str:
    load_dotenv(override=True)
    db_uri = os.getenv("DB_URI")
    if not db_uri:
        raise RuntimeError("DB_URI no está configurada en el entorno/.env")
    return db_uri


def create_tables(db_uri: str, *, drop_existing: bool = False) -> None:
    """Crea las tablas del esquema normalizado usando SQLAlchemy."""
    engine = create_engine(db_uri, future=True)
    if drop_existing:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Tablas creadas correctamente.")


def init_db() -> None:
    db_uri = get_db_uri()
    drop_existing = os.getenv("DROP_EXISTING", "false").lower() in {"1", "true", "yes"}
    create_tables(db_uri, drop_existing=drop_existing)


if __name__ == "__main__":
    init_db()
