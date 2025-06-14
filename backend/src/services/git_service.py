import os
import shutil
from git import Repo, GitCommandError
from git.exc import InvalidGitRepositoryError
from datetime import datetime
import requests
from urllib.parse import urlparse

class GitManager:
    def __init__(self, base_repos_dir="/tmp/giteasy_repos"):
        self.base_repos_dir = base_repos_dir
        os.makedirs(base_repos_dir, exist_ok=True)
    
    def clone_repository(self, github_url, repo_name, github_token=None):
        """Clone a GitHub repository to local storage"""
        try:
            local_path = os.path.join(self.base_repos_dir, repo_name)
            
            # Remove existing directory if it exists
            if os.path.exists(local_path):
                shutil.rmtree(local_path)
            
            # Prepare URL with token if provided
            if github_token:
                parsed_url = urlparse(github_url)
                auth_url = f"https://{github_token}@{parsed_url.netloc}{parsed_url.path}"
            else:
                auth_url = github_url
            
            # Clone the repository
            repo = Repo.clone_from(auth_url, local_path)
            return {
                'success': True,
                'local_path': local_path,
                'branch': repo.active_branch.name,
                'message': f'Repository {repo_name} cloned successfully'
            }
        except GitCommandError as e:
            return {
                'success': False,
                'error': f'Git error: {str(e)}',
                'message': 'Failed to clone repository'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Unexpected error during cloning'
            }
    
    def get_repository_status(self, local_path):
        """Get the current status of a Git repository"""
        try:
            repo = Repo(local_path)
            
            # Get modified files
            modified_files = [item.a_path for item in repo.index.diff(None)]
            
            # Get untracked files
            untracked_files = repo.untracked_files
            
            # Get staged files
            staged_files = [item.a_path for item in repo.index.diff("HEAD")]
            
            return {
                'success': True,
                'branch': repo.active_branch.name,
                'modified_files': modified_files,
                'untracked_files': list(untracked_files),
                'staged_files': staged_files,
                'is_dirty': repo.is_dirty(),
                'ahead_behind': self._get_ahead_behind_count(repo)
            }
        except InvalidGitRepositoryError:
            return {
                'success': False,
                'error': 'Invalid Git repository',
                'message': 'The specified path is not a valid Git repository'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to get repository status'
            }
    
    def add_files(self, local_path, file_paths=None):
        """Add files to the Git staging area"""
        try:
            repo = Repo(local_path)
            
            if file_paths is None:
                # Add all files
                repo.git.add(A=True)
                added_files = "all files"
            else:
                # Add specific files
                for file_path in file_paths:
                    repo.git.add(file_path)
                added_files = file_paths
            
            return {
                'success': True,
                'added_files': added_files,
                'message': 'Files added to staging area successfully'
            }
        except GitCommandError as e:
            return {
                'success': False,
                'error': f'Git error: {str(e)}',
                'message': 'Failed to add files'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Unexpected error while adding files'
            }
    
    def commit_changes(self, local_path, message, author_name="GitEasy User", author_email="user@giteasy.com"):
        """Commit staged changes"""
        try:
            repo = Repo(local_path)
            
            # Check if there are staged changes
            if not repo.index.diff("HEAD"):
                return {
                    'success': False,
                    'error': 'No staged changes to commit',
                    'message': 'Please stage some changes before committing'
                }
            
            # Configure user if not set
            try:
                repo.config_reader().get_value("user", "name")
            except:
                repo.config_writer().set_value("user", "name", author_name).release()
                repo.config_writer().set_value("user", "email", author_email).release()
            
            # Commit changes
            commit = repo.index.commit(message)
            
            return {
                'success': True,
                'commit_hash': commit.hexsha,
                'message': message,
                'author': f"{author_name} <{author_email}>",
                'timestamp': datetime.fromtimestamp(commit.committed_date).isoformat()
            }
        except GitCommandError as e:
            return {
                'success': False,
                'error': f'Git error: {str(e)}',
                'message': 'Failed to commit changes'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Unexpected error during commit'
            }
    
    def push_changes(self, local_path, github_token=None, branch='main'):
        """Push committed changes to GitHub"""
        try:
            repo = Repo(local_path)
            
            # Check if there are commits to push
            try:
                commits_ahead = list(repo.iter_commits(f'origin/{branch}..{branch}'))
                if not commits_ahead:
                    return {
                        'success': False,
                        'error': 'No commits to push',
                        'message': 'Repository is up to date with remote'
                    }
            except:
                # If we can't check, proceed with push anyway
                pass
            
            # Push changes
            if github_token:
                # Update remote URL with token
                origin = repo.remote('origin')
                original_url = origin.url
                parsed_url = urlparse(original_url)
                auth_url = f"https://{github_token}@{parsed_url.netloc}{parsed_url.path}"
                origin.set_url(auth_url)
            
            origin = repo.remote('origin')
            push_info = origin.push(branch)
            
            return {
                'success': True,
                'pushed_commits': len(commits_ahead) if 'commits_ahead' in locals() else 'unknown',
                'message': 'Changes pushed to GitHub successfully'
            }
        except GitCommandError as e:
            return {
                'success': False,
                'error': f'Git error: {str(e)}',
                'message': 'Failed to push changes to GitHub'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Unexpected error during push'
            }
    
    def _get_ahead_behind_count(self, repo):
        """Get how many commits ahead/behind the local branch is"""
        try:
            branch = repo.active_branch
            remote_branch = f'origin/{branch.name}'
            
            ahead = list(repo.iter_commits(f'{remote_branch}..{branch.name}'))
            behind = list(repo.iter_commits(f'{branch.name}..{remote_branch}'))
            
            return {
                'ahead': len(ahead),
                'behind': len(behind)
            }
        except:
            return {'ahead': 0, 'behind': 0}
    
    def save_uploaded_files(self, local_path, files):
        """Save uploaded files to the repository directory"""
        try:
            saved_files = []
            
            for file in files:
                file_path = os.path.join(local_path, file.filename)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Save the file
                file.save(file_path)
                saved_files.append(file.filename)
            
            return {
                'success': True,
                'saved_files': saved_files,
                'message': f'Successfully saved {len(saved_files)} files'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to save uploaded files'
            }

