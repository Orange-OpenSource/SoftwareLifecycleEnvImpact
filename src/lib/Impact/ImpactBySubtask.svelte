<script>
    import { onMount } from 'svelte';
	import { Chart, registerables } from 'chart.js';

    export let impactBySubtask;

    /* Var needed for chartjs */
	let labels = [];
	let data = [];
	let ctx;
	let myChart;

    $: impactBySubtask, updateChart()

    async function updateChart(){
        if(impactBySubtask != undefined){
            labels = []
            data = []

            for (const item of impactBySubtask){
                if(item.task.name != undefined && item.task_impact.CLIMATE_CHANGE != undefined){
                    labels.push(item.task.name)
                    let quantity = item.task_impact.CLIMATE_CHANGE.replace(" kg_co2e","")
                    data.push(quantity)
                }
            }

            myChart.data.labels = labels;
            myChart.data.datasets[0].data = data;
            myChart.update();
        }
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

		ctx = document.getElementById('myChart').getContext('2d'); /*TODO investigate*/
		myChart = getChart(ctx, labels, data);
	});
</script>

    <h5>By subtask</h5>

    <div>
        <canvas id="myChart" width="400" height="400" />
    </div>

