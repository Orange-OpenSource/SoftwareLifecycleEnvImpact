import importlib
import os

import yaml

from model.impacts.impact_factors import ImpactFactor
from model.resources import Resource
from model.tasks import TaskTemplate


def impact_factory(name: str) -> ImpactFactor:
    module = importlib.import_module("model.impacts.impact_factors")
    class_ = getattr(module, name)
    instance = class_()
    return instance


def resource_factory(name: str) -> Resource:
    name = name.replace(".yaml", "")
    with open("model/res/resources/" + name + ".yaml", "r") as stream:
        data_loaded = yaml.safe_load(stream)
        impacts_list = []
        for impact_name in data_loaded["impact_factors"]:
            impacts_list.append(impact_factory(impact_name))
        return Resource(name=data_loaded["name"], impacts=impacts_list)


def task_template_factory(name: str) -> TaskTemplate:
    name = name.replace(".yaml", "")
    with open("model/res/tasks/" + name + ".yaml", "r") as stream:
        data_loaded = yaml.safe_load(stream)

        resources_list = []
        if data_loaded["resources"] is not None:
            for resource_name in data_loaded["resources"]:
                resources_list.append(resource_factory(resource_name))

        subtasks_list = []
        if data_loaded["subtasks"] is not None:
            for resource_name in data_loaded["subtasks"]:
                subtasks_list.append(task_template_factory(resource_name))

        return TaskTemplate(
            name=data_loaded["name"], resources=resources_list, subtasks=subtasks_list
        )


def get_tasks_templates() -> [TaskTemplate]:
    tasks_template = []
    for filename in os.listdir("model/res/tasks"):
        tasks_template.append(task_template_factory(filename))
    return tasks_template
