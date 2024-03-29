import asyncio

from loguru import logger

from app.db.init_db import init_db
from app.db.session import async_session


async def init() -> None:
    async with async_session() as session:
        await init_db(session)
    await session.commit()


def main() -> None:
    logger.info("Creating initial data")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    loop.close()

    logger.info("Initial data created")


if __name__ == "__main__":
    main()
