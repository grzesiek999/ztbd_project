import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = None
SessionLocal = None
Base = declarative_base()


def connect_to_postgres():
    global engine, SessionLocal
    engine = create_engine(os.getenv("POSTGRES_URI"))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("Connected to PostgreSQL database.")

    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error during table creation: {e}")
        raise


def close_postgres_connection():
    global engine
    if engine:
        engine.dispose()
        print("PostgreSQL connection closed.")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()