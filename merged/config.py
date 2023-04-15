import os

from decouple import AutoConfig

# configures decouple to use settings.ini or .env file from another directory
if MERGED_PATH_TO_CONFIG := os.environ.get("MERGED_PATH_TO_CONFIG", None):
    config = AutoConfig(search_path=MERGED_PATH_TO_CONFIG)
else:
    config = AutoConfig(search_path=".")


# Github Config
GITHUB_DEFAULT_PAGE_SIZE = config("GITHUB_DEFAULT_PAGE_SIZE", cast=int, default=100)
GITHUB_ORG = config("GITHUB_ORG", cast=str)
GITHUB_REPOSITORY = config("GITHUB_REPOSITORY", cast=str)
GITHUB_BRANCH = config("GITHUB_BRANCH", cast=str, default="main")
GITHUB_TOKEN = config("GITHUB_TOKEN", cast=str)
GITHUB_URL = config("GITHUB_URL", cast=str, default="https://api.github.com")
GITHUB_USER = config("GITHUB_USER", cast=str)
DAYS_TO_REVIEW = config("DAYS_TO_REVIEW", cast=int, default=14)
