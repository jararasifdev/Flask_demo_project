from app.database import db

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('tags', lazy=True))
    __table_args__ = (db.UniqueConstraint('name', 'user_id', name='_tag_name_user_uc'),)
