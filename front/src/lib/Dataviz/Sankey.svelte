<script lang="ts">
	import { onMount } from 'svelte';
	import { select } from 'd3-selection';
	import * as d3Sankey from 'd3-sankey';
	import * as d3 from 'd3';
	import type { D3JSLink } from './d3js';
	import { exportPdf } from '$lib/utils';

	/*Bound var*/
	export let links: D3JSLink[];

	let width = 900,
		height = 450,
		marginTop = 5,
		marginRight = 5,
		marginBottom = 5,
		marginLeft = 5;

	let sankeySVG: SVGSVGElement;

	function drawSankey() {
		if (links && links.length > 0) {
			// Create nodes
			const linksSources = d3.map(links, (d: D3JSLink) => d.source);
			const linksTargets = d3.map(links, (d: D3JSLink) => d.target);

			let nodes = Array.from(d3.union(linksSources, linksTargets), (id) => ({ id }));
			const nodesNames = d3.map(nodes, (d) => d.id);

			// Construct the color scale
			const color = d3.scaleOrdinal(nodesNames, d3.schemeTableau10);

			// Compute the Sankey layout.
			d3Sankey
				.sankey()
				.nodeId((d) => d.id)
				.nodeAlign(d3Sankey.sankeyJustify)
				.nodeWidth(15)
				.nodePadding(10) // vertical separation between adjacent nodes
				.extent([
					[marginLeft, marginTop],
					[width - marginRight, height - marginBottom]
				])({ nodes, links });

			// Unique id to avoid link conflicts
			const uid = `O-${Math.random().toString(16).slice(2)}`;

			// Create SVG
			const svg = select(sankeySVG);

			// Draw nodes
			svg
				.append('g')
				.selectAll('rect')
				.data(nodes)
				.join('rect')
				.attr('x', (d) => d.x0)
				.attr('y', (d) => d.y0)
				.attr('height', (d) => d.y1 - d.y0)
				.attr('width', (d) => d.x1 - d.x0)
				.attr('fill', (d) => color(d.id))
				.on('mouseover', function (d) {
					// Brighter node on hover
					d3.select(this).attr('fill', (d) => d3.rgb(color(d.id)).brighter(0.8).toString());
				})
				.on('mouseout', function (d) {
					// Reset node hover to default color
					d3.select(this).attr('fill', (d) => color(d.id));
				})
				.append('title') // Node hover text
				.text((d) => Math.round(d.value * 100) / 100 + ' kgCO2e');

			// Draw node labels
			svg
				.append('g')
				.attr('font-family', 'sans-serif')
				.attr('font-size', 10)
				.selectAll('text')
				.data(nodes)
				.join('text')
				.attr('x', (d) => (d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6))
				.attr('y', (d) => (d.y1 + d.y0) / 2)
				.attr('dy', '0.35em')
				.attr('text-anchor', (d) => (d.x0 < width / 2 ? 'start' : 'end'))
				.text((d) => d.id);

			// Create link object
			const link = svg
				.append('g')
				.attr('fill', 'none')
				.attr('stroke-opacity', 0.5)
				.selectAll('g')
				.data(links)
				.join('g')
				.style('mix-blend-mode', 'multiply')
				.on('mouseover', function (d) {
					// Darken link on hover
					d3.select(this).style('stroke-opacity', 1);
				})
				.on('mouseout', function (d) {
					// Reset link hover to default color
					d3.select(this).style('stroke-opacity', 0.5);
				});

			// Set links gradiant
			link
				.append('linearGradient')
				.attr('id', (d) => `${uid}-link-${d.index}`)
				.attr('gradientUnits', 'userSpaceOnUse')
				.attr('x1', (d) => d.source.x1)
				.attr('x2', (d) => d.target.x0)
				.call(
					(gradient) =>
						gradient
							.append('stop')
							.attr('offset', '0%')
							.attr('stop-color', (d) => color(d.source.id)) // Start gradient color
				)
				.call(
					(gradient) =>
						gradient
							.append('stop')
							.attr('offset', '100%')
							.attr('stop-color', (d) => color(d.target.id)) // End gradient color
				);

			// Draw links
			link
				.append('path')
				.attr('d', d3Sankey.sankeyLinkHorizontal())
				.attr('stroke', ({ index: i }) => `url(#${uid}-link-${i})`)
				.attr('stroke-width', (d) => Math.max(1, d.width))
				.append('title') // Node hover text
				.text((d) => Math.round(d.value * 100) / 100 + ' kgCO2e');
		}
	}

	function exportSankey() {
		exportPdf(sankeySVG, 'sankey');
	}

	onMount(function () {
		drawSankey();
	});
</script>

<svg bind:this={sankeySVG} viewBox="0 0 {width + marginLeft + marginRight} {height + marginBottom + marginTop}" preserveAspectRatio="xMidYMid meet" />
<div class="d-flex justify-content-end">
	<button class="btn" on:click|stopPropagation={exportSankey} type="button">Export</button>
</div>
