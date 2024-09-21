import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.common.utils import get_env_variable

def get_db_url():
    try:
        pg_user = get_env_variable("DB_USER")
        pg_password = get_env_variable("DB_PASSWORD")
        db_host = get_env_variable("DB_HOST")
        db_name = get_env_variable("DB_NAME")

        return f"postgresql+asyncpg://{pg_user}:{pg_password}@{db_host}/{db_name}"
    except Exception as e:
        logging.error(f"Error detting db creds. {e}")
        raise e

logging.info("Creating new async engine") 
engine = create_async_engine(get_db_url(), echo=True)

async def get_db():

    logging.info("Creating Session")
    async_session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

    logging.info("Creating new DB connection")
    async with async_session() as session:
        yield session

