from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import Enum

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author's name cannot be empty.")
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) !=10 or not phone_number.isdigit():
            raise ValueError('Phone number must be exactly ten digits.')
        return phone_number 

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String(250))
    category = db.Column(Enum('Fiction', 'Non-Fiction', name='post_category'), nullable=False)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('title')
    def validate_title(self, key, title):
        if not any(keyword in title for keyword in ['Won\'t Believe', 'Secret', 'Top', 'Guess']):
            raise ValueError("Title must contain a keyword")
        return title
    
    @validates('content')
    def validate_content(self, key, content):
        if len(content) <250:
            raise ValueError('Content too short test. Less than 250 chars.')
        return content    
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and  len(summary)>250:
            raise ValueError('The summary is too long, should not exceed 250 characters')
        return summary
        
    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
