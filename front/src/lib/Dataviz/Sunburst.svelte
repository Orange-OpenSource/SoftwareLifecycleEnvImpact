<script lang="ts">
	import { onMount } from 'svelte';
	import { select } from 'd3-selection';
	import { arc, scaleOrdinal, partition, type HierarchyNode, schemeSet3, selectAll, quantize, interpolateRainbow, schemeSet2 } from 'd3';
	import type { D3JSNode } from './d3js';
	import type { Task } from '$lib/api/dataModel';

	/*Bound var*/
	export let selectedTask: Task;

	export let hierarchy: HierarchyNode<D3JSNode>;

	let sunburstSVG: SVGSVGElement;
	let legendSVG: SVGSVGElement;

	const margin = { top: 10, right: 10, bottom: 10, left: 10 },
		sunburstWidth = 500 - margin.left - margin.right,
		sunburstHeight = 500 - margin.left - margin.right,
		radius = sunburstHeight / 2;

	let legendHeight = 0;
	const legendLineHeight = 30;

	async function drawSunburst() {
		// Construct svg attributes
		const vis = select(sunburstSVG)
			.append('g')
			.attr('id', 'container')
			.attr('transform', 'translate(' + sunburstWidth / 2 + ',' + sunburstHeight / 2 + ')');

		// Add defs to fill each segment differently
		vis.append('defs').attr('id', 'defs');

		// Add text box middle
		addTextElement(vis);

		// Init the arc
		var svgArc = arc()
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
		var partitionSvg = partition().size([2 * Math.PI, radius * radius]);

		// Adding middle circle
		vis.append('circle').attr('r', radius).style('opacity', 0);

		// Classifying elements
		var root = hierarchy
			.sum((d: D3JSNode) => d.co2)
			.sort(function (a, b) {
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

		// Set legend height in function of node amount
		legendHeight = (root.children ? root.children.length : 1) * legendLineHeight;

		// prepare a color scale
		const color = scaleOrdinal().domain(names).range(schemeSet2);
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

				// TODO ICI
				vis.select('#nameMiddle').text(d.data.name);
				vis.select('#valueMiddle').text(Math.round(d.data.co2 * 100) / 100 + ' kgCO2e');

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

				// Text
				vis.select('#nameMiddle').text('');
				vis.select('#valueMiddle').text('');

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

	function addTextElement(vis) {
		var textGroup = vis.append('g');

		textGroup.append('text').attr('id', 'nameMiddle').attr('y', -50).attr('text-anchor', 'middle').style('font-size', '20px').style('font-weight', 'bold');

		// textGroup.append('text').attr('id', 'type-amount').attr('y', -80).attr('class', 'type-amount').attr('text-anchor', 'middle');
		// textGroup.append('text').attr('id', 'category-amount').attr('y', -60).attr('class', 'category-amount').attr('text-anchor', 'middle');
		textGroup.append('text').attr('id', 'valueMiddle').attr('text-anchor', 'middle').style('font-size', '15px');
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

	onMount(function () {
		drawSunburst();
	});
</script>

<div>
	<!-- <svg width={widthMin} height={heightMin} bind:this={sunburstSVG} /> -->
	<svg bind:this={sunburstSVG} viewBox="0 0 {sunburstWidth + margin.left + margin.right} {sunburstHeight + legendHeight + margin.left + margin.right}" preserveAspectRatio="xMidYMid meet" />
</div>
