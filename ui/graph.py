import ipywidgets as widgets  # type: ignore
from matplotlib import pyplot as plt  # type: ignore

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
    emissions = [s["CO2"] for s in task["subtasks"]]
    names = [s["name"] for s in task["subtasks"]]
    ax1.pie(emissions, labels=names)
    ax1.set_title(task["name"])


def draw_tasks(task_impact: TaskImpact) -> None:
    """
    Recursive base to draw all subtasks of a given TaskImpact
    :param task_impact: TaskImpact format
    """
    if task_impact["subtasks"]:
        draw_task(task_impact)
        for subtask in task_impact["subtasks"]:
            draw_tasks(subtask)


def draw_resources(resources: ResourcesList) -> None:
    """
    Draw a resourcesList a one chart
    :param resources: ResourcesList to draw
    """
    names = []
    co2 = []

    for r in resources:
        names.append(r)
        co2.append(resources[r]["CO2"])
    _, ax1 = plt.subplots()
    ax1.pie(co2, labels=names)
    ax1.set_title("Resources")


class ModelPieChart:
    """
    Ui class to display a StandardProject as pie charts
    """

    def __init__(self, p: StandardProject) -> None:
        self.p = p

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
        self.p.dev_days = dev_days
        self.p.design_days = design_days
        self.p.spec_days = spec_days
        self.p.management_days = management_days
        self.p.maintenance_days = maintenance_days
        self.p.electricity_mix = electricity_mix
        self.p.pue = pue
        self.p.servers_count = servers_count
        self.p.storage_size = storage_tb
        self.p.run_duration = run_duration
        self.p.avg_user = avg_user_day
        self.p.avg_time = avg_user_minutes
        self.p.avg_data = avg_user_data
        draw_resources(self.p.get_impact_by_resource())
        draw_tasks(self.p.get_impact_by_task())

    def get_widget(self) -> widgets.interactive:
        """
        Return an interactive widget with sliders to update the shown pie charts
        :return: an Interactive widget
        """
        return widgets.interactive(
            self._update,
            dev_days=widgets.IntSlider(
                min=0,
                max=3000,
                value=self.p.dev_days,
                description="Dev man-days",
                style=slider_style,
                layout=widgets.Layout(width="400"),
            ),
            design_days=widgets.IntSlider(
                min=0,
                max=500,
                value=self.p.design_days,
                description="Design man-days",
                style=slider_style,
                layout=widgets.Layout(width="400px"),
            ),
            spec_days=widgets.IntSlider(
                min=0,
                max=300,
                value=self.p.spec_days,
                description="Specifications man-days",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
            management_days=widgets.IntSlider(
                min=0,
                max=3000,
                value=self.p.management_days,
                description="Management man-days",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
            maintenance_days=widgets.IntSlider(
                min=0,
                max=1500,
                value=self.p.maintenance_days,
                description="Maintenance man-days",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
            electricity_mix=widgets.FloatSlider(
                min=0,
                max=0.8,
                value=self.p.electricity_mix,
                description="Electricity mix (kg)",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
            pue=widgets.FloatSlider(
                min=1,
                max=2.5,
                value=self.p.pue,
                description="PUE",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
            servers_count=widgets.IntSlider(
                min=0,
                max=50,
                value=self.p.servers_count,
                description="Servers count",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
            storage_tb=widgets.IntSlider(
                min=0,
                max=100,
                value=self.p.storage_size,
                description="Tb reserved",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
            run_duration=widgets.IntSlider(
                min=0,
                max=3000,
                value=self.p.run_duration,
                description="Run days",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
            avg_user_day=widgets.IntSlider(
                min=0,
                max=3000,
                value=self.p.avg_user,
                description="User per day",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
            avg_user_minutes=widgets.IntSlider(
                min=0,
                max=250,
                value=self.p.avg_time,
                description="Average user time(minutes)",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
            avg_user_data=widgets.FloatSlider(
                min=0,
                max=20,
                value=self.p.avg_data,
                description="Average data transferred",
                style=slider_style,
                layout=widgets.Layout(width=slider_width),
            ),
        )
