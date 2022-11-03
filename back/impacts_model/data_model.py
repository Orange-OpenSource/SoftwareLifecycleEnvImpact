from typing import Any, List
from flask_marshmallow import Marshmallow as FlaskMarshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy.fields import Nested
from pint import Quantity
from sqlalchemy import func

from impacts_model.impacts import (
    AggregatedImpact,
    AggregatedImpactByResource,
    ImpactCategory,
)
from impacts_model.impact_sources import impact_source_factory, ImpactSource
from impacts_model.quantities.quantities import deserialize_pint, serialize_pint
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()
ma = FlaskMarshmallow()


class Resource(db.Model):  # type: ignore
    """
    Resource object and table with a name, an impact source name and a computed value from duration and input
    """

    __tablename__ = "resource"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    impact_source_id = db.Column(db.String, nullable=False)

    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)

    _input = db.Column(db.String, nullable=False)
    _time_use = db.Column(db.String)
    _frequency = db.Column(db.String)
    _duration = db.Column(db.String)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @hybrid_property
    def input(self):
        # Pint does not deal with None values
        if self._input is None:
            return None
        else:
            # Quantity are stored as string in the database, deserialize it
            return deserialize_pint(self._input)

    @input.setter
    def input(self, input):
        if input is None:
            self._input = None
            return

        # Check the given input is a pint.Quantity instance
        # try:
        #     if not input.check("[any]"):
        #         raise ValueError(
        #             "Input must be a Quantity with a dimensionality of [any]"
        #         )
        # except AttributeError:
        #     raise TypeError("Input must be a Quantity")
        # TODO check for the quantity given to inputs
        if not isinstance(input, Quantity):
            try:
                input = deserialize_pint(input)
            except Exception as err:
                raise TypeError("Input must be a Quantity")

        # Serialize the value to save in database
        self._input = serialize_pint(input)

    @input.expression
    def input(self):
        # Used as filter by SQLAlchemy queries
        return self._input

    @hybrid_property
    def time_use(self):
        # Pint does not deal with None values
        if self._time_use is None:
            return None
        else:
            # Quantity are stored as string in the database, deserialize it
            return deserialize_pint(self._time_use)

    @time_use.setter
    def time_use(self, time_use):
        if time_use is None:
            self._time_use = None
            return

        # Check the given time_use is a pint.Quantity instance with a dimension of 'time'
        try:
            if not time_use.check("[time]"):
                raise ValueError(
                    "Time use must be a Quantity with a dimensionality of [time]"
                )
        except AttributeError:
            raise TypeError("Time use must be a Quantity")

        # Serialize the value to save in database
        self._time_use = serialize_pint(time_use)

    @time_use.expression
    def time_use(self):
        # Used as filter by SQLAlchemy queries
        return self._time_use

    @hybrid_property
    def frequency(self):
        # Pint does not deal with None values
        if self._frequency is None:
            return None
        else:
            # Quantity are stored as string in the database, deserialize it
            return deserialize_pint(self._frequency)

    @frequency.setter
    def frequency(self, frequency):
        if frequency is None:
            self._frequency = None
            return

        # Check the given duration is a pint.Quantity instance with a dimension of 'time'
        try:
            if not frequency.check("1/[time]"):  # TODO test this
                raise ValueError(
                    "Frequency must be a Quantity with a dimensionality of 1/[time]"
                )
        except AttributeError:
            raise TypeError("Frequency must be a Quantity")

        # Serialize the value to save in database
        self._frequency = serialize_pint(frequency)

    @frequency.expression
    def frequency(self):
        # Used as filter by SQLAlchemy queries
        return self._frequency

    @hybrid_property
    def duration(self):
        # Pint does not deal with None values
        if self._duration is None:
            return None
        else:
            # Quantity are stored as string in the database, deserialize it
            return deserialize_pint(self._duration)

    @duration.setter
    def duration(self, duration):
        if duration is None:
            self._duration = None
            return

        # Check the given duration is a pint.Quantity instance with a dimension of 'time'
        try:
            if not duration.check("[time]"):
                raise ValueError(
                    "Duration must be a Quantity with a dimensionality of [time]"
                )
        except AttributeError:
            raise TypeError("Duration must be a Quantity")

        # Serialize the value to save in database
        self._duration = serialize_pint(duration)

    @duration.expression
    def duration(self):
        # Used as filter by SQLAlchemy queries
        return self._duration

    def value(self):  # TODO put this return as a quantity
        return (
            self.input
            * (self.time_use if self.time_use is not None else 1)
            * (self.frequency if self.frequency is not None else 1)
            * (self.duration if self.duration is not None else 1)
        )
        # TODO unit test

    def copy(self) -> Any:

        return Resource(
            name=self.name,
            impact_source_id=self.impact_source_id,
            _input=self._input,
            _time_use=self._time_use,
            _frequency=self._frequency,
            _duration=self._duration,
        )

    def get_environmental_impact(self) -> AggregatedImpact:
        """
        Get a resource complete environmental impact as an EnvironmentalImpact object
        :return: an AggregatedImpact object with all resource impacts
        """
        impact_source = impact_source_factory(self.impact_source_id)
        aggregated_impact = AggregatedImpact()

        for key in impact_source.aggregated_impact.impacts:
            aggregated_impact.merge_impact(
                key,
                impact_source.aggregated_impact.impacts[key]
                * self.value()
                / impact_source.unit,  # TODO this is probably a bad way
            )

        return aggregated_impact

    def get_category_impact(self, impact_category: ImpactCategory) -> Quantity[Any]:
        """
        Compute and return a resource environmental impact for an ImpactCategory
        :param resource: the Resource object to view to impact from
        :param impact_category: The ImpactCategory to retrieve the impact
        :return: A quantity corresponding to the resource ImpactCategory quantity
        """
        impact_source = impact_source_factory(self.impact_source_id)

        return (
            impact_source.aggregated_impact.impacts[impact_category]
            * self.value()  # TODO this should not use the aggregated impacts
        )


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

    _input = ma.auto_field(data_key="input", attribute="_input", allow_none=False)
    _time_use = ma.auto_field(data_key="time_use", attribute="_time_use")
    _frequency = ma.auto_field(data_key="frequency", attribute="_frequency")
    _duration = ma.auto_field(
        data_key="duration", attribute="_duration", allow_none=False
    )


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

    def get_category_impact(self, category: ImpactCategory) -> Quantity[Any]:
        """
        Compute and return a Task impact for a given ImpactCategory
        :param category: the ImpactCategory to get the value for the task
        :return: A quantity corresponding to the task ImpactCategory chosen
        """
        impacts_resources: List[Quantity[Any]] = [
            r.get_category_impact(category) for r in self.resources
        ]
        impacts_subtasks: List[Quantity[Any]] = [
            s.get_category_impact(category) for s in self.subtasks
        ]

        return sum(impacts_resources) + sum(impacts_subtasks)

    def get_impact_by_resource_type(self) -> AggregatedImpactByResource:
        """
        Return a class environmental impact classified by its Resource types
        :param task: task to get the impact from
        :return: AggregatedImpactByResource object, with AggregatedImpact objects by resource type
        """
        result: AggregatedImpactByResource = {}

        for r in self.resources:
            impacts_to_add = r.get_environmental_impact()
            if r.impact_source_id in result:
                result[r.impact_source_id].merge_aggregated_impact(impacts_to_add)
            else:
                result[r.impact_source_id] = impacts_to_add

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
        return Model(
            name=self.name,
            root_task=self.root_task.copy(),
        )


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
    project_id = ma.auto_field(allow_none=True)


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

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def copy(self) -> Any:
        models_copy = [model.copy() for model in self.models]
        project = Project(name=self.name, models=models_copy)
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
    models = Nested("ModelSchema", many=True)
