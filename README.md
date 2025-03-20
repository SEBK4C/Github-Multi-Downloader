# GitHub Multi-Downloader

A command-line tool that allows you to download all public repositories from a GitHub user with an interactive selection interface.

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
python github_downloader.py <github_username>
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
- Downloads repositories to an organized directory structure
- Shows progress with rich terminal output
- Handles rate limiting and errors gracefully
- Skips already downloaded repositories
- Shows repository descriptions and star counts

## Example

```bash
$ python github_downloader.py example_user

Available Repositories:
┌───────┬──────────────────┬──────────────────────────────┬───────┐
│ Index │ Repository Name  │ Description                   │ Stars │
├───────┼──────────────────┼──────────────────────────────┼───────┤
│ 1     │ project1        │ A sample project              │ 42    │
│ 2     │ project2        │ Another great project         │ 15    │
│ 3     │ project3        │ Yet another project           │ 8     │
└───────┴──────────────────┴──────────────────────────────┴───────┘

Would you like to download all repositories? [y/N]: n

Enter repository indices to download (comma-separated, e.g., '1,3,5')
Selection: 1,3 