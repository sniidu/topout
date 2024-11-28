import logging
import duckdb

logger = logging.getLogger(__name__)


class Duck:
    """For longevity, storing problems to local duckdb"""

    def __init__(self):
        self.connect()
        self.initialize_db(replace=True)
        # Create relation to table and it's data
        self.problems = self.con.sql("select id, struct from problem")

    def connect(self) -> None:
        """First time connection creates db"""
        # duck.db will to be relative to this file
        self.con = duckdb.connect(database="../../duck.db")
        logger.info("Created/Connected to db")

    def initialize_db(self, replace: bool = False):
        """Create tables if not exists or replace"""
        if replace:
            self.con.execute(
                "create or replace table problem (id bigint primary key, struct json)"
            )
            logger.info("Replaced problem-table")
        else:
            self.con.execute(
                "create table if not exists problem (id bigint primary key, struct json)"
            )
            logger.info("Maybe created problem-table")

    def store(self, key: int, val: dict):
        """Store problem to db"""
        self.con.execute("insert into problem values (?, ?)", [key, val])
