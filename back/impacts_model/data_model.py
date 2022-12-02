import re
from copy import copy
from typing import Any, List

from flask_marshmallow import Marshmallow as FlaskMarshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_load,
    pre_dump,
    validates_schema,
)
from marshmallow_sqlalchemy.fields import Nested
from pint import Quantity
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

from impacts_model.impact_sources import (
    ImpactSource,
    ImpactSourceError,
    impact_source_factory,
)
from impacts_model.impacts import (
    EnvironmentalImpact,
    EnvironmentalImpactByResource,
    ImpactCategory,
)
from impacts_model.quantities.quantities import (
    deserialize_quantity,
    serialize_quantity,
)

db = SQLAlchemy()
ma = FlaskMarshmallow()


class Resource(db.Model):  # type: ignore
    """
    Resource object and table with a name, an impact source name and a computed value from period and amount
    """

    __tablename__ = "resource"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    impact_source_id = db.Column(db.String, nullable=False)

    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)

    _amount = db.Column(db.String, nullable=False)
    _duration = db.Column(db.String)
    _frequency = db.Column(db.String)
    _period = db.Column(db.String)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @hybrid_property
    def impact_source(self) -> ImpactSource:
        """Load and return ImpactSource corresponding to saved id"""
        return impact_source_factory(self.impact_source_id)

    @hybrid_property
    def has_time_input(self) -> bool:
        try:
            return self.impact_source.has_time_input
        except:
            print("no impactsource for " + self.impact_source_id)
            return False

    @hybrid_property
    def amount(self) -> Quantity[Any]:
        # Pint does not deal with None values
        if self._amount is None:
            return None
        else:
            # Quantity are stored as string in the database, deserialize it
            return deserialize_quantity(self._amount)

    @amount.setter
    def amount(self, amount) -> None:
        if amount is None:
            self._amount = None
            return

        if not isinstance(amount, Quantity):
            try:
                amount = deserialize_quantity(amount)
            except Exception as err:
                raise TypeError("Amount must be a Quantity")

        # Serialize the value to save in database
        self._amount = serialize_quantity(amount)

    @amount.expression
    def amount(self) -> str:
        # Used as filter by SQLAlchemy queries
        return self._amount

    @hybrid_property
    def duration(self):
        # Pint does not deal with None values
        if self._duration is None:
            return None
        else:
            # Quantity are stored as string in the database, deserialize it
            return deserialize_quantity(self._duration)

    @duration.setter
    def duration(self, duration):
        if duration is None:
            self._duration = None
            return

        # Check the given duration is a pint.Quantity instance with a dimension of 'time'
        try:
            if not duration.check("[time]"):
                raise ValueError(
                    "Time use must be a Quantity with a dimensionality of [time]"
                )
        except AttributeError:
            raise TypeError("Time use must be a Quantity")

        # Serialize the value to save in database
        self._duration = serialize_quantity(duration)

    @duration.expression
    def duration(self):
        # Used as filter by SQLAlchemy queries
        return self._duration

    @hybrid_property
    def frequency(self):
        # Pint does not deal with None values
        if self._frequency is None:
            return None
        else:
            # Quantity are stored as string in the database, deserialize it
            return deserialize_quantity(self._frequency)

    @frequency.setter
    def frequency(self, frequency):
        if frequency is None:
            self._frequency = None
            return

        # Check the given frequency is a pint.Quantity instance with a dimension of 'time'
        try:
            if not frequency.check("[time]"):  # TODO test this
                raise ValueError(
                    "Frequency must be a Quantity with a dimensionality of [time]"
                )
        except AttributeError:
            raise TypeError("Frequency must be a Quantity")

        # Serialize the value to save in database
        self._frequency = serialize_quantity(frequency)

    @frequency.expression
    def frequency(self):
        # Used as filter by SQLAlchemy queries
        return self._frequency

    @hybrid_property
    def period(self):
        # Pint does not deal with None values
        if self._period is None:
            return None
        else:
            # Quantity are stored as string in the database, deserialize it
            return deserialize_quantity(self._period)

    @period.setter
    def period(self, period):
        if period is None:
            self.period = None
            return

        # Check the given period is a pint.Quantity instance with a dimension of 'time'
        try:
            if not period.check("[time]"):
                raise ValueError(
                    "Period must be a Quantity with a dimensionality of [time]"
                )
        except AttributeError:
            raise TypeError("Period must be a Quantity")

        # Serialize the value to save in database
        self._period = serialize_quantity(period)

    @period.expression
    def period(self):
        # Used as filter by SQLAlchemy queries
        return self._period

    def value(self) -> Quantity[Any]:
        """
        Computed the value of the amounts, as a quantity
        Value is of the form : amount * duration * (1/frequency) * period
        duration, frequency and period can be None
        """
        return (
            self.amount
            * (self.duration if self.duration is not None else 1)
            / (self.frequency if self.frequency is not None else 1)
            * (self.period if self.period is not None else 1)
        )

    def __copy__(self):
        """Override of copy function to return a Resource stripped of ids"""
        return Resource(
            name=self.name,
            impact_source_id=self.impact_source_id,
            _amount=self._amount,
            _duration=self._duration,
            _frequency=self._frequency,
            _period=self._period,
        )

    def get_environmental_impact(self) -> EnvironmentalImpact:
        """
        Get a resource complete environmental impact as an EnvironmentalImpact object
        :return: an EnvironmentalImpact object with all resource impacts
        """
        environmental_impact = EnvironmentalImpact()

        for key in self.impact_source.environmental_impact.impacts:
            # Adding the impact to impact category indicator unit
            environmental_impact.add_impact(
                key,
                (
                    self.impact_source.environmental_impact.impacts[key] * self.value()
                ).to(key.value),
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
            * self.value()
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
        if isinstance(data, Quantity):
            data = {
                "value": data.magnitude,
                "unit": data.units,
            }
        else:  # mean its a string
            try:
                split = data.split()
                data = {
                    "value": round(float(split[0]), 2),
                    "unit": split[1],
                }
            except:
                return data
        return data

    @validates_schema
    def validate_quantities(self, data, **kwargs):
        if "value" not in data or data["value"] == "":
            raise ValidationError("Missing value")
        if "unit" not in data["unit"] == "":
            raise ValidationError("Missing unit")
        try:
            deserialize_quantity(str(data["value"]) + " " + data["unit"])
        except TypeError:
            raise ValidationError("Wrong quantity format")


class ResourceSchema(Schema):  # type: ignore
    """
    Resource schema to serialize a Resource object
    """

    id = fields.Integer(allow_none=True)
    task_id = fields.Integer(allow_none=True)
    name = fields.String()

    impact_source_id = fields.String()
    has_time_input = fields.Bool()

    updated_at = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(allow_none=True)

    _amount = Nested(
        QuantitySchema,
        data_key="amount",
        attribute="_amount",
        allow_none=False,
        many=False,
    )
    _duration = Nested(
        QuantitySchema,
        data_key="duration",
        attribute="_duration",
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
    _period = Nested(
        QuantitySchema,
        data_key="period",
        attribute="_period",
        allow_none=True,
        many=False,
    )

    @post_load
    def post_load(self, data, **kwargs):
        if "has_time_input" in data:
            data.pop("has_time_input")  # Delete hybrid property that can't be set
        return Resource(**data)

    @validates_schema
    def validate_quantities(self, data, **kwargs):
        """
        Marshmallow schema validation to insure input follow the rules:
        No time in ImpactSource unit: frequency AND period OR none of them
        Time in ImpactSourceUnit:
            - Period is mandatory
            - If duration is is set, frequency should also be set
        """
        errors = {}

        try:
            # Validate that the ImpactSource can be retrieved
            impact_source = impact_source_factory(data["impact_source_id"])

            # Deserialize the quantities
            amount = (
                deserialize_quantity(data["_amount"]) if "_amount" in data else None
            )
            period = (
                deserialize_quantity(data["_period"]) if "_period" in data else None
            )
            duration = (
                deserialize_quantity(data["_duration"]) if "_duration" in data else None
            )
            frequency = (
                deserialize_quantity(data["_frequency"])
                if "_frequency" in data
                else None
            )

            # Validate that the amount unit correspond to the ImpactSource one
            if amount.units == impact_source.unit:
                # If it is the right unit, and they're is no time in resource_unit, should either have period and frequency or nothing

                if period is None and frequency is not None:
                    errors["period"] = [
                        "period should not be none if frequency is set, as they're is no [time] the ImpactSource unit ("
                        + str(impact_source.unit)
                        + ")"
                    ]
                if frequency is None and period is not None:
                    errors["frequency"] = [
                        "frequency should not be none if period is set, as they're is no [time] the ImpactSource unit ("
                        + str(impact_source.unit)
                        + ")"
                    ]
                if (1 * amount.units).check("[time]"):
                    # Should not happen, safeguard for the future
                    errors["amount"] = ["ImpactSource input can't be time"]
            else:  # If the amount unit is different from the ImpactSource one
                # Use the string to compare units
                units_split = re.split(r"[*,/]", str(impact_source.unit))
                units_split_len = len(units_split)

                if units_split_len > 2 or units_split_len == 0:
                    # Should not happen, safeguard for the future
                    errors["impact_source"] = ["ImpactSource unit dimensionality > 2"]
                elif units_split_len == 2:
                    # Means that period should be set, or if no time in impactsource unit that the inputed unit should match with a dimensionality of 2

                    # Check that time is present in ImpactSource unit
                    if deserialize_quantity(1 * units_split[0]).check(
                        "[time]"
                    ) or deserialize_quantity(1 * units_split[1]).check("[time]"):

                        # If time in ImpactSourceUnit, period should be set
                        if period is None:
                            errors["period"] = [
                                "Impact source unit is "
                                + str(impact_source.unit)
                                + ", period is needed"
                            ]
                        else:
                            # If period is set, frequency and (time use and frequency) can be set, not duration alone
                            if duration is not None and frequency is None:
                                errors["frequency"] = [
                                    "If duration is set, frequency should be set"
                                ]
                    else:
                        # No time in ImpactSource unit
                        errors["amount"] = [
                            "Amount unit should be " + str(impact_source.unit)
                        ]
                elif units_split_len == 1:
                    # Wrong unit
                    errors["amount"] = [
                        "Amount unit should be " + str(impact_source.unit)
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

    def __copy__(self):
        """Override of copy function to return a Task stripped of ids"""
        return Task(
            name=self.name,
            subtasks=[copy(subtask) for subtask in self.subtasks],
            resources=[copy(resource) for resource in self.resources],
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
        """
        Return a dict with all subtask ids as key, with their EnvironmentalImpact as values
        """
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

    def __copy__(self):
        """Override of copy function to return a Model stripped of ids"""
        copy_root = copy(self.root_task)
        copy_root.name += " copy"
        return Model(name=self.name + " copy", root_task=copy_root)


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

    def __copy__(self) -> Any:
        """Override of copy function to return a Project stripped of ids"""
        models_copy = [copy(model) for model in self.models]
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
