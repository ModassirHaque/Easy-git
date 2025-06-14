from flask import Blueprint, jsonify, request
import requests
import base64
from urllib.parse import urlparse

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/github/validate-token', methods=['POST'])
def validate_github_token():
    """Validate a GitHub personal access token"""
    try:
        data = request.json
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token is required'}), 400
        
        # Test the token by making a request to GitHub API
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            return jsonify({
                'valid': True,
                'user': {
                    'login': user_data.get('login'),
                    'name': user_data.get('name'),
                    'email': user_data.get('email'),
                    'avatar_url': user_data.get('avatar_url')
                },
                'scopes': response.headers.get('X-OAuth-Scopes', '').split(', ') if response.headers.get('X-OAuth-Scopes') else []
            })
        else:
            return jsonify({
                'valid': False,
                'error': 'Invalid token or insufficient permissions'
            }), 401
            
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to validate token'}), 500

@auth_bp.route('/github/repositories', methods=['GET'])
def get_user_repositories():
    """Get user's GitHub repositories"""
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token required'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Get user's repositories
        response = requests.get('https://api.github.com/user/repos', headers=headers, params={
            'sort': 'updated',
            'per_page': 100
        })
        
        if response.status_code == 200:
            repos = response.json()
            formatted_repos = []
            
            for repo in repos:
                formatted_repos.append({
                    'id': repo['id'],
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                    'description': repo['description'],
                    'clone_url': repo['clone_url'],
                    'ssh_url': repo['ssh_url'],
                    'html_url': repo['html_url'],
                    'private': repo['private'],
                    'default_branch': repo['default_branch'],
                    'updated_at': repo['updated_at'],
                    'language': repo['language']
                })
            
            return jsonify({
                'repositories': formatted_repos,
                'total_count': len(formatted_repos)
            })
        else:
            return jsonify({'error': 'Failed to fetch repositories'}), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to get repositories'}), 500

@auth_bp.route('/github/repository/<path:repo_full_name>', methods=['GET'])
def get_repository_info(repo_full_name):
    """Get detailed information about a specific repository"""
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token required'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Get repository information
        response = requests.get(f'https://api.github.com/repos/{repo_full_name}', headers=headers)
        
        if response.status_code == 200:
            repo = response.json()
            
            # Get branches
            branches_response = requests.get(f'https://api.github.com/repos/{repo_full_name}/branches', headers=headers)
            branches = branches_response.json() if branches_response.status_code == 200 else []
            
            return jsonify({
                'repository': {
                    'id': repo['id'],
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                    'description': repo['description'],
                    'clone_url': repo['clone_url'],
                    'ssh_url': repo['ssh_url'],
                    'html_url': repo['html_url'],
                    'private': repo['private'],
                    'default_branch': repo['default_branch'],
                    'updated_at': repo['updated_at'],
                    'language': repo['language'],
                    'size': repo['size'],
                    'stargazers_count': repo['stargazers_count'],
                    'forks_count': repo['forks_count']
                },
                'branches': [{'name': branch['name'], 'protected': branch.get('protected', False)} for branch in branches]
            })
        else:
            return jsonify({'error': 'Repository not found or access denied'}), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to get repository information'}), 500

@auth_bp.route('/github/check-permissions', methods=['POST'])
def check_repository_permissions():
    """Check if the user has write permissions to a repository"""
    try:
        data = request.json
        token = data.get('token')
        repo_full_name = data.get('repository')
        
        if not token or not repo_full_name:
            return jsonify({'error': 'Token and repository name are required'}), 400
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Check repository permissions
        response = requests.get(f'https://api.github.com/repos/{repo_full_name}', headers=headers)
        
        if response.status_code == 200:
            repo_data = response.json()
            permissions = repo_data.get('permissions', {})
            
            return jsonify({
                'has_access': True,
                'permissions': {
                    'admin': permissions.get('admin', False),
                    'push': permissions.get('push', False),
                    'pull': permissions.get('pull', False)
                },
                'can_push': permissions.get('push', False) or permissions.get('admin', False)
            })
        else:
            return jsonify({
                'has_access': False,
                'error': 'Repository not found or access denied'
            }), response.status_code
            
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to check permissions'}), 500

