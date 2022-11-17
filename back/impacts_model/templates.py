from __future__ import annotations

import os
from typing import List, Optional

import yaml
from marshmallow import fields, Schema

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
    ):
        """
        Define a task with a name, resources and subtasks
        :param name: the name of the resource
        """
        self.name = name.replace(".yaml", "")
        file_res = self._load_file()
        self.id = file_res[0]
        self.impact_sources = file_res[1]
        self.subtasks = file_res[2]

    def _load_file(self):
        name = self.name.replace(".yaml", "")
        with open("impacts_model/data/tasks/" + name + ".yaml", "r") as stream:
            data_loaded = yaml.safe_load(stream)

            impact_sources = []
            if data_loaded["impact_sources"] is not None:
                for impact_source in data_loaded["impact_sources"]:
                    impact_sources.append(impact_source)

            subtasks_list = []
            if data_loaded["subtasks"] is not None:
                for subtask_name in data_loaded["subtasks"]:
                    subtasks_list.append(TaskTemplate(subtask_name))

            return data_loaded["id"], impact_sources, subtasks_list


class TaskTemplateSchema(Schema):
    """Marshmallow schema to serialize a TaskTemplate object"""

    id = fields.Integer()
    name = fields.String()
    impact_sources = fields.String(many=True)
    subtasks = fields.Nested("TaskTemplateSchema", many=True)


def load_tasks_templates() -> List[TaskTemplate]:
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
    return next((x for x in load_tasks_templates() if x.id == template_id), None)
