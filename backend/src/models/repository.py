from src.models.user import db
from datetime import datetime
import os

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    github_url = db.Column(db.String(500), nullable=False)
    local_path = db.Column(db.String(500), nullable=False)
    branch = db.Column(db.String(100), default='main')
    status = db.Column(db.String(50), default='active')
    last_sync = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'github_url': self.github_url,
            'local_path': self.local_path,
            'branch': self.branch,
            'status': self.status,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class FileChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    change_type = db.Column(db.String(20), nullable=False)  # added, modified, deleted
    status = db.Column(db.String(20), default='pending')  # pending, committed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    repository = db.relationship('Repository', backref=db.backref('file_changes', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'repository_id': self.repository_id,
            'file_path': self.file_path,
            'change_type': self.change_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class CommitHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repository_id = db.Column(db.Integer, db.ForeignKey('repository.id'), nullable=False)
    commit_hash = db.Column(db.String(40), nullable=False)
    message = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    repository = db.relationship('Repository', backref=db.backref('commits', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'repository_id': self.repository_id,
            'commit_hash': self.commit_hash,
            'message': self.message,
            'author': self.author,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

