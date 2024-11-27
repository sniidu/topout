from pathlib import Path
import duckdb


class duck:
    def __init__(self, db: str | Path):
        """First time connection creates db"""
        self.con = duckdb.connect(database=db)
        self.initialize()

    def initialize(self, replace: bool = False):
        """Create tables if not exists or replace"""
        if replace:
            self.con.execute(
                "create or replace table problem (problem_id bigint primary key, val json)"
            )
        else:
            self.con.execute(
                "create table if not exists problem (problem_id bigint primary key, val json)"
            )
