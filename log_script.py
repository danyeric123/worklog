import os
from datetime import datetime, date
import subprocess
import click
import yaml
from pathlib import Path
import sys

CONFIG_FILE = "worklog_config.yaml"
DEFAULT_CONFIG = {
    "categories": [
        "Projects",
        "Code Changes",
        "Code Reviews",
        "Design Documents",
        "Meetings & Discussions",
        "Helping Others",
        "Other Tasks",
    ],
    "backup_dir": "~/.worklog_backup",
    "git_auto_commit": False,
}


class WorkLogError(Exception):
    """Custom exception for work log errors."""

    pass


def load_config():
    """Load configuration from YAML file."""
    config_path = Path(get_git_root()) / CONFIG_FILE
    if not config_path.exists():
        return DEFAULT_CONFIG

    with open(config_path) as f:
        return {**DEFAULT_CONFIG, **yaml.safe_load(f)}


def get_git_root():
    """Get the root directory of the git repository."""
    try:
        git_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL
        )
        return git_root.decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return os.getcwd()


def create_log_directory():
    """Create the logs directory if it doesn't exist."""
    git_root = get_git_root()
    log_dir = os.path.join(git_root, "work_logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def get_log_file_path():
    """Generate the log file path for the current month."""
    now = datetime.now()
    log_dir = create_log_directory()
    return os.path.join(log_dir, f"{now.strftime('%Y_%m')}.md")


def create_daily_entry():
    """Create a new daily entry in the monthly log file."""
    now = datetime.now()
    date_header = f"## {now.strftime('%Y-%m-%d')}"

    categories = [
        "Projects",
        "Code Changes",
        "Code Reviews",
        "Design Documents",
        "Meetings & Discussions",
        "Helping Others",
        "Other Tasks",
    ]

    click.echo("\nDaily Work Log Entry")
    click.echo("===================")

    entries = {}
    for category in categories:
        click.echo(f"\n{category}:")
        click.echo(
            "(Enter multiple items, one per line. Press Enter twice to move to next category)"
        )

        items = []
        while True:
            item = click.prompt(">", type=str, default="", show_default=False).strip()
            if not item:
                if not items:  # If no items were entered
                    break
                if items and not items[-1]:  # If last item was empty
                    items.pop()  # Remove the empty item
                    break
                items.append(item)
            else:
                items.append(item)

        if items:
            entries[category] = items

    # Format the entry
    entry_text = f"\n{date_header}\n\n"
    for category, items in entries.items():
        if items:
            entry_text += f"### {category}\n"
            for item in items:
                entry_text += f"* {item}\n"
            entry_text += "\n"

    return entry_text


def update_log_file(entry):
    """Update the monthly log file with the new entry."""
    file_path = get_log_file_path()

    # Create file with header if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            month_year = datetime.now().strftime("%B %Y")
            f.write(f"# Work Log - {month_year}\n")

    # Append the new entry
    with open(file_path, "a") as f:
        f.write(entry)

    return file_path


def commit_to_git(file_path):
    """Commit the changes to git."""
    try:
        subprocess.run(["git", "add", file_path], check=True)
        commit_message = f"Update work log for {datetime.now().strftime('%Y-%m-%d')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        click.echo("Changes committed to git successfully!")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error committing to git: {e}", err=True)


@click.group()
def cli():
    """Work Log CLI - Create and manage daily work logs."""
    pass


@cli.command()
@click.option(
    "--git/--no-git", default=None, help="Automatically commit changes to git"
)
@click.option(
    "--date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="Override date (YYYY-MM-DD)",
)
def log(git, date):
    """Create a new work log entry."""
    config = load_config()
    git = git if git is not None else config["git_auto_commit"]

    try:
        click.echo("Creating new work log entry...")
        entry = create_daily_entry(date)
        file_path = update_log_file(entry)

        click.echo(f"\nWork log updated successfully!")
        click.echo(f"File location: {file_path}")

        if git:
            commit_to_git(file_path)
    except WorkLogError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--month",
    type=click.DateTime(formats=["%Y-%m"]),
    help="View logs for specific month (YYYY-MM)",
)
def view(month):
    """View work log entries."""
    try:
        file_path = (
            get_log_file_path()
            if not month
            else os.path.join(create_log_directory(), f"{month.strftime('%Y_%m')}.md")
        )

        if not os.path.exists(file_path):
            raise WorkLogError("No logs found for specified period")

        with open(file_path) as f:
            click.echo(f.read())
    except WorkLogError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def init():
    """Initialize work log configuration."""
    config_path = Path(get_git_root()) / CONFIG_FILE
    if config_path.exists():
        if not click.confirm("Configuration file exists. Overwrite?"):
            return

    with open(config_path, "w") as f:
        yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False)
    click.echo(f"Configuration file created at {config_path}")


if __name__ == "__main__":
    cli()
