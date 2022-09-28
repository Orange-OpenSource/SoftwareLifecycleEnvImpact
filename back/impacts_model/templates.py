from __future__ import annotations

import os
from typing import List, Optional

import yaml
from marshmallow import fields, Schema

from impacts_model.impact_sources import impact_source_factory, ImpactSource


####################
# ResourceTemplate #
####################


class ResourceTemplate:
    """
    Resource template to load from files
    A name with a list of ImpactSource
    """

    def __init__(self, name: str):
        self.name = name.replace(".yaml", "")
        self.impact_sources = self._load_impacts()

    def _load_impacts(self) -> List[ImpactSource]:
        """
        Load the list of impact_sources from the corresponding Resource file
        """
        with open("impacts_model/data/resources/" + self.name + ".yaml", "r") as stream:
            data_loaded = yaml.safe_load(stream)
            self.id = data_loaded["id"]
            impacts_list = []
            for impact_name in data_loaded["impact_factors"]:
                impacts_list.append(impact_source_factory(impact_name))
            return impacts_list


class ResourceTemplateSchema(Schema):
    """Marshmallow schema to serialize a ResourceTemplate object"""
    id = fields.Integer()
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
        self.id = file_res[0]
        self.unit = file_res[1]
        self.resources = file_res[2]
        self.subtasks = file_res[3]

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

            return data_loaded["id"], data_loaded["unit"], resources_list, subtasks_list


class TaskTemplateSchema(Schema):
    """Marshmallow schema to serialize a TaskTemplate object"""

    id = fields.Integer()
    name = fields.String()
    resources = fields.Nested(ResourceTemplateSchema, many=True)
    subtasks = fields.Nested("TaskTemplateSchema", many=True)


def get_tasks_templates() -> List[TaskTemplate]:  # TODO improve naming clash with route
    """
    Load and return all TaskTemplate from files
    """
    tasks_template = []
    for filename in os.listdir("impacts_model/data/tasks"):
        tasks_template.append(TaskTemplate(filename))
    return tasks_template


def get_task_template_by_id(template_id: int) -> Optional[TaskTemplate]:
    """
    Search in task templates and reurn the one corresponding to an id, if it exits
    :param template_id: id of the TaskTemplate to retrieve
    :return: TaskTemplate if it exists with id, or None
    """
    return [x for x in get_tasks_templates() if x.id == template_id][
        0
    ]  # TODO bad solution to create associated resource


def get_resources_templates() -> List[ResourceTemplate]:
    """
    Load and return all ResourceTemplate from files
    Memoized function to avoid loading from files at each call
    """
    resources_template = []
    for filename in os.listdir("impacts_model/data/resources"):
        resources_template.append(ResourceTemplate(filename))
    return resources_template

def get_resource_template_by_id(template_id: int) -> Optional[ResourceTemplate]:
    """
    Search in resource templates and reurn the one corresponding to an id, if it exits
    :param template_id: id of the ResourceTemplate to retrieve
    :return: ResourceTemplate if it exists with id, or None
    """
    return [x for x in get_resources_templates() if x.id == template_id][
        0
    ]  # TODO bad solution to create associated resource