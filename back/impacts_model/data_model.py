# BSD-3-Clause License
#
# Copyright 2017 Orange
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import re
from copy import copy, deepcopy
from typing import Any, List

from flask_marshmallow import Marshmallow as FlaskMarshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_load,
    pre_load,
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
    ImpactSourceId,
    ImpactSourceImpact,
    ActivityImpact,
    merge_env_impact,
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

    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), nullable=False)

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

    def value(self) -> Quantity[Any]:
        """
        Computed the value of the amounts, as a quantity
        Value is of the form : amount * duration * (1/frequency) * period
        duration, frequency and period can be None
        amount is never None
        """
        time = None

        if self.duration is not None:
            # If duration is not None, frequency and period are mandatory
            # Time computation will output a time quantity
            time = (self.duration / self.frequency * self.period).to_reduced_units()
        elif self.frequency is not None:
            # If duration is not but not frequency, then time will be dimensionless
            # Ex: every month for two years = 24 dimensionless
            time = ((1 / self.frequency) * self.period).to_reduced_units()
        elif self.period is not None:
            time = self.period

        if time is None:
            return self.amount

        return (self.amount * time).to_reduced_units()

    def get_impact(self) -> ImpactSourceImpact:
        """
        Get the complete impact, as an ImpactSource
        Environmental impact by self.impact_source_id
        For each ImpactCategory of the ImpactSource, multiply by this resource value()
        Retrun aresource impact, as its value multiplied by the impact source impact
        :return: an ImpactSourceImpact to keep track of the impact source id
        """
        result: ImpactSourceImpact = self.impact_source.get_impact()
        value = self.value()
        result.multiply_by(value)

        return result


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

    id = fields.Integer(allow_none=True)
    activity_id = fields.Integer(allow_none=True)
    updated_at = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(allow_none=True)
    has_time_input = fields.Bool()

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

    @pre_load
    def pre_load(self, data, **kwargs):
        if "has_time_input" in data:
            data.pop("has_time_input")  # Delete hybrid property that can't be set
        return data

    # @post_load
    # def post_load(self, data, **kwargs):
    #     data.has_time_input = None  # Delete hybrid property that can't be set
    #     return data

    @validates_schema
    def validate_quantities(self, data, **kwargs):
        """
        Marshmallow schema validation to insure input follow the rules:
        No time in ImpactSource unit:
            - frequency AND period (to remove time)
            - OR none of them
        Time in ImpactSourceUnit:
            - Period is mandatory
            - frequency AND duration or none of them (to keep time)
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
            if amount is not None and amount.units == impact_source.unit:
                # If it is the right unit, mean that they're is no time in resource_unit, should either have period and frequency or nothing

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
            else:  # If the amount unit is different from the ImpactSource one, mean that it contains time
                # Use the string to compare units
                units_split = re.split(r"[*,/]", str(impact_source.unit))
                units_split_len = len(units_split)

                if units_split_len > 2 or units_split_len == 0:
                    # Should not happen, safeguard for the future
                    errors["impact_source"] = ["ImpactSource unit dimensionality > 2"]
                elif units_split_len == 2:
                    # Means that period is mandatory, or if no time in impactsource unit that the inputed unit should match with a dimensionality of 2

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
                            # If period is set, either frequency and duration should be set, or none of them
                            if duration is not None and frequency is None:
                                errors["frequency"] = [
                                    "If duration is set, frequency should be set"
                                ]
                            elif duration is None and frequency is not None:
                                errors["duration"] = [
                                    "If frequency is set, duration should be set"
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
            errors["impact_source_id"] = [
                "Wrong impact_source_id: " + data["impact_source_id"]
            ]

        if errors:
            raise ValidationError(errors)


class Activity(db.Model):  # type: ignore
    """
    Table activity representing one project phase
    Has a parent activity and can have sub activities
    Inputs are linked to resources
    """

    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    # model_id = db.Column(db.Integer, db.ForeignKey("model.id"), nullable=False)

    parent_activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"))
    subactivities = db.relationship(
        "Activity", foreign_keys=[parent_activity_id], lazy=True, cascade="all"
    )

    resources: list[Resource] = db.relationship(
        Resource, backref="resource", lazy=True, cascade="all"
    )

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __copy__(self):
        """Override of copy function to return a Activity stripped of ids"""
        return Activity(
            name=self.name,
            subactivities=[copy(subactivity) for subactivity in self.subactivities],
            resources=[copy(resource) for resource in self.resources],
        )

    def get_impact(self) -> ActivityImpact:
        """
        Compute and return this Activity complete impact as a ActivityImpact
        """
        subactivities = self._get_subactivities_impact()
        resources = self._get_resources_impact(subactivities)
        total = self._get_total(resources)

        return ActivityImpact(
            activity_id=self.id,
            total=total,
            sub_activities=subactivities,
            impact_sources=resources,
        )

    def _get_total(
        self,
        resources: dict[ImpactSourceId, ImpactSourceImpact],
    ) -> EnvironmentalImpact:
        """
        Return the complete EnvironmentalImpact of the activity as the sum of its resources
        """
        result: EnvironmentalImpact = {}

        # Sum resources impacts
        for resource in resources:
            result = merge_env_impact(result, resources[resource].total_impact)

        return result

    def _get_resources_impact(
        self, subactivities_impacts: List[ActivityImpact]
    ) -> dict[ImpactSourceId, ImpactSourceImpact]:
        """
        Get resources impacts, sum of this one AND subactivities one
        """
        result: dict[ImpactSourceId, ImpactSourceImpact] = {}

        # Sum subactivities resources
        for subactivityImpact in subactivities_impacts:
            subImpactSources = subactivityImpact.impact_sources
            # Iterate trough id
            for i in subImpactSources:
                subImpactSource = subImpactSources[i]
                # Add to result
                if subImpactSource.impact_source_id not in result:
                    result[subImpactSource.impact_source_id] = deepcopy(subImpactSource)
                else:
                    result[subImpactSource.impact_source_id].add(subImpactSource)

        # Sum self resources
        for r in self.resources:
            if r.impact_source_id not in result:
                result[r.impact_source_id] = r.get_impact()
            else:
                result[r.impact_source_id].add(r.get_impact())

        return result

    def _get_subactivities_impact(self) -> List[ActivityImpact]:
        """
        Return a dict with all subactivity ids as key, with their ActivityImpact as values
        """
        impacts_list: List[ActivityImpact] = []
        for subactivity in self.subactivities:
            impacts_list.append(subactivity.get_impact())
        return impacts_list


class ActivitySchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for Activity to serialize/deserialize
    Specify nested elements to show theme completely when deserializing, ot only their id
    """

    class Meta(ma.SQLAlchemyAutoSchema.Meta):  # type: ignore
        """Schema meta class"""

        model = Activity
        include_relationships = True
        load_instance = True
        include_fk = True
        sqla_session = db.session

    id = ma.auto_field(allow_none=True)
    subactivities = Nested("ActivitySchema", many=True)
    resources = Nested(ResourceSchema, many=True)


class Model(db.Model):  # type: ignore
    """
    Table Model representing one possibility for a project with a tree of activities
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    root_activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"))
    root_activity = db.relationship(
        Activity, lazy=True, foreign_keys=[root_activity_id], cascade="all"
    )

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __copy__(self):
        """Override of copy function to return a Model stripped of ids"""
        copy_root = copy(self.root_activity)
        copy_root.name += " copy"
        return Model(name=self.name + " copy", root_activity=copy_root)


class ModelSchema(ma.SQLAlchemyAutoSchema):  # type: ignore
    """
    Schema for Model to serialize/deserialize
    Nested activities to show them when deserializing
    """

    class Meta(ma.SQLAlchemyAutoSchema.Meta):  # type: ignore
        """Schema meta class"""

        model = Model
        include_relationships = True
        load_instance = True
        include_fk = True
        sqla_session = db.session

    id = ma.auto_field(allow_none=True)
    root_activity = Nested("ActivitySchema")
    activities = Nested("ActivitySchema", many=True)
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
