import ipywidgets as widgets
from matplotlib import pyplot as plt

from model.impacts.impacts import ImpactIndicator, ImpactsList
from model.projects import StandardProject
from model.resources import ResourcesList
from model.tasks import TaskImpact

slider_style = {"description_width": "initial"}
slider_width = "400px"


def draw_task(task: TaskImpact) -> None:
    """
    Draw one task as a chart, using TaskImpact format
    :param task: TaskImpact format
    """
    _, ax1 = plt.subplots()
    emissions = [s["impacts"][ImpactIndicator.CLIMATE_CHANGE].magnitude for s in task["subtasks"]]  # type: ignore
    names = [s["name"] for s in task["subtasks"]]  # type: ignore
    ax1.pie(emissions, labels=names)
    ax1.set_title(task["name"])


def draw_tasks(task_impact: TaskImpact) -> None:
    """
    Recursive base to draw all subtasks of a given TaskImpact
    :param task_impact: TaskImpact format
    """
    if task_impact["subtasks"]:
        draw_task(task_impact)
        for subtask in task_impact["subtasks"]:  # type: ignore
            draw_tasks(subtask)  # type: ignore


def draw_resources(resources: ResourcesList) -> None:
    """
    Draw a resourcesList a one chart
    :param resources: ResourcesList to draw
    """
    names = []
    co2 = []

    for r in resources:
        names.append(r)
        co2.append(resources[r][ImpactIndicator.CLIMATE_CHANGE].magnitude)
    _, ax1 = plt.subplots()
    ax1.pie(co2, labels=names)
    ax1.set_title("Resources")


def draw_impacts(impacts_list: ImpactsList) -> None:
    """
    Draw an impact list
    :param impacts_list: the impacts list to draw
    """
    names = []
    impacts = []

    for impact_name in impacts_list:
        names.append(impact_name.value)
        impacts.append(impacts_list[impact_name].magnitude)

    _, ax1 = plt.subplots()
    ax1.pie(impacts, labels=names)
    ax1.set_title("Environmental impacts")


class ModelDisplay:
    """
    Class to dislay a Model on a notebook, both inputs and outputs
    """

    def __init__(self, project: StandardProject) -> None:
        self.inputs = ModelInputs(project)
        self.output = ModelOutput(project, self.inputs)


class ModelInputs:
    """
    Class to display Model inputs
    """

    def __init__(self, p: StandardProject) -> None:
        self.p = p
        self.dev_days_widget = widgets.IntSlider(
            min=0,
            max=3000,
            value=self.p.dev_days,
            description="Dev man-days",
            style=slider_style,
            layout=widgets.Layout(width="400px"),
        )
        self.design_days_widget = widgets.IntSlider(
            min=0,
            max=500,
            value=self.p.design_days,
            description="Design man-days",
            style=slider_style,
            layout=widgets.Layout(width="400px"),
        )
        self.spec_days_widget = widgets.IntSlider(
            min=0,
            max=300,
            value=self.p.spec_days,
            description="Specifications man-days",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )
        self.management_days_widget = widgets.IntSlider(
            min=0,
            max=3000,
            value=self.p.management_days,
            description="Management man-days",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )
        self.maintenance_days_widget = widgets.IntSlider(
            min=0,
            max=1500,
            value=self.p.maintenance_days,
            description="Maintenance man-days",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )
        self.electricity_mix_widget = widgets.FloatSlider(
            min=0,
            max=0.8,
            value=self.p.electricity_mix,
            description="Electricity mix (kg)",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )
        self.pue_widget = widgets.FloatSlider(
            min=1,
            max=2.5,
            value=self.p.pue,
            description="PUE",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )
        self.servers_count_widget = widgets.IntSlider(
            min=0,
            max=50,
            value=self.p.servers_count,
            description="Servers count",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )
        self.storage_tb_widget = widgets.IntSlider(
            min=0,
            max=100,
            value=self.p.storage_size,
            description="Tb reserved",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )
        self.run_duration_widget = widgets.IntSlider(
            min=0,
            max=3000,
            value=self.p.run_duration,
            description="Run days",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )
        self.avg_user_day_widget = widgets.IntSlider(
            min=0,
            max=3000,
            value=self.p.avg_user,
            description="User per day",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )
        self.avg_user_minutes_widget = widgets.IntSlider(
            min=0,
            max=250,
            value=self.p.avg_time,
            description="Average user time(minutes)",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )
        self.avg_user_data_widget = widgets.FloatSlider(
            min=0,
            max=20,
            value=self.p.avg_data,
            description="Average data transferred",
            style=slider_style,
            layout=widgets.Layout(width=slider_width),
        )

    def get_widget(self) -> widgets.HBox:
        """
        Return the hbox containing all the project inputs as sliders
        :return: an HBox with all inputs widgets
        """
        vbox_build = widgets.VBox(
            [
                widgets.Text("Build"),
                self.dev_days_widget,
                self.design_days_widget,
                self.spec_days_widget,
                self.management_days_widget,
                self.maintenance_days_widget,
            ]
        )

        vbox_run = widgets.VBox(
            [
                widgets.Text("Run"),
                self.run_duration_widget,
                self.servers_count_widget,
                self.storage_tb_widget,
                self.avg_user_day_widget,
                self.avg_user_minutes_widget,
                self.avg_user_data_widget,
            ]
        )
        vbox_impacts = widgets.VBox(
            [widgets.Text("Impacts"), self.electricity_mix_widget, self.pue_widget]
        )

        return widgets.HBox([vbox_build, vbox_run, vbox_impacts])


