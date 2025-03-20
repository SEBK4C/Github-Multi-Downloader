# GitHub Multi-Downloader

A command-line tool that allows you to download all public repositories from a GitHub user with an interactive selection interface.

## Prerequisites

This tool requires the UV Python package manager. To install UV:

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For more installation options, visit: https://github.com/astral-sh/uv#installation

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   ```
3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Usage

```bash
# Basic usage - saves repositories to ~/Downloads by default
python github_downloader.py <github_username>

# Update existing repositories
python github_downloader.py <github_username> --update

# Specify a custom save location
python github_downloader.py <github_username> --saveto /path/to/directory

# Combined options
python github_downloader.py <github_username> --update --saveto /path/to/directory
```

This will:
1. Fetch all public repositories from the specified GitHub username
2. Display a table showing:
   - Repository index
   - Repository name
   - Description
   - Star count
3. Prompt you to either:
   - Download all repositories
   - Select specific repositories by their index numbers (comma-separated, e.g., "1,3,5")

## Features

- Interactive repository selection interface
- Beautiful table display of available repositories
- Option to download all repositories or select specific ones
- Saves repositories to ~/Downloads by default (cross-platform compatible)
- Custom save location with --saveto flag
- Downloads repositories to an organized directory structure
- Shows progress with rich terminal output
- Handles rate limiting and errors gracefully
- Skips already downloaded repositories
- Shows repository descriptions and star counts
- Automatically adds downloaded repositories to .gitignore
- Keep repositories updated with the --update flag

## Directory Structure

When you run the script, it will:
1. By default, create a directory in ~/Downloads named after the GitHub username
2. Download all selected repositories into that directory
3. Automatically add the directory to .gitignore if the current directory is a git repository

Example structure:
```
~/Downloads/
└── example_user/           # Created automatically
    ├── repo1/
    ├── repo2/
    └── repo3/
```

Or with custom save location:
```
/path/to/directory/
└── example_user/           # Created automatically
    ├── repo1/
    ├── repo2/
    └── repo3/
```

## Example

```bash
$ python github_downloader.py example_user

Repositories will be saved to: /Users/username/Downloads

Available Repositories:
┌───────┬──────────────────┬──────────────────────────────┬───────┐
│ Index │ Repository Name  │ Description                  │ Stars │
├───────┼──────────────────┼──────────────────────────────┼───────┤
│ 1     │ project1         │ A sample project             │ 42    │
│ 2     │ project2         │ Another great project        │ 15    │
│ 3     │ project3         │ Yet another project          │ 8     │
└───────┴──────────────────┴──────────────────────────────┴───────┘

Would you like to download all repositories? [y/N]: n

Enter repository indices to download (comma-separated, e.g., '1,3,5')
Selection: 1,3
```

## Future Updates

The following features are planned for future updates:
- Support for private repositories (requires GitHub token)
- Repository filtering by language, stars, or last updated date
- Parallel downloads for faster repository cloning
- Repository metadata export (stars, forks, issues, etc.)