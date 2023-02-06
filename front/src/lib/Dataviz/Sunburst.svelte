<script lang="ts">
	import { onMount } from 'svelte';
	import { select } from 'd3-selection';
	import * as d3 from 'd3';
	import type { D3JSHierarchyNode } from './d3js';
	import type { Task } from '$lib/api/dataModel';
	import { exportSvg } from '$lib/utils';

	/*Bound var*/
	export let selectedTask: Task;

	export let hierarchy: d3.HierarchyNode<D3JSHierarchyNode>;

	let sunburstSVG: SVGSVGElement;
	let legendSVG: SVGSVGElement;

	const margin = { top: 10, right: 10, bottom: 10, left: 10 },
		sunburstWidth = 500 - margin.left - margin.right,
		sunburstHeight = 500 - margin.left - margin.right,
		radius = sunburstHeight / 2;

	let legendHeight = 0;
	const legendLineHeight = 30;

	const legendRequired = selectedTask == undefined;

	async function drawSunburst() {
		if (hierarchy && hierarchy.children && hierarchy.children.length > 0) {
			// Construct svg attributes
			const vis = select(sunburstSVG)
				.append('g')
				.attr('id', 'container')
				.attr('transform', 'translate(' + sunburstWidth / 2 + ',' + sunburstHeight / 2 + ')');

			// Add defs to fill each segment differently
			vis.append('defs').attr('id', 'defs');

			// Init the arc
			var svgArc = d3
				.arc()
				.startAngle(function (d) {
					return d.x0;
				})
				.endAngle(function (d) {
					return d.x1;
				})
				.innerRadius(function (d) {
					return Math.sqrt(d.y0);
				})
				.outerRadius(function (d) {
					return Math.sqrt(d.y1);
				});

			// Partition
			var partitionSvg = d3.partition().size([2 * Math.PI, radius * radius]);

			// Adding middle circle
			vis.append('circle').attr('r', radius).style('opacity', 0);

			// Classifying elements
			var root = hierarchy
				.sum(function (d: D3JSHierarchyNode) {
					// Inputed values already contains the childrens, do not sum twice
					return !d.children || d.children.length === 0 ? d.use + d.manufacture : 0;
				})
				// .sum((d: D3JSHierarchyNode) => (d.manufacture + d.use)d.co2)
				.sort(function (a: d3.HierarchyNode<D3JSHierarchyNode>, b: d3.HierarchyNode<D3JSHierarchyNode>) {
					if (a.depth === 1) {
						return b.value - a.value;
					} else {
						return b.data.name.localeCompare(a.data.name) * -1;
					}
				});

			// Prepare rectangle names
			let names: String[] = [];
			root.each(function (node: any) {
				names.push(node.data.name);
			});
			// Keep the total value, as it ill we be modified as the sum of all nodes later
			const totalValue = root.value;

			// Add text box middle
			addTextElement(vis, totalValue);

			// Set legend height in function of node amount
			// No need for legend if legendRequired is false
			legendHeight = !legendRequired ? 0 : (root.children ? root.children.length : 1) * legendLineHeight;

			// prepare a color scale
			// Different color scale if selected task is defined or not
			const color = d3
				.scaleOrdinal()
				.domain(names)
				.range(selectedTask != undefined ? d3.schemeSet2 : d3.schemeSet3);
			// const color = scaleOrdinal(quantize(interpolateRainbow, names.length + 1))

			// Create nodes
			var nodes = partitionSvg(root)
				.descendants()
				.filter(function (d) {
					return d.x1 - d.x0 > 0.005; // 0.005 radians = 0.29 degrees
				});

			var path = vis
				.selectAll('path')
				.data(nodes)
				.enter()
				.append('path')
				.attr('display', function (d) {
					return d.depth ? null : 'none'; // Do not dislay root node circle
				})
				.attr('d', svgArc)
				.style('fill', (d) => {
					// while (d.depth > 1) d = d.parent;
					return color(d.data.name);
				})
				.on('mouseover', (event, d) => {
					// Select the element

					var sequenceArray = d.ancestors().reverse();
					sequenceArray.shift(); // suppression de la racine

					vis.select('#nameMiddle').text(d.data.name);
					vis.select('#valueMiddle').text(Math.round(d.value * 100) / 100 + ' kgCO2e');

					vis
						.selectAll('path') // Grey all segments
						.style('opacity', 0.6);

					vis
						.selectAll('path') // Ensuite on met en valeur uniquement ceux qui sont ancêtres de la sélection
						.filter(function (node) {
							return sequenceArray.indexOf(node) >= 0;
						})
						.style('opacity', 1);
				})
				.on('mouseleave', (event, d) => {
					// Set back to normal state

					// // Text
					vis.select('#nameMiddle').text('Total');
					vis.select('#valueMiddle').text(Math.round(totalValue * 100) / 100 + ' kgCO2e');

					// Opacity
					vis.selectAll('path').style('opacity', 1);
				})
				.on('click', (event, d) => {
					// Select clicked task
					if (d.data.task != undefined) {
						selectedTask = d.data.task;
					}
				});
			drawLegend(vis, nodes, color);
		}
	}

	function addTextElement(vis, totalValue) {
		var textGroup = vis.append('g');

		textGroup.append('text').attr('id', 'nameMiddle').attr('y', -50).attr('text-anchor', 'middle').style('font-size', '20px').style('font-weight', 'bold').text('Total');

		// textGroup.append('text').attr('id', 'type-amount').attr('y', -80).attr('class', 'type-amount').attr('text-anchor', 'middle');
		// textGroup.append('text').attr('id', 'category-amount').attr('y', -60).attr('class', 'category-amount').attr('text-anchor', 'middle');
		textGroup
			.append('text')
			.attr('id', 'valueMiddle')
			.attr('text-anchor', 'middle')
			.style('font-size', '15px')
			.text(Math.round(totalValue * 100) / 100 + ' kgCO2e');
	}

	function drawLegend(vis, nodes, color) {
		vis
			.selectAll('mydots')
			.data(nodes)
			.enter()
			.append('circle')
			.attr('display', function (d) {
				return d.depth ? null : 'none'; // Do not dislay root node
			})
			.attr('cx', 120)
			.attr('cy', function (d, i) {
				return sunburstWidth / 2 + i * legendLineHeight;
			})
			.attr('r', 7)
			.style('fill', function (d) {
				return color(d.data.name);
			});

		// Add one dot in the legend for each name.
		vis
			.selectAll('mylabels')
			.data(nodes)
			.enter()
			.append('text')
			.attr('display', function (d) {
				return d.depth ? null : 'none'; // Do not dislay ùiddle circle
			})
			.attr('x', 140)
			.attr('y', function (d, i) {
				return sunburstWidth / 2 + i * legendLineHeight + 4;
			})
			.style('fill', function (d) {
				return 'black';
			})
			.text(function (d) {
				return d.data.name;
			});
	}

	function exportSunburst() {
		exportSvg(sunburstSVG.outerHTML, 'sunburst');
	}

	onMount(function () {
		drawSunburst();
	});
</script>

{#if hierarchy && hierarchy.children && hierarchy.children.length > 0}
	<svg bind:this={sunburstSVG} viewBox="0 0 {sunburstWidth + margin.left + margin.right} {sunburstHeight + legendHeight + margin.left + margin.right}" preserveAspectRatio="xMidYMid meet" />
	<div class="d-flex justify-content-end">
		<button class="btn" on:click|stopPropagation={exportSunburst} type="button">Export</button>
	</div>
{/if}
