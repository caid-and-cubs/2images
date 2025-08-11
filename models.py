from app import db
from datetime import datetime
from sqlalchemy import DateTime, String, Text, Integer

class GeneratedImage(db.Model):
    id = db.Column(Integer, primary_key=True)
    prompt = db.Column(Text, nullable=False)
    model_name = db.Column(String(200), nullable=False)
    filename = db.Column(String(255), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    file_size = db.Column(Integer)  # in bytes
    
    def __repr__(self):
        return f'<GeneratedImage {self.id}: {self.prompt[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'prompt': self.prompt,
            'model_name': self.model_name,
            'filename': self.filename,
            'created_at': self.created_at.isoformat(),
            'file_size': self.file_size
        }
