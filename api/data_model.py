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


class TaskType(db.Model):
    __tablename__ = "task_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class TaskTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskType
        include_relationships = True
        load_instance = True


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    parent_task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    task_type_id = db.Column(db.Integer, db.ForeignKey("task_type.id"), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey("model.id"), nullable=False)
    subtasks = db.relationship("Task", lazy=True)
    inputs = db.relationship("TaskInput", backref="task_input", lazy=True)


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True

    subtasks = ma.Nested("TaskSchema", many=True)
    inputs = ma.Nested("TaskInputSchema", many=True)


class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    root_task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)


class ModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Model
        include_relationships = True
        load_instance = True

    tasks = ma.Nested("TaskSchema", many=True)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    models = db.relationship("Model", backref="model", lazy=True)


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_relationships = True
        load_instance = True

    models = ma.Nested("ModelSchema", many=True)
