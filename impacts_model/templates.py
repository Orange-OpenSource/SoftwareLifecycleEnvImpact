from __future__ import annotations

import os
from typing import List

import yaml

from api.data_model import Resource
from impacts_model.impact_sources import impact_source_factory, ImpactSource


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
        resources: List[Resource] = None,
        subtasks: List[TaskTemplate] = None,
    ):
        """
        Define a task with a name, resources and subtasks
        :param name: the name of the resource
        :param resources: optional list of resources
        :param subtasks: optional list of subtasks
        """
        self.name = name
        self.resources = resources if (resources is not None) else []
        self.subtasks = subtasks if (subtasks is not None) else []


def get_tasks_templates() -> [TaskTemplate]:
    tasks_template = []
    for filename in os.listdir("impacts_model/data/tasks"):
        tasks_template.append(task_template_factory(filename))
    return tasks_template


def task_template_factory(name: str) -> TaskTemplate:
    name = name.replace(".yaml", "")
    with open("impacts_model/data/tasks/" + name + ".yaml", "r") as stream:
        data_loaded = yaml.safe_load(stream)

        resources_list = []
        if data_loaded["resources"] is not None:
            for resource_name in data_loaded["resources"]:
                resources_list.append(resource_template_factory(resource_name))

        subtasks_list = []
        if data_loaded["subtasks"] is not None:
            for resource_name in data_loaded["subtasks"]:
                subtasks_list.append(task_template_factory(resource_name))

        return TaskTemplate(
            name=data_loaded["name"], resources=resources_list, subtasks=subtasks_list
        )


################
# ResourceTemplate #
################
class ResourceTemplate:
    def __init__(self, name: str, impacts: List[ImpactSource]):
        self.name = name
        self.impacts = impacts


def resource_template_factory(name: str) -> ResourceTemplate:
    name = name.replace(".yaml", "")
    with open("impacts_model/data/resources/" + name + ".yaml", "r") as stream:
        data_loaded = yaml.safe_load(stream)

        impacts_list = []
        for impact_name in data_loaded["impact_factors"]:
            impacts_list.append(impact_source_factory(impact_name))

        return ResourceTemplate(name=data_loaded["name"], impacts=impacts_list)


def load_resource_impacts(name: str) -> List[ImpactSource]:
    name = name.replace(".yaml", "")
    with open("impacts_model/data/resources/" + name + ".yaml", "r") as stream:
        data_loaded = yaml.safe_load(stream)
        impacts_list = []
        for impact_name in data_loaded["impact_factors"]:
            impacts_list.append(impact_source_factory(impact_name))
        return impacts_list
