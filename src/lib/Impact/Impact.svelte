<script lang="ts">
    import { onMount } from "svelte";
    import { getChart } from '$lib/utils/chartobj';
	import { Chart, registerables } from 'chart.js';
	import { getModelImpact } from "$lib/controllers/RequestController";

    /*Bound var*/
    export let selectedTask;

    /* Var needed for chartjs */
	let labels: string[] = [];
	let data: any[] = [];
	let ctx: CanvasRenderingContext2D;
	let myChart: Chart;

	/*Update chart when selected task is updated*/
	$: {
		if(selectedTask !== undefined){
			getModelImpact(selectedTask).then(
				res => updateChart(res)
			)
		}
	}


	/**
	 * Update the chart with the new data.
	 */
     async function updateChart(impact) {
		/*
		labels = [];
		data = [];

		let dict: any = {};

		*/
		/* Run recursively through tree to get all task id and their corresponding impact in dictionary */
		/*
		function pushEachTaskAndImpactIntoDict(array: any) {
			dict[array.task.id] = array.environmental_impact;

			for (let i = 0; i < array.subtasks_impacts.length; i++) pushEachTaskAndImpactIntoDict(array.subtasks_impacts[i]);
		}

		pushEachTaskAndImpactIntoDict(impact);

		if (impact.task.subtasks.length) {
			for (let i in impact.task.subtasks) {
				// if the subtask has an impact (some tasks still have empty `environmental_impact` field)
				if (Object.keys(dict[impact.task.subtasks[i].id]).length) {
					let climate_change = dict[impact.task.subtasks[i].id]['Climate change'].split(' ')[0];
					data.push(+climate_change);
					labels.push(impact.task.subtasks[i].name);
				}
			}
		} else {
			// if the task has no subtask (= chart filled with 100% of task)
			if (Object.keys(dict[impact.task.id]).length) {
				let climate_change = dict[impact.task.id]['Climate change'].split(' ')[0];
				data.push(+climate_change);
				labels.push(impact.task.name);
			}
		}

		labels = labels;
		data = data;
		*/
		labels = ["Test 0", "Test 1", "Test 2", "Test 3", ]
		data = [Math.random() * 1000, Math.random() * 1000, Math.random() * 1000, Math.random() * 1000, ]

		myChart.data.labels = labels;
		myChart.data.datasets[0].data = data;
		myChart.update();
	}


    onMount(async function () {
		if (document.querySelector('div.modal-backdrop.fade.show')) document.querySelector('div.modal-backdrop.fade.show')!.remove(); /*TODO what is this ?*/

		Chart.register(...registerables);

		ctx = document.getElementById('myChart').getContext('2d');
		myChart = getChart(ctx, labels, data);
	});

</script>

<div>
    <canvas id="myChart" width="400" height="400" />
</div>