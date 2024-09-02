from datetime import datetime

from slugify import slugify
from sqlalchemy.orm import relationship

from app.config import db

class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    sort_in_list = db.Column(db.Integer, nullable=True)
    cover_proj = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), unique=True, nullable=True)

    section = relationship('Project', backref='sections')

    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f'<Section {self.title}>'

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    sort_in_list = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(255), nullable=False)
    cover_proj = db.Column(db.String(256), nullable=False)
    slug = db.Column(db.String(256), unique=True, nullable=True)

    section_id = db.Column(db.Integer, db.ForeignKey('sections.id', name='fk_section_project'))

    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f'<Project {self.title}>'


