import logging
import json
import duckdb
from pydantic import ValidationError
from models import Problem

logger = logging.getLogger(__name__)


class Duck:
    """For longevity, storing problems to local duckdb"""

    def __init__(self) -> None:
        self.connect()
        self.initialize_db(replace=True)
        # Create relation to table and it's data
        self.problems = self.con.sql("select id, struct from problem")

    def connect(self) -> None:
        """First time connection creates db"""
        # duck.db will to be relative to this file
        self.con = duckdb.connect(database="../../duck.db")
        logger.info("Created/Connected to db")

    def initialize_db(self, replace: bool = False) -> None:
        """Create tables required by app.

        Args:
            replace: Should tables be recreated? Used for debugging
        """
        if replace:
            self.con.execute(
                "create or replace table problem (id bigint primary key, struct json)"
            )
            logger.info("Replaced problem-table")
        else:
            self.con.execute(
                "create table if not exists problem (id bigint primary key, struct json)"
            )
            logger.info("Created problem-table if not existed")

    def store_problem(self, key: int, val: dict) -> None:
        """Store problem to duckdb.
        Validate first to contain the most important fields.
        Insert if new key, update if exists already.

        Args:
            key: Primary key of record
            val: JSON with information of key
        """
        try:
            Problem.model_validate_json(json.dumps(val))
        except ValidationError as e:
            logger.warning(f"Won't store problem {key} due to validation error:\n{e}")
            return
        self.con.execute("insert or replace into problem values (?, ?)", [key, val])
        logger.debug(f"Inserted {key} to db")
