from config import db, ma


class TaskInput(db.Model):
    __tablename__ = "task_input"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    kind = db.Column(db.String, nullable=False)
    value = db.Column(db.String)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)


class TaskInputSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskInput
        include_relationships = True
        load_instance = True
        include_fk = True


class TaskType(db.Model):
    __tablename__ = "task_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class TaskTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskType
        include_relationships = True
        load_instance = True
        include_fk = True


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey("model.id"), nullable=False)

    parent_task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    subtasks = db.relationship("Task", lazy=True)

    task_type_id = db.Column(db.Integer, db.ForeignKey("task_type.id"), nullable=False)
    task_type = db.relationship(TaskType, lazy=True, foreign_keys="Task.task_type_id")

    inputs = db.relationship(TaskInput, backref="task_input", lazy=True)


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True
        include_fk = True

    subtasks = ma.Nested("TaskSchema", many=True)
    inputs = ma.Nested(TaskInputSchema, many=True)


class Model(db.Model):
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


class ModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model
        include_relationships = True
        load_instance = True
        include_fk = True

    tasks = ma.Nested("TaskSchema", many=True)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    models = db.relationship(
        Model, backref="model", lazy=True, primaryjoin=id == Model.project_id
    )
    base_model_id = db.Column(db.Integer, db.ForeignKey("model.id"))
    base_model = db.relationship(
        Model, primaryjoin=base_model_id == Model.id, post_update=True
    )


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_relationships = True
        load_instance = True
        include_fk = True

    models = ma.Nested("ModelSchema", many=True)
