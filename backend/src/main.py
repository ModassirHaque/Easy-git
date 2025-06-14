import os
import sys
# DON\'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models import db # Changed import path for db
from src.models.repository import Repository, FileChange, CommitHistory
from src.routes.user import user_bp
from src.routes.git_routes import git_bp
from src.routes.auth_routes import auth_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(git_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)




# from flask import Flask, send_from_directory
# import os

# # Get the absolute path to the directory where this script is located
# basedir = os.path.abspath(os.path.dirname(__file__))

# # Define the path to your frontend's dist directory
# # Adjusted path: go up two levels from 'src' to 'my-git-tool', then into 'dist'
# frontend_dist_folder = os.path.join(basedir, '..', '..', 'dist')

# app = Flask(__name__,
#             static_folder=frontend_dist_folder,
#             static_url_path='/')

# # ... (rest of your Flask application code remains the same)

# @app.route('/')
# def serve_index():
#     return send_from_directory(app.static_folder, 'index.html')

# @app.route('/<path:filename>')
# def serve_static(filename):
#     return send_from_directory(app.static_folder, filename)

# # Example API route (your existing backend routes)
# @app.route('/api/hello')
# def hello():
#     return {"message": "Hello from Flask backend!"}

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# import os
# from git import Repo, GitCommandError

# # Assuming your Flask app is in my-git-tool/backend/src/main.py
# # And your Git repository root is my-git-tool/
# REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# app = Flask(__name__)

# @app.route('/api/git/commit_and_push', methods=['POST'])
# def commit_and_push():
#     data = request.get_json()
#     file_paths = data.get('file_paths') # List of files to add, e.g., ['path/to/file1.txt', 'path/to/folder/file2.txt']
#     commit_message = data.get('commit_message')

#     if not file_paths or not commit_message:
#         return jsonify({'error': 'Missing file_paths or commit_message'}), 400

#     try:
#         repo = Repo(REPO_PATH)
#         git = repo.git

#         # Add files
#         for path in file_paths:
#             # Ensure the path is relative to the repository root
#             relative_path = os.path.relpath(os.path.join(REPO_PATH, path), REPO_PATH)
#             git.add(relative_path)

#         # Commit changes
#         git.commit('-m', commit_message)

#         # Push changes
#         # You might need to configure credentials for push, or use a token
#         # For simplicity, this assumes credentials are set up (e.g., via SSH agent or credential helper)
#         git.push()

#         return jsonify({'message': 'Files committed and pushed successfully!'}), 200

#     except GitCommandError as e:
#         return jsonify({'error': f'Git command failed: {e.stderr}'}), 500
#     except Exception as e:
#         return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

# # Example of how to initialize a repo if it's not already a git repo
# # This is for demonstration and might not be needed if your project is already a git repo
# @app.route('/api/git/init_repo', methods=['POST'])
# def init_repo():
#     try:
#         Repo.init(REPO_PATH)
#         return jsonify({'message': 'Repository initialized successfully!'}), 200
#     except Exception as e:
#         return jsonify({'error': f'Failed to initialize repository: {str(e)}'}), 500

# # ... (your existing Flask routes for serving frontend)

# if __name__ == '__main__':
#     # Ensure the repository exists and is initialized
#     if not os.path.exists(os.path.join(REPO_PATH, '.git')):
#         print(f"WARNING: {REPO_PATH} is not a Git repository. Please initialize it or clone one.")
#         # For development, you might want to uncomment the line below to auto-init
#         # Repo.init(REPO_PATH)

#     app.run(debug=True)
