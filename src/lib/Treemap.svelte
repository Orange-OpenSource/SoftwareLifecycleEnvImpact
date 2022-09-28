<script lang="ts">
	import { scaleLinear, scaleOrdinal, schemeSet1, schemeSet2, schemeSet3, treemap, type HierarchyNode } from 'd3';
	import { select } from 'd3-selection';
	import { onMount } from 'svelte';

	export let hierarchy: HierarchyNode;

	let svgElement;

	let size = 500;

	async function drawTreeMap() {
		// Give the data to this cluster layout:
		const root = hierarchy.sum((d) => d.value);
		let names: String[] = [];
		root.each(function (node: any) {
			names.push(node.data.name);
		});

		// Then d3.treemap computes the position of each element of the hierarch
		const graph = treemap().size([size, size]).padding(2)(root);

		const svg = select(svgElement);

		svg.html('');

		// prepare a color scale
		const color = scaleOrdinal().domain(names).range(schemeSet3);

		// And a opacity scale
		const opacity = scaleLinear().domain([10, 30]).range([0.5, 1]);

		svg
			.selectAll('rect')
			.data(root.leaves())
			.join('rect')
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
			.style('stroke', 'black')
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
			.attr('x', function (d) {
				return d.x0 + 10;
			}) // +10 to adjust position (more right)
			.attr('y', function (d) {
				return d.y0 + 20;
			}) // +20 to adjust position (lower)
			.text(function (d) {
				return d.data.name;
			})
			.attr('font-size', '19px')
			.attr('fill', 'black');

		// and to add the values
		svg
			.selectAll('vals')
			.data(root.leaves())
			.enter()
			.append('text')
			.attr('x', function (d) {
				return d.x0 + 10;
			}) // +10 to adjust position (more right)
			.attr('y', function (d) {
				return d.y0 + 35;
			}) // +20 to adjust position (lower)
			.text(function (d) {
				return d.data.value;
			})
			.attr('font-size', '11px')
			.attr('fill', 'black');
	}

	onMount(function () {
		drawTreeMap();
	});
</script>

<div>
	<svg width="90%" viewBox="0 0 {size} {size}" bind:this={svgElement} />
</div>
