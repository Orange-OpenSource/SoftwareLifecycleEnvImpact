from api.config import db, ma


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_relationships = True
        load_instance = True
