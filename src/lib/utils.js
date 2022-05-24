/**
 * Returns the last updated date (or creation date if null).
 *
 * @param model the model with `created_at` and `updated_at` fields.
 * @returns 	the date under format : DD/MM/YYYY XX:XX
 */
 export function getLastUpdate(model) {
	let date;

	if (model.updated_at) {
		date = new Date(model.updated_at);
	} else {
		date = new Date(model.created_at);
	}

	return (
		(date.getDate() < 10 ? '0' : '') +
		date.getDate() +
		'/' +
		(date.getMonth() + 1 < 10 ? '0' : '') +
		(date.getMonth() + 1) +
		'/' +
		date.getFullYear() +
		' ' +
		(date.getHours() + 2) +
		':' +
		(date.getMinutes() < 10 ? '0' : '') +
		date.getMinutes()
	);
}

/**
 * Returns the creation date.
 *
 * @param ISODate 	the date in ISO format.
 * @returns 		the date under format : DD/MM/YYYY XX:XX
 */
export function getCreationDate(ISODate) {
	let date = new Date(ISODate);

	return (
		(date.getDate() < 10 ? '0' : '') +
		date.getDate() +
		'/' +
		(date.getMonth() + 1 < 10 ? '0' : '') +
		(date.getMonth() + 1) +
		'/' +
		date.getFullYear() +
		' ' +
		(date.getHours() + 2) +
		':' +
		(date.getMinutes() < 10 ? '0' : '') +
		date.getMinutes()
	);
}

import { Chart } from 'chart.js';

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

import Split from 'split.js';

/**
 * Returns a Split object with 3 rows (for the main page with "My models" / Treeview / "Impact by task")
 *
 * @param document 	the html Document() object
 * @returns 		Split object
 */
export function get3RowsSplitObject(document) {
	return Split(['#split-0', '#split-1', '#split-2'], {
		sizes: [25, 50, 25],
		minSize: 0,
		snapOffset: 150,
		onDrag: function () {
			for (let i = 0; i < 3; i++) {
				let element = document.getElementById('split-' + i);
				if (element.offsetWidth === 0) {
					element.style.visibility = 'hidden';
				} else {
					element.style.visibility = 'visible';
				}
			}
		}
	});
}

/**
 * Returns a Split object with 2 rows (for the compare page with "My models" / "Differences")
 *
 * @param document 	the html Document() object
 * @returns 		Split object
 */
export function get2RowsSplitObject(document) {
	return Split(['#split-0', '#split-1'], {
		sizes: [25, 75],
		minSize: 0,
		snapOffset: 150,
		onDrag: function () {
			for (let i = 0; i < 2; i++) {
				let element = document.getElementById('split-' + i);
				if (element.offsetWidth === 0) {
					element.style.visibility = 'hidden';
				} else {
					element.style.visibility = 'visible';
				}
			}
		}
	});
}
