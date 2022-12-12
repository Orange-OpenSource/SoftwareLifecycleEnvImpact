<script lang="ts">
	import { onMount } from 'svelte';
	import { select } from 'd3-selection';
	import { sankey, sankeyLinkHorizontal } from 'd3-sankey';
	import { rgb, scaleOrdinal, schemeSet3, map, gray } from 'd3';

	let sankeySVG: SVGSVGElement;

	var margin = { top: 10, right: 10, bottom: 10, left: 10 },
		width = 500 - margin.left - margin.right,
		height = 480 - margin.top - margin.bottom;

	const nodeWidth = 25;
	const nodePadding = 290;

	let data = {
		nodes: [
			{ node: 0, name: 'node0' },
			{ node: 1, name: 'node1' },
			{ node: 2, name: 'node2' },
			{ node: 3, name: 'node3' },
			{ node: 4, name: 'node4' }
		],
		links: [
			{ source: 0, target: 2, value: 2 },
			{ source: 1, target: 2, value: 2 },
			{ source: 1, target: 3, value: 2 },
			{ source: 0, target: 4, value: 2 },
			{ source: 2, target: 3, value: 2 },
			{ source: 2, target: 4, value: 2 },
			{ source: 3, target: 4, value: 4 }
		]
	};

	async function drawSankey() {
		// Construct svg attributes
		const vis = select(sankeySVG).append('g').attr('id', 'container').attr('transform', `translate(${margin.left}, ${margin.top})`);

		// Define color scale
		var color = scaleOrdinal(schemeSet3);

		// Set the sankey diagram properties
		var svgSankey = sankey()
			.nodeWidth(nodeWidth) // width of node rects
			.nodePadding(nodePadding) // vertical separation between adjacent nodes
			.size([width, height]);

		// Construct with data
		svgSankey(data);

		// add in the links
		var link = vis
			.append('g')
			.selectAll('.link')
			.data(data.links) // TODO HOVER
			.enter()
			.append('path')
			.attr('fill', 'none')
			.attr('stroke', '#000')
			.attr('stroke-opacity', 0.2)
			.attr('d', sankeyLinkHorizontal())
			.style('stroke-width', function (d) {
				return Math.max(1, d.width);
			})
			.sort(function (a, b) {
				console.log(a);
				return b.dy - a.dy;
			});

		// add in the nodes
		var node = vis
			.append('g')
			.selectAll('.node')
			.data(data.nodes)
			.enter()
			.append('g')
			.attr('class', 'node')
			.attr('transform', function (d) {
				return 'translate(' + d.x0 + ',' + d.y0 + ')';
			})

		// add the rectangles for the nodes
		node
			.append('rect')
			.attr('height', function (d) {
				return d.y0;
			})
			.attr('width', nodeWidth)
			.style('fill', function (d) {
				console.log(d.name);
				return color(d.name);
			})
			.style('stroke', function (d) {
				return color(d.name);
			});

		// add in the title for the nodes
		node
			.append('text')
			.attr('x', -6)
			.attr('y', function (d) {
				return d.width / 2;
			})
			.attr('dy', '.35em')
			.attr('text-anchor', 'end')
			.attr('transform', null)
			.text(function (d) {
				return d.name;
			})
			.filter(function (d) {
				return d.x < width / 2;
			})
			.attr('x', 6 + nodeWidth)
			.attr('text-anchor', 'start');
	}

	onMount(function () {
		drawSankey();
	});
</script>

<div>
	<svg bind:this={sankeySVG} viewBox="0 0 {width + margin.left + margin.right} {height + margin.left + margin.right}" preserveAspectRatio="xMidYMid meet" />
</div>
