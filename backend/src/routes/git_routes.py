from flask import Blueprint, jsonify, request
from src.models.repository import Repository, FileChange, CommitHistory, db
from src.services.git_service import GitManager
from datetime import datetime
import os

git_bp = Blueprint('git', __name__)
git_manager = GitManager()

@git_bp.route('/repositories', methods=['GET'])
def get_repositories():
    """Get all repositories"""
    repositories = Repository.query.all()
    return jsonify([repo.to_dict() for repo in repositories])

@git_bp.route('/repositories', methods=['POST'])
def create_repository():
    """Clone a new repository from GitHub"""
    try:
        data = request.json
        github_url = data.get('github_url')
        repo_name = data.get('name')
        github_token = data.get('github_token')
        
        if not github_url or not repo_name:
            return jsonify({'error': 'GitHub URL and repository name are required'}), 400
        
        # Clone the repository
        result = git_manager.clone_repository(github_url, repo_name, github_token)
        
        if not result['success']:
            return jsonify({'error': result['error'], 'message': result['message']}), 400
        
        # Save repository to database
        repository = Repository(
            name=repo_name,
            github_url=github_url,
            local_path=result['local_path'],
            branch=result['branch'],
            status='active',
            last_sync=datetime.utcnow()
        )
        
        db.session.add(repository)
        db.session.commit()
        
        return jsonify({
            'message': 'Repository cloned successfully',
            'repository': repository.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to create repository'}), 500

@git_bp.route('/repositories/<int:repo_id>', methods=['GET'])
def get_repository(repo_id):
    """Get a specific repository"""
    repository = Repository.query.get_or_404(repo_id)
    return jsonify(repository.to_dict())

@git_bp.route('/repositories/<int:repo_id>/status', methods=['GET'])
def get_repository_status(repo_id):
    """Get the current Git status of a repository"""
    try:
        repository = Repository.query.get_or_404(repo_id)
        
        # Get Git status
        status_result = git_manager.get_repository_status(repository.local_path)
        
        if not status_result['success']:
            return jsonify({'error': status_result['error'], 'message': status_result['message']}), 400
        
        # Update pending changes in database
        _update_pending_changes(repository.id, status_result)
        
        return jsonify({
            'repository': repository.to_dict(),
            'git_status': status_result
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to get repository status'}), 500

@git_bp.route('/repositories/<int:repo_id>/upload', methods=['POST'])
def upload_files(repo_id):
    """Upload files to a repository"""
    try:
        repository = Repository.query.get_or_404(repo_id)
        
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        # Save uploaded files
        result = git_manager.save_uploaded_files(repository.local_path, files)
        
        if not result['success']:
            return jsonify({'error': result['error'], 'message': result['message']}), 400
        
        # Update repository status
        repository.last_sync = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Files uploaded successfully',
            'uploaded_files': result['saved_files']
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to upload files'}), 500

@git_bp.route('/repositories/<int:repo_id>/add', methods=['POST'])
def add_files(repo_id):
    """Add files to Git staging area"""
    try:
        repository = Repository.query.get_or_404(repo_id)
        data = request.json
        file_paths = data.get('file_paths')  # None means add all files
        
        # Add files to staging area
        result = git_manager.add_files(repository.local_path, file_paths)
        
        if not result['success']:
            return jsonify({'error': result['error'], 'message': result['message']}), 400
        
        return jsonify({
            'message': 'Files added to staging area',
            'added_files': result['added_files']
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to add files'}), 500

@git_bp.route('/repositories/<int:repo_id>/commit', methods=['POST'])
def commit_changes(repo_id):
    """Commit staged changes"""
    try:
        repository = Repository.query.get_or_404(repo_id)
        data = request.json
        message = data.get('message', 'Update files via GitEasy')
        author_name = data.get('author_name', 'GitEasy User')
        author_email = data.get('author_email', 'user@giteasy.com')
        
        # Commit changes
        result = git_manager.commit_changes(
            repository.local_path, 
            message, 
            author_name, 
            author_email
        )
        
        if not result['success']:
            return jsonify({'error': result['error'], 'message': result['message']}), 400
        
        # Save commit to database
        commit_history = CommitHistory(
            repository_id=repository.id,
            commit_hash=result['commit_hash'],
            message=message,
            author=result['author'],
            timestamp=datetime.fromisoformat(result['timestamp'])
        )
        
        db.session.add(commit_history)
        
        # Update repository status
        repository.last_sync = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Changes committed successfully',
            'commit': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to commit changes'}), 500

@git_bp.route('/repositories/<int:repo_id>/push', methods=['POST'])
def push_changes(repo_id):
    """Push committed changes to GitHub"""
    try:
        repository = Repository.query.get_or_404(repo_id)
        data = request.json
        github_token = data.get('github_token')
        branch = data.get('branch', repository.branch)
        
        # Push changes
        result = git_manager.push_changes(repository.local_path, github_token, branch)
        
        if not result['success']:
            return jsonify({'error': result['error'], 'message': result['message']}), 400
        
        # Update repository status
        repository.last_sync = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Changes pushed to GitHub successfully',
            'push_result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to push changes'}), 500

@git_bp.route('/repositories/<int:repo_id>/history', methods=['GET'])
def get_commit_history(repo_id):
    """Get commit history for a repository"""
    try:
        repository = Repository.query.get_or_404(repo_id)
        commits = CommitHistory.query.filter_by(repository_id=repo_id).order_by(CommitHistory.timestamp.desc()).all()
        
        return jsonify({
            'repository': repository.to_dict(),
            'commits': [commit.to_dict() for commit in commits]
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to get commit history'}), 500

@git_bp.route('/repositories/<int:repo_id>/changes', methods=['GET'])
def get_pending_changes(repo_id):
    """Get pending file changes for a repository"""
    try:
        repository = Repository.query.get_or_404(repo_id)
        changes = FileChange.query.filter_by(repository_id=repo_id, status='pending').all()
        
        return jsonify({
            'repository': repository.to_dict(),
            'pending_changes': [change.to_dict() for change in changes]
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to get pending changes'}), 500

def _update_pending_changes(repo_id, git_status):
    """Update pending changes in database based on Git status"""
    try:
        # Clear existing pending changes
        FileChange.query.filter_by(repository_id=repo_id, status='pending').delete()
        
        # Add modified files
        for file_path in git_status.get('modified_files', []):
            change = FileChange(
                repository_id=repo_id,
                file_path=file_path,
                change_type='modified',
                status='pending'
            )
            db.session.add(change)
        
        # Add untracked files
        for file_path in git_status.get('untracked_files', []):
            change = FileChange(
                repository_id=repo_id,
                file_path=file_path,
                change_type='added',
                status='pending'
            )
            db.session.add(change)
        
        db.session.commit()
        
    except Exception as e:
        print(f"Error updating pending changes: {e}")
        db.session.rollback()

