from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        index=True,
        primary_key=True
    )
    slack_id = db.Column(
        db.String(12),
        index=True,
        nullable=False
    )
    username = db.Column(
        db.String(54),
        nullable=False
    )
    name = db.Column(
        db.String(54),
        nullable=False
    )
    real_name = db.Column(
        db.String(54),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)
