from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import func

db = SQLAlchemy()
ma = Marshmallow()


class Resource(db.Model):  # type: ignore
    __tablename__ = "resource"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)

    type = db.Column(db.String, nullable=False)
    value = db.Column(db.Integer)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class ResourceSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    class Meta(ma.SQLAlchemyAutoSchema.Meta):  # type: ignore
        model = Resource
        include_relationships = True
        load_instance = True
        include_fk = True
        sqla_session = db.session


class Task(db.Model):  # type: ignore
    """
    Table task representing one project phase
    """

    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    model_id = db.Column(db.Integer, db.ForeignKey("model.id"), nullable=False)

    parent_task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    subtasks = db.relationship("Task", lazy=True)

    resources = db.relationship(
        Resource, backref="task_input", lazy=True, cascade="all"
    )

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class TaskSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for Task to serialize/deserialize
    Specify nested elements to show theme completely when deserializing, ot only their id
    """

    class Meta(ma.SQLAlchemyAutoSchema.Meta):  # type: ignore
        """Schema meta class"""

        model = Task
        include_relationships = True
        load_instance = True
        include_fk = True
        sqla_session = db.session

    subtasks = Nested("TaskSchema", many=True)
    resources = Nested(ResourceSchema, many=True)


class Model(db.Model):  # type: ignore
    """
    Table Model representing one possibility for a project with a tree of tasks
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    tasks = db.relationship(
        Task, backref="task", lazy=True, primaryjoin=id == Task.model_id, cascade="all"
    )

    root_task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    root_task = db.relationship(
        Task, primaryjoin=root_task_id == Task.id, post_update=True, cascade="all"
    )

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class ModelSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for Model to serialize/deserialize
    Nested tasks to show them when deserializing
    """

    class Meta(ma.SQLAlchemyAutoSchema.Meta):  # type: ignore
        """Schema meta class"""

        model = Model
        include_relationships = True
        load_instance = True
        include_fk = True
        sqla_session = db.session

    tasks = Nested("TaskSchema", many=True)


class Project(db.Model):  # type: ignore
    """
    Table project which contains multiple models
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    models = db.relationship(
        Model,
        backref="model",
        lazy=True,
        primaryjoin=id == Model.project_id,
        cascade="all",
    )
    base_model_id = db.Column(db.Integer, db.ForeignKey("model.id"))
    base_model = db.relationship(
        Model, primaryjoin=base_model_id == Model.id, post_update=True, cascade="all"
    )

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())


class ProjectSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for Project to serialize/deserialize
    Nested models to show them when deserializing
    """

    class Meta(ma.SQLAlchemyAutoSchema.Meta):  # type: ignore
        """Schema meta class"""

        model = Project
        include_relationships = True
        load_instance = True
        include_fk = True
        sqla_session = db.session

    models = Nested("ModelSchema", many=True)
