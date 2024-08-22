from datetime import datetime
from app.config import db

class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    sort_in_list = db.Column(db.Integer, nullable=True)
    cover_proj = db.Column(db.String(256), nullable=False)

    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Section {self.title}>'

