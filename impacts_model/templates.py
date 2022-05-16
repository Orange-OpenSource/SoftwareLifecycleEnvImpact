from __future__ import annotations

import os
from typing import List

import yaml
from marshmallow import fields, Schema

####################
# ResourceTemplate #
####################
from impacts_model.impact_sources import impact_source_factory, ImpactSource


class ResourceTemplate:
    """
    Resource template to load from files
    A name with a list of ImpactSource
    """
    def __init__(self, name: str):
        self.name = name
        self.impact_sources = self._load_impacts()

    def _load_impacts(self) -> List[ImpactSource]:
        """
        Load the list of impact_sources from the corresponding Resource file
        """
        name = self.name.replace(".yaml", "")
        with open("impacts_model/data/resources/" + name + ".yaml", "r") as stream:
            data_loaded = yaml.safe_load(stream)
            impacts_list = []
            for impact_name in data_loaded["impact_factors"]:
                impacts_list.append(impact_source_factory(impact_name))
            return impacts_list


class ResourceTemplateSchema(Schema):
    """Marshmallow schema to serialize a ResourceTemplate object"""
    name = fields.String()


################
# TaskTemplate #
################


class TaskTemplate:
    """
    Define a Task/Phase as a node containing an ImpactFactor and/or Subtask(s)
    """

    def __init__(
        self,
        name: str,
    ):
        """
        Define a task with a name, resources and subtasks
        :param name: the name of the resource
        """
        self.name = name.replace(".yaml", "")
        file_res = self._load_file()
        self.resources = file_res[0]
        self.subtasks = file_res[1]

    def _load_file(self):
        name = self.name.replace(".yaml", "")
        with open("impacts_model/data/tasks/" + name + ".yaml", "r") as stream:
            data_loaded = yaml.safe_load(stream)

            resources_list = []
            if data_loaded["resources"] is not None:
                for resource_name in data_loaded["resources"]:
                    resources_list.append(ResourceTemplate(resource_name))

            subtasks_list = []
            if data_loaded["subtasks"] is not None:
                for subtask_name in data_loaded["subtasks"]:
                    subtasks_list.append(TaskTemplate(subtask_name))

            return resources_list, subtasks_list


class TaskTemplateSchema(Schema):
    """Marshmallow schema to serialize a TaskTemplate object"""
    name = fields.String()
    resources = fields.Nested(ResourceTemplateSchema, many=True)
    subtasks = fields.Nested("TaskTemplateSchema", many=True)


def get_tasks_templates() -> List[TaskTemplate]:
    """Load and return all TaskTemplate from files"""
    tasks_template = []
    for filename in os.listdir("impacts_model/data/tasks"):
        tasks_template.append(TaskTemplate(filename))
    return tasks_template
