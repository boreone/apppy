from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(120))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    userrole = db.Column(db.Integer)
    addziduan = db.Column(db.String(10))
    addziduan1 = db.Column(db.String(10))

    def __repr__(self):
        return '%s' % self.id


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


tags = db.Table('tags',
                db.Column('id', db.Integer, primary_key=True),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('page_id', db.Integer, db.ForeignKey('page.id')))


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String(20))
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('pages', lazy='dynamic'))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    text = db.Column(db.String(120))


class Tagadd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    text = db.Column(db.String(120))

class Tagaddd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    text = db.Column(db.String(120))

class Tagadddd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    text = db.Column(db.String(120))
