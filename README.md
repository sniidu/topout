# TopOut

Looking for a bouldering gym to go to?
Don't know which one to choose?
Set some preferences and I'll propose gym for you!

## Disclaimer

Data is gathered from [Problemator](https://www.problemator.fi) according to [Terms Of Service](https://results.problemator.fi/terms_of_service.html)
Only public non-authenticated endpoints are used and rate-limiting will be implemented.

## Plan

- Features
  - Fetch, store and keep up-to-date problems from local gyms
  - Propose climbing gym based on location and preferences
- Tech
  - CLI app done in Python
    - click for args
    - Pydantic for db scheme
    - httpx for handling requests
  - duckdb for storage
  - YAML for config
  - uv for package management
  - pytest for testing
