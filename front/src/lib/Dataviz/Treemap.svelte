<script lang="ts">
	import { scaleLinear, scaleOrdinal, schemeSet3, treemap, type HierarchyNode } from 'd3';
	import { select } from 'd3-selection';
	import { onMount } from 'svelte';

	export let hierarchy: HierarchyNode<D3JSNode>;

	let svgElement: SVGSVGElement;

	// set the dimensions and margins of the graph
	const margin = { top: 10, right: 10, bottom: 10, left: 10 },
		width = 445 - margin.left - margin.right,
		height = 445 - margin.top - margin.bottom;

	const titleFontSize = 0.8;
	const valueFontSize = 0.7;

	async function drawTreeMap() {
		// append the svg object to the body of the page
		const svg = select(svgElement).append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

		// Give the data to this cluster layout:
		const root = hierarchy.sum((d: { value: any }) => d.value);

		// Prepare rectangle names
		let names: String[] = [];
		root.each(function (node: any) {
			names.push(node.data.name);
		});

		// prepare a color scale
		const color = scaleOrdinal().domain(names).range(schemeSet3);

		// And a opacity scale
		const opacity = scaleLinear().domain([10, 30]).range([0.5, 1]);

		// computes the position of each element of the hierarchy
		// The coordinates are added to the root object above
		treemap().size([width, height]).padding(4)(root);

		// use this information to add rectangles:
		svg
			.selectAll('rect')
			.data(root.leaves())
			.join('rect')
			.attr('display', function (d) {
				return d.depth ? null : 'none'; // Do not dislay root node
			})
			.attr('x', function (d) {
				return d.x0;
			})
			.attr('y', function (d) {
				return d.y0;
			})
			.attr('width', function (d) {
				return d.x1 - d.x0;
			})
			.attr('height', function (d) {
				return d.y1 - d.y0;
			})
			.style('fill', function (d) {
				return color(d.data.name);
			})
			.style('opacity', function (d) {
				return opacity(d.data.value);
			});

		// and to add the text labels
		svg
			.selectAll('text')
			.data(root.leaves())
			.enter()
			.append('text')
			.attr('display', function (d) {
				return d.depth ? null : 'none'; // Do not dislay root node
			})
			.attr('x', function (d) {
				return d.x0 + 10;
			}) // +10 to adjust position (more right)
			.attr('y', function (d) {
				return d.y0 + 20;
			}) // +20 to adjust position (lower)
			.text(function (d) {
				return d.data.name;
			})
			.attr('font-size', titleFontSize + 'em');

		// and to add the values
		svg
			.selectAll('vals')
			.data(root.leaves())
			.enter()
			.append('text')
			.attr('display', function (d) {
				return d.depth ? null : 'none'; // Do not dislay root node
			})
			.attr('x', function (d) {
				return d.x0 + 10;
			}) // +10 to adjust position (more right)
			.attr('y', function (d) {
				return d.y0 + 35;
			}) // +20 to adjust position (lower)
			.text(function (d) {
				return Math.round(d.data.value * 100) / 100 + ' kgCO2e';
			})
			.attr('font-size', valueFontSize + 'em')
			.attr('fill', 'black');
	}

	onMount(function () {
		drawTreeMap();
	});
</script>

<div>
	<!-- <svg width={width + margin.left + margin.right} height={height + margin.top + margin.bottom} bind:this={svgElement} /> -->
	<svg bind:this={svgElement} viewBox="0 0 {width + margin.left + margin.right} {height + margin.left + margin.right}" preserveAspectRatio="xMidYMid meet" />
</div>
