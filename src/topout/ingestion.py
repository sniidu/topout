import logging
import httpx
from datetime import datetime
from storage import Duck

logger = logging.getLogger(__name__)

base_url = "https://api3.problemator.fi/api/v03"
problem_endpoint = f"{base_url}/problem"


def initial_loader(db: Duck, endpoint: str, initial_key: int = 91507):
    """Nothing in db - load like there's no tomorrow"""
    key = initial_key
    # Store all keys tried in session
    keyd = []
    rate_left = 60
    status = 200
    while rate_left > 1:
        response = httpx.get(f"{endpoint}/{key}")
        keyd.append(key)

        status = response.status_code
        rate_left = response.headers.get("X-Ratelimit-Remaining")

        if status == 200:
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
        else:
            logger.warning(
                f"Status: {status} with problem {key} and headers {response.headers}"
            )
            # Moving to in-between last and one before that
