from app import db
from datetime import datetime, timedelta, timezone
from flask_login import UserMixin

JST = timezone(timedelta(hours=9))

class Learning_info(UserMixin, db.Model):
    __tablename__ = 'lrecord'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    user_id = db.Column(db.String(255)) # システムで使う番号
    nowtime = db.Column(db.String(255))
    record = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=JST))  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=JST), onupdate=datetime.now)  # 更新日時