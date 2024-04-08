import os
from collections.abc import Generator
from typing import Any

import dlt
from dlt.sources.helpers import requests
from dotenv import load_dotenv


@dlt.resource(
    table_name="commits",
    write_disposition="merge",
    primary_key="id",
)
def get_commits() -> Generator[dict[str, Any], None, None]:
    github_token = os.environ.get("GITHUB_REPO_TOKEN")
    repository = "gdelepoulle/local-efficient-data-platform"

    # GitHub API URL for fetching commits from the specified repository
    url = f"https://api.github.com/repos/{repository}/commits"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        yield response.json()

        # Get next page
        if "next" not in response.links:
            break
        url = response.links["next"]["url"]


load_dotenv()
pipeline = dlt.pipeline(
    pipeline_name="github_commits_pipeline",
    destination="duckdb",
    dataset_name="github_commits",
)
load_info = pipeline.run(get_commits)
row_counts = pipeline.last_trace.last_normalize_info

print(row_counts)
print("------")
print(load_info)
