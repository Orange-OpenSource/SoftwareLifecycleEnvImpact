from config import db, ma

class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)


class ModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model
        include_relationships = True
        load_instance = True

    id = ma.auto_field()
    name = ma.auto_field()
    project_id = ma.auto_field()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    models = db.relationship('Model', backref='model', lazy=True)


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_relationships = True
        load_instance = True


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
