from . import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_name = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    posture_type = db.Column(db.String(50), nullable=False)  # Enum-like: "sitting" or "standing"
    avg_good_posture = db.Column(db.Float, nullable=True)
    avg_bad_posture = db.Column(db.Float, nullable=True)
    session_posture_score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref='sessions')

    def __repr__(self):
        return f'<Session {self.session_name}>'
