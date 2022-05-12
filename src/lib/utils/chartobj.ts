import { Chart } from 'chart.js';

export function getChart(ctx: any, labels: any, data: any) {
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
