from apps import db

class ThreeWords(db.Model):
    __tablename__ = 'threewords'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grant_id  = db.Column(db.String(256))
    message_id = db.Column(db.String(256))
    three_words =  db.Column(db.String(256))

    def __init__(self,grant_id,message_id, three_words):
        self.grant_id = grant_id
        self.message_id = message_id
        self.three_words = three_words

    def __repr__(self):
        return self.three_words