import logging

from app.db.db import get_db
from app.db.init_db import InitializeDatabase

# TODO: Call it inside do.py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with next(get_db()) as session:
        InitializeDatabase(db=session, asc_crud)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