class ModelOutput:
    """
    Ui class to display a StandardProject as pie charts
    """

    def __init__(self, project: StandardProject, inputs: ModelInputs) -> None:
        self.project = project
        self.inputs = inputs

    def _update(
        self,
        dev_days: int,
        design_days: int,
        spec_days: int,
        management_days: int,
        maintenance_days: int,
        electricity_mix: float,
        pue: float,
        servers_count: int,
        storage_tb: int,
        run_duration: int,
        avg_user_day: int,
        avg_user_minutes: int,
        avg_user_data: float,
    ) -> None:
        """
        Helper function to interact widget to update all values and draw again after a change
        """
        self.project.dev_days = dev_days
        self.project.design_days = design_days
        self.project.spec_days = spec_days
        self.project.management_days = management_days
        self.project.maintenance_days = maintenance_days
        self.project.electricity_mix = electricity_mix
        self.project.pue = pue
        self.project.servers_count = servers_count
        self.project.storage_size = storage_tb
        self.project.run_duration = run_duration
        self.project.avg_user = avg_user_day
        self.project.avg_time = avg_user_minutes
        self.project.avg_data = avg_user_data
        draw_resources(self.project.get_impact_by_resource())
        draw_impacts(self.project.get_impacts())
        draw_tasks(self.project.get_impact_by_task())

    def get_widget(self) -> widgets.interactive_output:
        """
        Return an interactive widget with sliders to update the shown pie charts
        :return: an Interactive widget
        """
        return widgets.interactive_output(
            self._update,
            {
                "dev_days": self.inputs.dev_days_widget,
                "design_days": self.inputs.design_days_widget,
                "spec_days": self.inputs.spec_days_widget,
                "management_days": self.inputs.management_days_widget,
                "maintenance_days": self.inputs.maintenance_days_widget,
                "electricity_mix": self.inputs.electricity_mix_widget,
                "pue": self.inputs.pue_widget,
                "servers_count": self.inputs.servers_count_widget,
                "storage_tb": self.inputs.storage_tb_widget,
                "run_duration": self.inputs.run_duration_widget,
                "avg_user_day": self.inputs.avg_user_day_widget,
                "avg_user_minutes": self.inputs.avg_user_minutes_widget,
                "avg_user_data": self.inputs.avg_user_data_widget,
            },
        )
