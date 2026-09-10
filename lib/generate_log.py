"""Create timestamped text files containing log entries."""

from datetime import datetime


def generate_log(entries):
    """Create today's log file and return its filename.

    Args:
        entries: A list of values to write, one value per line. An empty list
            creates an empty log file.

    Returns:
        The name of the created log file.

    Raises:
        ValueError: If ``entries`` is not a list.
    """
    if not isinstance(entries, list):
        raise ValueError("entries must be provided as a list")

    filename = f"log_{datetime.now():%Y%m%d}.txt"

    with open(filename, "w", encoding="utf-8") as log_file:
        for entry in entries:
            log_file.write(f"{entry}\n")

    print(f"Log file created: {filename}")
    return filename


if __name__ == "__main__":
    sample_entries = [
        "User logged in",
        "User updated profile",
        "Report exported",
    ]
    generate_log(sample_entries)
