from __future__ import annotations

import os
from typing import List

import yaml

from impacts_model.impact_sources import impact_source_factory, ImpactSource


################
# ResourceTemplate #
################
class ResourceTemplate:
    def __init__(self, name: str):
        self.name = name
        self.impacts = self._load_impacts()

    def _load_impacts(self) -> List[ImpactSource]:
        name = self.name.replace(".yaml", "")
        with open("impacts_model/data/resources/" + name + ".yaml", "r") as stream:
            data_loaded = yaml.safe_load(stream)
            impacts_list = []
            for impact_name in data_loaded["impact_factors"]:
                impacts_list.append(impact_source_factory(impact_name))
            return impacts_list


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
        self.name = name
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


def get_tasks_templates() -> List[TaskTemplate]:
    tasks_template = []
    for filename in os.listdir("impacts_model/data/tasks"):
        tasks_template.append(TaskTemplate(filename))
    return tasks_template


"""
def resource_template_factory(name: str) -> ResourceTemplate:
    name = name.replace(".yaml", "")
    with open("impacts_model/data/resources/" + name + ".yaml", "r") as stream:
        data_loaded = yaml.safe_load(stream)

        impacts_list = []
        for impact_name in data_loaded["impact_factors"]:
            impacts_list.append(impact_source_factory(impact_name))

        return ResourceTemplate(name=data_loaded["name"], impacts=impacts_list)


def load_resource_impacts_source(name: str) -> List[ImpactSource]:
    name = name.replace(".yaml", "")
    with open("impacts_model/data/resources/" + name + ".yaml", "r") as stream:
        data_loaded = yaml.safe_load(stream)
        impacts_list = []
        for impact_name in data_loaded["impact_factors"]:
            impacts_list.append(impact_source_factory(impact_name))
        return impacts_list
"""
