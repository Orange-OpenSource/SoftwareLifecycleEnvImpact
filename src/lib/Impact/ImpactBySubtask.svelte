<script lang="ts">
	import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';
	import type { Task } from 'src/model/task';
	import type { SubtasksImpact } from 'src/model/taskImpact';

	export let impactBySubtask: SubtasksImpact;

	/*Bound var*/
	export let selectedTask: Task;

	let chart: Chart;
	let pieCanvas: HTMLCanvasElement;
	let chartLabels: string[] = []; /*chartjs require a separated array of labels*/
	let chartData: any[] = [];

	$: impactBySubtask, updateChart();

	function updateChart() {
		if (chart != undefined && impactBySubtask != undefined && selectedTask != undefined) {
			/*Clear chart data*/
			chartLabels = [];
			chartData = [];

			for (const [task_id, impact] of Object.entries(impactBySubtask)) {
				/*Retrieve task object from its id*/
				let task = selectedTask.subtasks.find((s) => s.id == Number(task_id))!;

				chartLabels.push(task.name);
				if (impact['Climate change'] != undefined) {
					/**For each task push it with its associated impact*/
					chartData.push({
						task: task,
						impact: impact['Climate change'].value
					});
				}
			}

			/*Redundant assignement for chartjs to see the updates*/
			chart.data.labels = chartLabels;
			chart.data.datasets[0].data = chartData;
			chart.update();
		}
	}

	onMount(function () {
		/*Chart config*/
		Chart.register(...registerables);
		let ctx = pieCanvas.getContext('2d')!;
		chart = new Chart(ctx, {
			type: 'pie',
			data: {
				labels: chartLabels,
				datasets: [
					{
						data: chartData,
						backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(153, 102, 255)', 'rgb(75, 192, 192)'],
						hoverOffset: 4
					}
				]
			},
			options: {
				onClick: function (_, item) {
					if (item[0]) {
						/*Click on pie part select corresponding task*/
						selectedTask = chartData[item[0].index].task;
					}
				},
				parsing: {
					/*using property impact of object to get co2 to display*/
					key: 'impact'
				}
			}
		});
		updateChart()
	});
</script>

<div>
	<canvas bind:this={pieCanvas} id="myChart" width="400" height="400" />
</div>
