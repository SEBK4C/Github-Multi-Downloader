#!/usr/bin/env python3
import os
import sys
import requests
import click
import subprocess
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import print as rprint
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.live import Live
from rich.layout import Layout

console = Console()

class GitHubDownloader:
    def __init__(self):
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Multi-Downloader"
        }

    def get_user_repos(self, username):
        """Fetch all public repositories for a given username."""
        url = f"{self.api_base}/users/{username}/repos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def download_repo(self, repo_url, target_dir):
        """Download a repository using git clone."""
        os.system(f"git clone {repo_url} {target_dir}")

    def update_gitignore(self, username):
        """Update .gitignore to exclude the downloaded repositories folder."""
        gitignore_path = ".gitignore"
        ignore_pattern = f"{username}/"
        
        # Read existing .gitignore content
        try:
            with open(gitignore_path, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            content = ""
        
        # Add the pattern if it's not already there
        if ignore_pattern not in content:
            with open(gitignore_path, 'a') as f:
                if content and not content.endswith('\n'):
                    f.write('\n')
                f.write(f"{ignore_pattern}\n")
            console.print(f"[green]Updated .gitignore to exclude {username}/ directory[/green]")

    def get_repo_status(self, repo_path):
        """Get the current branch and status of a repository."""
        try:
            # Get current branch
            branch = subprocess.check_output(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                cwd=repo_path,
                stderr=subprocess.PIPE,
                universal_newlines=True
            ).strip()

            # Get last commit hash
            commit = subprocess.check_output(
                ['git', 'rev-parse', '--short', 'HEAD'],
                cwd=repo_path,
                stderr=subprocess.PIPE,
                universal_newlines=True
            ).strip()

            # Get last commit date
            date = subprocess.check_output(
                ['git', 'log', '-1', '--format=%cd', '--date=short'],
                cwd=repo_path,
                stderr=subprocess.PIPE,
                universal_newlines=True
            ).strip()

            return {
                'branch': branch,
                'commit': commit,
                'date': date,
                'status': 'clean'
            }
        except subprocess.CalledProcessError:
            return None

    def update_repo(self, repo_path):
        """Update a repository using git pull."""
        try:
            # Check if there are uncommitted changes
            status = subprocess.check_output(
                ['git', 'status', '--porcelain'],
                cwd=repo_path,
                stderr=subprocess.PIPE,
                universal_newlines=True
            ).strip()

            if status:
                return False, "Repository has uncommitted changes"

            # Perform git pull
            result = subprocess.run(
                ['git', 'pull'],
                cwd=repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return True, "Successfully updated"
            else:
                return False, f"Update failed: {result.stderr}"
        except subprocess.CalledProcessError as e:
            return False, f"Error updating repository: {str(e)}"

    def display_repos_table(self, repos):
        """Display repositories in a formatted table."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Index", style="dim")
        table.add_column("Repository Name")
        table.add_column("Description")
        table.add_column("Stars", justify="right")
        
        for idx, repo in enumerate(repos, 1):
            table.add_row(
                str(idx),
                repo["name"],
                repo.get("description", "No description")[:100] + "..." if repo.get("description") else "No description",
                str(repo.get("stargazers_count", 0))
            )
        
        console.print(table)

    def display_status_table(self, repos_info):
        """Display repository status in a formatted table."""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Repository")
        table.add_column("Branch")
        table.add_column("Last Commit")
        table.add_column("Date")
        table.add_column("Status")
        
        for repo_name, info in repos_info.items():
            if info:
                status_color = "green" if info['status'] == 'clean' else "yellow"
                table.add_row(
                    repo_name,
                    info['branch'],
                    info['commit'],
                    info['date'],
                    f"[{status_color}]{info['status']}[/{status_color}]"
                )
            else:
                table.add_row(
                    repo_name,
                    "N/A",
                    "N/A",
                    "N/A",
                    "[red]Not a git repository[/red]"
                )
        
        console.print(table)

    def download_selected_repos(self, repos, selected_indices, base_dir):
        """Download selected repositories."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Downloading selected repositories...", total=len(selected_indices))
            for idx in selected_indices:
                repo = repos[idx - 1]  # Convert 1-based index to 0-based
                repo_name = repo["name"]
                repo_url = repo["clone_url"]
                target_dir = os.path.join(base_dir, repo_name)
                
                if not os.path.exists(target_dir):
                    self.download_repo(repo_url, target_dir)
                else:
                    console.print(f"[yellow]Repository {repo_name} already exists, skipping...[/yellow]")
                
                progress.update(task, advance=1)

    def download_all_repos(self, username):
        """Download all public repositories for a given username."""
        try:
            # Create base directory for the user's repos
            base_dir = os.path.join(os.getcwd(), username)
            os.makedirs(base_dir, exist_ok=True)

            # Get all repositories
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"Fetching repositories for {username}...", total=None)
                repos = self.get_user_repos(username)
                progress.update(task, completed=True)

            if not repos:
                console.print(f"[yellow]No public repositories found for user '{username}'[/yellow]")
                return

            # Display repositories table
            console.print("\n[bold]Available Repositories:[/bold]")
            self.display_repos_table(repos)

            # Ask user if they want to download all repositories
            if Confirm.ask("\nWould you like to download all repositories?"):
                selected_indices = list(range(1, len(repos) + 1))
            else:
                # Get repository selection from user
                console.print("\nEnter repository indices to download (comma-separated, e.g., '1,3,5')")
                selection = Prompt.ask("Selection")
                try:
                    selected_indices = [int(idx.strip()) for idx in selection.split(",")]
                    # Validate indices
                    if not all(1 <= idx <= len(repos) for idx in selected_indices):
                        raise ValueError("Invalid index")
                except (ValueError, TypeError):
                    console.print("[red]Invalid selection. Please enter valid comma-separated numbers.[/red]")
                    return

            # Update .gitignore before downloading
            self.update_gitignore(username)

            # Download selected repositories
            self.download_selected_repos(repos, selected_indices, base_dir)

            console.print(Panel(f"Successfully downloaded {len(selected_indices)} repositories to {base_dir}",
                              title="[green]Download Complete![/green]"))

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                console.print(f"[red]Error: User '{username}' not found[/red]")
            else:
                console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)

    def update_all_repos(self, username):
        """Update all repositories for a given username."""
        base_dir = os.path.join(os.getcwd(), username)
        
        if not os.path.exists(base_dir):
            console.print(f"[red]Error: No repositories found for user '{username}'[/red]")
            return

        # Get status of all repositories
        repos_info = {}
        for repo_name in os.listdir(base_dir):
            repo_path = os.path.join(base_dir, repo_name)
            if os.path.isdir(repo_path):
                repos_info[repo_name] = self.get_repo_status(repo_path)

        # Display current status
        console.print("\n[bold]Current Repository Status:[/bold]")
        self.display_status_table(repos_info)

        # Ask for confirmation
        if not Confirm.ask("\nWould you like to update all repositories?"):
            return

        # Update repositories
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Updating repositories...", total=len(repos_info))
            for repo_name, info in repos_info.items():
                if info:  # Only update if it's a valid git repository
                    repo_path = os.path.join(base_dir, repo_name)
                    success, message = self.update_repo(repo_path)
                    if not success:
                        console.print(f"[yellow]Warning: {repo_name}: {message}[/yellow]")
                progress.update(task, advance=1)

        # Display updated status
        console.print("\n[bold]Updated Repository Status:[/bold]")
        for repo_name in repos_info:
            repos_info[repo_name] = self.get_repo_status(os.path.join(base_dir, repo_name))
        self.display_status_table(repos_info)

@click.command()
@click.argument('username')
@click.option('--update', is_flag=True, help='Update all downloaded repositories')
def main(username, update):
    """Download or update repositories from a GitHub user."""
    downloader = GitHubDownloader()
    if update:
        downloader.update_all_repos(username)
    else:
        downloader.download_all_repos(username)

if __name__ == '__main__':
    main()