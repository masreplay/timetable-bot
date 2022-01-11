import logging

from app.db.db import get_db
from app.db.init_db import InitializeDatabaseWithASC
# TODO: Call it inside do.py
from asc_scrapper.crud import AscCRUD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with next(get_db()) as session:

        InitializeDatabaseWithASC(
            db=session, asc_crud=AscCRUD.from_file(file_name="../../asc_scrapper/asc_schedule.json")
        )


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
