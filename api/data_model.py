from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


class TaskInput(db.Model):  # type: ignore
    """
    Table task_input, containing one input for a task
    """

    __tablename__ = "task_input"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    kind = db.Column(db.String, nullable=False)
    value = db.Column(db.String)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)


class TaskInputSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for TaskInput to serialize/deserialize
    """

    class Meta:
        """Schema meta class"""

        model = TaskInput
        include_relationships = True
        load_instance = True
        include_fk = True


class TaskType(db.Model):  # type: ignore
    """
    Table task_type, representing a task type, ie.build, design, development...
    """

    __tablename__ = "task_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class TaskTypeSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for TaskType to serialize/deserialize
    """

    class Meta:
        """Schema meta class"""

        model = TaskType
        include_relationships = True
        load_instance = True
        include_fk = True


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

    task_type_id = db.Column(db.Integer, db.ForeignKey("task_type.id"), nullable=False)
    task_type = db.relationship(TaskType, lazy=True, foreign_keys="Task.task_type_id")

    inputs = db.relationship(TaskInput, backref="task_input", lazy=True)


class TaskSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for Task to serialize/deserialize
    Specify nested elements to show theme completely when deserializing, ot only their id
    """

    class Meta:
        """Schema meta class"""

        model = Task
        include_relationships = True
        load_instance = True
        include_fk = True

    subtasks = ma.Nested("TaskSchema", many=True)
    inputs = ma.Nested(TaskInputSchema, many=True)


class Model(db.Model):  # type: ignore
    """
    Table Model representing one possibility for a project with a tree of tasks
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    tasks = db.relationship(
        Task, backref="task", lazy=True, primaryjoin=id == Task.model_id
    )

    root_task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    root_task = db.relationship(
        Task, primaryjoin=root_task_id == Task.id, post_update=True
    )

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)


class ModelSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for Model to serialize/deserialize
    Nested tasks to show them when deserializing
    """

    class Meta:
        """Schema meta class"""

        model = Model
        include_relationships = True
        load_instance = True
        include_fk = True

    tasks = ma.Nested("TaskSchema", many=True)


class Project(db.Model):  # type: ignore
    """
    Table project which contains multiple models
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    models = db.relationship(
        Model, backref="model", lazy=True, primaryjoin=id == Model.project_id
    )
    base_model_id = db.Column(db.Integer, db.ForeignKey("model.id"))
    base_model = db.relationship(
        Model, primaryjoin=base_model_id == Model.id, post_update=True
    )


class ProjectSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for Project to serialize/deserialize
    Nested models to show them when deserializing
    """

    class Meta:
        """Schema meta class"""

        model = Project
        include_relationships = True
        load_instance = True
        include_fk = True

    models = ma.Nested("ModelSchema", many=True)
