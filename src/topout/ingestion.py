import logging
from time import sleep
import httpx
from datetime import datetime
from storage import Duck

logger = logging.getLogger(__name__)

base_url = "https://api3.problemator.fi/api/v03"
problem_endpoint = f"{base_url}/problem"


def find_head(db: Duck, endpoint: str, initial_key: int = 91507) -> int:
    """Find latest problem.
    While at it, store found.

    Args:
        db: Connection to duckdb instance
        endpoint: Base endpoint without / in the end
        initial_key: Key where head's tracing starts

    Returns:
        Latest problem's id if successfull or some milestone
        or initial_key if not.
    """

    key = initial_key
    keyd = []
    rate_left = 60
    status = 200
    head = None
    while not head:
        if rate_left < 2:
            # Trying to play nice and not getting limited
            sleep(20)

        response = httpx.get(f"{endpoint}/{key}")

        status = response.status_code
        rate_left = response.headers.get("X-Ratelimit-Remaining")

        match status:
            case 200:
                keyd.append(key)
                # Store to db
                val = response.json()
                db.store_problem(key, val["problem"])
                logger.debug(f"Stored: {key}")

                # Determine how long has it been since and where the head might be
                today = datetime.today()
                problem_added = datetime.strptime(
                    val["problem"]["added"], "%Y-%m-%d %H:%M:%S"
                )
                delta = (today - problem_added).days

                # Around 30 problems are created daily
                # If already on today's problems, just add 1
                key += delta * 30 + 1
            case 404:
                keyd.append(key)
                logger.debug(f"Not available: {key}")
                potential_head = keyd[-1] - 1
                # We are getting 404
                # and previous key has been successfully found
                # and next to that has been tried
                # -> head has been found
                if (
                    len(db.problems.filter(f"id = {potential_head}")) > 0
                    and potential_head + 1 in keyd
                ):
                    head = potential_head
                # Moving back one
                key -= 1
            case 429:
                logger.info(
                    f"""Status: {status} with problem {key} and headers {response.headers} 
                    waiting a bit and trying again"""
                )
                sleep(20)
            case _:
                logger.warning(
                    f"Status: {status} with problem {key} and headers {response.headers}"
                )

        if len(keyd) > 200:
            # Shouldn't take this long, abort with latest key
            max_id = db.problems.max("id").fetchone()
            if max_id:
                head = max_id[0]
            # Default to initial_key if nothing better available
            else:
                head = initial_key
    return head
