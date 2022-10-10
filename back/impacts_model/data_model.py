from typing import Any, List
from flask_marshmallow import Marshmallow as FlaskMarshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy.fields import Nested
from pint import Quantity
from sqlalchemy import func

from impacts_model.impacts import (
    AggregatedImpact,
    AggregatedImpactByResource,
    ImpactIndicator,
)
from impacts_model.templates import ResourceTemplate

db = SQLAlchemy()
ma = FlaskMarshmallow()


class ResourceInput(db.Model):  # type: ignore
    __tablename__ = "resource_input"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    resource_id = db.Column(db.Integer, db.ForeignKey("resource.id"), nullable=False)
    resource = db.relationship("Resource", back_populates="input")

    type = db.Column(db.String, nullable=False)
    input = db.Column(db.Integer, default=0)
    days = db.Column(db.Integer, default=0)
    months = db.Column(db.Integer, default=0)
    years = db.Column(db.Integer, default=0)

    value = (
        db.Column(
            db.Integer, db.Computed("input * days * (months * 31) * (years * 365)")
        ),
    )

    def copy(self) -> Any:
        return ResourceInput(
            time_input=self.time_input.copy(),
            type=self.type,
            hours=self.hours,
            days=self.days,
            months=self.months,
            years=self.years,
            value=self.value,
        )


class Resource(db.Model):  # type: ignore # TODO resource should have a unit
    """
    Resource object and table with a name, a type and a value. Only for a task
    The type represents the name of the ResourceTemplate to retrieve model values for computation
    """

    __tablename__ = "resource"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    input = db.relationship(
        ResourceInput,
        back_populates="resource",
        lazy=True,
        cascade="all",
        uselist=False,
    )

    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def copy(self) -> Any:
        return Resource(
            name=self.name,
            type=self.type,
            input=self.input.copy(),
        )

    def get_environmental_impact(self) -> AggregatedImpact:
        """
        Get a resource complete environmental impact as an EnvironementalImapct object
        :return: an AggregatedImpact object with all resource impacts
        """
        resource_template = ResourceTemplate(self.type)
        environmental_impact = AggregatedImpact()

        for impact_source in resource_template.impact_sources:
            for key in impact_source.environmental_impact.impacts:
                environmental_impact.merge_impact(
                    key,
                    impact_source.environmental_impact.impacts[key] * self.input.value,
                )

        return environmental_impact

    def get_indicator_impact(self, impact_indicator: ImpactIndicator) -> Quantity[Any]:
        """
        Compute and return a resource environmental impact for an ImpactIndicator
        :param resource: the Resource object to view to impact from
        :param impact_indicator: The ImpactIndicator to retrieve the impact
        :return: A quantity corresponding to the resource ImpactIndicator quantity
        """
        resource_template = ResourceTemplate(self.type)

        impacts: List[Quantity[Any]] = [
            i.environmental_impact.impacts[impact_indicator] * self.input.value
            for i in resource_template.impact_sources
        ]

        return sum(impacts)


class ResourceSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Resource schema to serialize a Resource object
    """

    class Meta(ma.SQLAlchemyAutoSchema.Meta):  # type: ignore
        """Schema meta class"""

        model = Resource
        include_relationships = True
        load_instance = True
        include_fk = True
        sqla_session = db.session

    id = ma.auto_field(allow_none=True)
    task_id = ma.auto_field(allow_none=True)


class Task(db.Model):  # type: ignore
    """
    Table task representing one project phase
    Has a parent task and can have sub tasks
    Inputs are linked to resources
    """

    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    # model_id = db.Column(db.Integer, db.ForeignKey("model.id"), nullable=False)

    parent_task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    subtasks = db.relationship(
        "Task", foreign_keys=[parent_task_id], lazy=True, cascade="all"
    )

    resources = db.relationship(
        Resource, backref="task_input", lazy=True, cascade="all"
    )

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def copy(self) -> Any:
        return Task(
            name=self.name,
            subtasks=[subtask.copy() for subtask in self.subtasks],
            resources=[resource.copy() for resource in self.resources],
        )

    def get_environmental_impact(self) -> AggregatedImpact:
        """
        Get a Task complete Environmental impact via an AggregatedImpact object
        :return: an EnvironmentImpact object with all the task environmental impacts
        """
        environmental_impact = AggregatedImpact()

        for r in self.resources:
            environmental_impact.merge_aggregated_impact(r.get_environmental_impact())

        for s in self.subtasks:
            environmental_impact.merge_aggregated_impact(s.get_environmental_impact())

        return environmental_impact

    def get_subtasks_impact(self) -> dict[int, AggregatedImpact]:
        # TODO test comment
        impacts_list = {}
        for subtask in self.subtasks:
            impacts_list[subtask.id] = subtask.get_environmental_impact()
        return impacts_list

    def get_indicator_impact(self, indicator: ImpactIndicator) -> Quantity[Any]:
        """
        Compute and return a Task impact for a given ImpactIndicator
        :param indicator: the ImpactIndicator to get the value for the task
        :return: A quantity corresponding to the task ImpactIndicator chosen
        """
        impacts_resources: List[Quantity[Any]] = [
            r.get_indicator_impact(indicator) for r in self.resources
        ]
        impacts_subtasks: List[Quantity[Any]] = [
            s.get_indicator_impact(indicator) for s in self.subtasks
        ]

        return sum(impacts_resources) + sum(impacts_subtasks)

    def get_impact_by_resource_type(self) -> AggregatedImpactByResource:
        """
        Return a class environmental impact classified by its Resource types
        :param task: task to get the impact from
        :return: AggregatedImpactByResource object, with AggregatedImpact objects by resource type
        """
        result = AggregatedImpactByResource()

        for r in self.resources:
            impacts_to_add = r.get_environmental_impact()
            if r.type in result:
                result[r.type].merge_aggregated_impact(impacts_to_add)
            else:
                result[r.type] = impacts_to_add

        for s in self.subtasks:
            subtasks_impacts = s.get_impact_by_resource_type()
            for resource_type in subtasks_impacts:
                if resource_type in result:
                    result[resource_type].merge_aggregated_impact(
                        subtasks_impacts[resource_type]
                    )
                else:
                    result[resource_type] = subtasks_impacts[resource_type]

        return result


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

    id = ma.auto_field(allow_none=True)
    subtasks = Nested("TaskSchema", many=True)
    resources = Nested(ResourceSchema, many=True)


class Model(db.Model):  # type: ignore
    """
    Table Model representing one possibility for a project with a tree of tasks
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    root_task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    root_task = db.relationship(
        Task, lazy=True, foreign_keys=[root_task_id], cascade="all"
    )

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def copy(self) -> Any:
        model = Model(
            name=self.name,
            root_task=self.root_task.copy(),
            project_id=self.project_id,
        )
        return model


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

    id = ma.auto_field(allow_none=True)
    root_task = Nested("TaskSchema")
    tasks = Nested("TaskSchema", many=True)


class Project(db.Model):  # type: ignore
    """
    Table project which contains multiple models
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def copy(self) -> Any:
        models_copy = [model.copy() for model in self.models]
        project = Project(name=self.name, models=models_copy, base_model=models_copy[0])
        return project


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

    id = ma.auto_field(allow_none=True)
    base_model_id = ma.auto_field(allow_none=True)
    models = Nested("ModelSchema", many=True)
