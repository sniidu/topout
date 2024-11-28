import logging
import httpx
from storage import Duck

logger = logging.getLogger(__name__)

base_url = "https://api3.problemator.fi/api/v03"
problem_endpoint = f"{base_url}/problem"


def fetch(db: Duck, endpoint: str, key: int):
    response = httpx.get(f"{endpoint}/{key}")

    status = response.status_code
    val = response.json()
    rate_left = response.headers.get("X-Ratelimit-Remaining")

    if status == 200:
        db.store(key, val["problem"])
        logger.debug(f"Stored: {key}")
    else:
        logger.warning(f"Status: {status} with problem {key}")
        logger.warning(f"Headers: {response.headers.get}")

    return (status, rate_left)


def initial_loader(db: Duck, endpoint: str, initial_key: int):
    """Nothing in db - load like there's no tomorrow"""
    key = initial_key
    rate_left = 60
    status = 200
    while rate_left > 1:
        status, rate_left = fetch(db, endpoint, key)
