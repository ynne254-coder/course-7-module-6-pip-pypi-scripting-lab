"""Create timestamped log files and fetch a sample API record."""

from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import requests


DEFAULT_POST_URL = "https://jsonplaceholder.typicode.com/posts/1"


def generate_log(entries: list[Any], output_dir: str | Path = ".") -> str:
    """Write *entries* to today's timestamped log file.

    Args:
        entries: A list of values to write, one value per line.
        output_dir: Directory in which to create the log file.

    Returns:
        The path of the created log file as a string. For the default output
        directory this remains the historical filename (for example,
        ``log_20260910.txt``).

    Raises:
        ValueError: If ``entries`` is not a list.
    """
    if not isinstance(entries, list):
        raise ValueError("entries must be provided as a list")

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    filename = destination / f"log_{datetime.now():%Y%m%d}.txt"

    with filename.open("w", encoding="utf-8") as log_file:
        for entry in entries:
            log_file.write(f"{entry}\n")

    result = str(filename)
    print(f"Log file created: {result}")
    return result


def fetch_data(url: str = DEFAULT_POST_URL, timeout: float = 10) -> dict[str, Any]:
    """Fetch a JSON object from *url* using :mod:`requests`.

    Network failures, non-success responses, and non-object JSON responses
    are converted into an empty dictionary so the command-line workflow can
    still complete and create its local log file.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return {}

    return data if isinstance(data, dict) else {}


def main() -> None:
    """Fetch a sample post and write a local execution log."""
    post = fetch_data()
    title = post.get("title", "No title found")
    print("Fetched Post Title:", title)
    generate_log(
        [
            "User logged in",
            "User updated profile",
            "Report exported",
            f"Fetched post: {title}",
        ]
    )


if __name__ == "__main__":
    main()
