<script>
    import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';

    export let impactBySubtask;

    /* Var needed for chartjs */
	let labels = [];
	let data = [];
	let ctx;
	let myChart;

    $: impactBySubtask, updateChart2()

    async function updateChart2(){
        if(impactBySubtask != undefined){
            labels = []
            data = []

            for (const item of impactBySubtask){
                console.log("label", item.task.name)
                labels.push(item.task.name)
                let quantity = item.task_impact.CLIMATE_CHANGE.replace(" kg_co2e","")
                data.push(quantity)
            }

            myChart.data.labels = labels;
            myChart.data.datasets[0].data = data;
            myChart.update();
        }
    }


    async function updateChart(impact) {
        labels = ['Test 0', 'Test 1', 'Test 2', 'Test 3'];
        data = [Math.random() * 1000, Math.random() * 1000, Math.random() * 1000, Math.random() * 1000];

        myChart.data.labels = labels;
        myChart.data.datasets[0].data = data;
        myChart.update();
        /*impact = await getModelImpact(selectedTask);*/
        /*TODO route get impacts*/
        

        /*
        labels = [];
        data = [];

        let dict = {};

        */
        /* Run recursively through tree to get all task id and their corresponding impact in dictionary */
        /*
        function pushEachTaskAndImpactIntoDict(array) {
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
	}

    /**
	 * Returns a pie chart filled with `labels` and `data`.
	 *
	 * @param ctx		the canvas context
	 * @param labels 	the labels
	 * @param data		the data
	 * @returns 		the pie Chart object
	 */
	export function getChart(ctx, labels, data) {
		return new Chart(ctx, {
			type: 'pie',
			data: {
				labels: labels,
				datasets: [
					{
						label: 'My First Dataset',
						data: data,
						backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(153, 102, 255)', 'rgb(75, 192, 192)'],
						hoverOffset: 4
					}
				]
			}
		});
	}

	onMount(async function () {
		if (document.querySelector('div.modal-backdrop.fade.show')) document.querySelector('div.modal-backdrop.fade.show').remove(); /*TODO what is this ?*/

		Chart.register(...registerables);

		ctx = document.getElementById('myChart').getContext('2d');
		myChart = getChart(ctx, labels, data);
	});
</script>

    <h5>By subtask</h5>

    <div>
        <canvas id="myChart" width="400" height="400" />
    </div>

