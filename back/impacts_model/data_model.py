from typing import Any, List, Optional
from flask_marshmallow import Marshmallow as FlaskMarshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError, validates_schema
from marshmallow_sqlalchemy.fields import Nested
from pint import Quantity
from sqlalchemy import func
import re
from marshmallow import post_dump, pre_load, pre_dump, post_load

from impacts_model.impacts import (
    EnvironmentalImpact,
    EnvironmentalImpactByResource,
    ImpactCategory,
)
from impacts_model.impact_sources import (
    ImpactSourceError,
    impact_source_factory,
)
from impacts_model.quantities.quantities import (
    MONTH,
    TIME,
    deserialize_pint,
    serialize_pint,
)
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

db = SQLAlchemy()
ma = FlaskMarshmallow()


class Resource(db.Model):  # type: ignore
    """
    Resource object and table with a name, an impact source name and a computed value from duration and input
    """

    __tablename__ = "resource"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    def impact_source(self):
        return impact_source_factory(self.impact_source_id)

    @hybrid_property
    def input(self) -> Quantity[Any]:
        # Pint does not deal with None values
        if self._input is None:
            return None
        else:
            # Quantity are stored as string in the database, deserialize it
            return deserialize_pint(self._input)

    @input.setter
    def input(self, input) -> None:
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
    def input(self) -> str:
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
            if not frequency.check("[time]"):  # TODO test this
                raise ValueError(
                    "Frequency must be a Quantity with a dimensionality of [time]"
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

    def value(self) -> Quantity[Any]:
        return (
            self.input
            * (self.time_use if self.time_use is not None else 1)
            / (self.frequency if self.frequency is not None else 1)
            * (self.duration if self.duration is not None else 1)
        )
        # TODO unit test

    def copy(self) -> Any:

        return Resource(
            impact_source_id=self.impact_source_id,
            _input=self._input,
            _time_use=self._time_use,
            _frequency=self._frequency,
            _duration=self._duration,
        )

    def get_environmental_impact(self) -> EnvironmentalImpact:
        """
        Get a resource complete environmental impact as an EnvironmentalImpact object
        :return: an EnvironmentalImpact object with all resource impacts
        """
        environmental_impact = EnvironmentalImpact()

        for key in self.impact_source.environmental_impact.impacts:
            environmental_impact.add_impact(
                key, self.impact_source.environmental_impact.impacts[key] * self.value()
            )

        return environmental_impact

    def get_category_impact(self, impact_category: ImpactCategory) -> Quantity[Any]:
        """
        Compute and return a resource environmental impact for an ImpactCategory
        :param resource: the Resource object to view to impact from
        :param impact_category: The ImpactCategory to retrieve the impact
        :return: A quantity corresponding to the resource ImpactCategory quantity
        """
        return (
            self.impact_source.environmental_impact.impacts[impact_category]
            * self.value()  # TODO this should not use the aggregated impacts
        )


class QuantitySchema(Schema):
    value = fields.Number()
    unit = fields.Str()

    @post_load
    def post_load(self, data, **kwargs):
        """Translate serialized pint quantites before loading"""
        return str(data["value"]) + " " + data["unit"]

    @pre_dump
    def preprocess(self, data, **kwargs):
        """Translate pint quantities to dict before serialization
        {
            'value': 12421.4213,
            'unit': "KG_CO2E",
        }
        """
        split = data.split()
        data = {
            "value": round(float(split[0]), 2),
            "unit": split[1],
        }
        return data

    @validates_schema
    def validate_quantities(self, data, **kwargs):
        try:
            deserialize_pint(str(data["value"]) + " " + data["unit"])
        except TypeError:
            raise ValidationError("Wrong quantity format")


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

    _input = Nested(
        QuantitySchema,
        data_key="input",
        attribute="_input",
        allow_none=False,
        many=False,
    )
    _time_use = Nested(
        QuantitySchema,
        data_key="time_use",
        attribute="_time_use",
        allow_none=True,
        many=False,
    )
    _frequency = Nested(
        QuantitySchema,
        data_key="frequency",
        attribute="_frequency",
        allow_none=True,
        many=False,
    )
    _duration = Nested(
        QuantitySchema,
        data_key="duration",
        attribute="_duration",
        allow_none=True,
        many=False,
    )

    @pre_load
    def pre_load(self, data, **kwargs):
        return data

    @post_load
    def post_load(self, data, **kwargs):
        return data

    @pre_dump
    def pre_dump(self, data, **kwargs):
        return data
    
    @post_dump
    def post_dump(self, data, **kwargs):
        return data

    # Validate time in resource (duration, duration and frequency, duration an frequency and time_use)

    # Validate no time in resource either duration and frequency or nothing

    @validates_schema
    def validate_quantities(self, data, **kwargs):
        errors = {}

        try:
            # Validate that the ImpactSource can be retrieved
            impact_source = impact_source_factory(data["impact_source_id"])

            # Deserialize the quantities
            input = deserialize_pint(data["_input"]) if "_input" in data else None
            duration = deserialize_pint(data["_duration"]) if "_duration" in data else None
            time_use = deserialize_pint(data["_time_use"]) if "_time_use" in data else None
            frequency = deserialize_pint(data["_frequency"]) if "_frequency" in data else None

            # Validate that the input unit correspond to the ImpactSource one
            if input.units == impact_source.unit:
                # If it is the right unit, and they're is no time in resource_unit, should either have time_use and frequency or nothing
                # TODO is there really no time here ?
                if time_use is None and frequency is not None:
                    errors["time_use"] = [
                        "time_use should not be none if frequency is set, as they're is no [time] the ImpactSource unit ("
                        + str(impact_source.unit)
                        + ")"
                    ]
                if frequency is None and time_use is not None:
                    errors["frequency"] = [
                        "frequency should not be none if time_use is set, as they're is no [time] the ImpactSource unit ("
                        + str(impact_source.unit)
                        + ")"
                    ]
            else:
                # If the input unit is different from the ImpactSource one

                # Use the string to compare units
                units_split = re.split(r"[*,/]", str(impact_source.unit))
                units_split_len = len(units_split)

                if units_split_len > 2 or units_split_len == 0:
                    # Should not happen, safeguard for the future
                    errors["impact_source"] = ["ImpactSource unit dimensionality > 2"]
                elif units_split_len == 2:
                    # Means that duration should be set, or if no time in impactsource unit that input unit should match with a dimensionality of 2

                    # Check that time is present in ImpactSource unit
                    if deserialize_pint(1 * units_split[0]).check(
                        "[time]"
                    ) or deserialize_pint(1 * units_split[1]).check("[time]"):

                        # If time in ImpactSourceUnit, duration should be set
                        if duration is None:
                            errors["_duration"] = [
                                "Impact source unit is "
                                + str(impact_source.unit)
                                + ", duration is needed"
                            ]
                        else:
                            # If duration is set, frequency and (time use and frequency) can be set, not time_use alone
                            if time_use is not None and frequency is None:
                                errors["_time_use"] = [
                                    "If time_use is set, frequency should be set"
                                ]
                    else:
                        # No time in ImpactSource unit
                        errors["_input"] = [
                            "Input unit should be " + str(impact_source.unit)
                        ]
                elif units_split_len == 1:
                    errors["_input"] = [
                        "Input unit should be " + str(impact_source.unit)
                    ]
        except ImpactSourceError:
            errors["impact_source_id"] = ["Wrong impact_source_id"]

        if errors:
            raise ValidationError(errors)


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

    def get_environmental_impact(self) -> EnvironmentalImpact:
        """
        Get a Task complete Environmental impact via an EnvironmentalImpact object
        :return: an EnvironmentalImpact object with all the task environmental impacts
        """
        environmental_impact = EnvironmentalImpact()

        for r in self.resources:
            environmental_impact.add(r.get_environmental_impact())

        for s in self.subtasks:
            environmental_impact.add(s.get_environmental_impact())

        return environmental_impact

    def get_subtasks_impact(self) -> dict[int, EnvironmentalImpact]:
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

    def get_impact_by_resource_type(self) -> EnvironmentalImpactByResource:
        """
        Return a class environmental impact classified by its Resource types
        :param task: task to get the impact from
        :return: EnvironmentalImpactByResource object, with EnvironmentalImpact objects by resource type
        """
        result: EnvironmentalImpactByResource = {}

        for r in self.resources:
            impacts_to_add = r.get_environmental_impact()
            if r.impact_source_id in result:
                result[r.impact_source_id].add(impacts_to_add)
            else:
                result[r.impact_source_id] = impacts_to_add

        for s in self.subtasks:
            subtasks_impacts = s.get_impact_by_resource_type()
            for resource_type in subtasks_impacts:
                if resource_type in result:
                    result[resource_type].add(subtasks_impacts[resource_type])
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
