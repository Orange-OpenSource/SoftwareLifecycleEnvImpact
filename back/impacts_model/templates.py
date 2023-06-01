from __future__ import annotations

import os
from typing import List, Optional

import yaml
from marshmallow import fields, Schema

from impacts_model.impact_sources import impact_source_factory, ImpactSource

####################
# ActivityTemplate #
####################


class ActivityTemplate:
    """
    Define a Activity/Phase as a node containing an ImpactFactor and/or Subactivity(s)
    """

    def __init__(
        self,
        name: str,
    ):
        """
        Define a activity with a name, resources and subactivities
        :param name: the name of the resource
        """
        self.name = name.replace(".yaml", "")
        file_res = self._load_file()
        self.id = file_res[0]
        self.impact_sources = file_res[1]
        self.subactivities = file_res[2]

    def _load_file(self):
        name = self.name.replace(".yaml", "")
        with open("impacts_model/data/activities/" + name + ".yaml", "r") as stream:
            data_loaded = yaml.safe_load(stream)

            impact_sources = []
            if data_loaded["impact_sources"] is not None:
                for impact_source in data_loaded["impact_sources"]:
                    impact_sources.append(impact_source)

            subactivities_list = []
            if data_loaded["subactivities"] is not None:
                for subactivity_name in data_loaded["subactivities"]:
                    subactivities_list.append(ActivityTemplate(subactivity_name))

            return data_loaded["id"], impact_sources, subactivities_list


class ActivityTemplateSchema(Schema):
    """Marshmallow schema to serialize a ActivityTemplate object"""

    id = fields.Integer()
    name = fields.String()
    impact_sources = fields.String(many=True)
    subactivities = fields.Nested("ActivityTemplateSchema", many=True)


def load_activities_templates() -> List[ActivityTemplate]:
    """
    Load and return all ActivityTemplate from files
    """
    activities_template = []
    for filename in os.listdir("impacts_model/data/activities"):
        activities_template.append(ActivityTemplate(filename))
    return activities_template


def get_activity_template_by_id(template_id: int) -> Optional[ActivityTemplate]:
    """
    Search in activity templates and reurn the one corresponding to an id, if it exits
    :param template_id: id of the ActivityTemplate to retrieve
    :return: ActivityTemplate if it exists with id, or None
    """
    return next((x for x in load_activities_templates() if x.id == template_id), None)
