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
- Automatically adds downloaded repositories to .gitignore
- Keeps all downloaded repositories within the script's directory

## Directory Structure

When you run the script, it will:
1. Create a directory named after the GitHub username in the same directory as the script
2. Download all selected repositories into that directory
3. Automatically add the username directory to .gitignore to prevent git from tracking the downloaded repositories

Example structure:
```
github-multi-downloader/
├── github_downloader.py
├── requirements.txt
├── README.md
└── .gitignore
└── example_user/           # Created automatically
    ├── repo1/
    ├── repo2/
    └── repo3/
```

## Example

```bash
$ python github_downloader.py example_user

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
- `--update` flag to update all downloaded repositories using `git pull`
- Support for private repositories (requires GitHub token)
- Repository filtering by language, stars, or last updated date
- Parallel downloads for faster repository cloning
- Repository metadata export (stars, forks, issues, etc.)