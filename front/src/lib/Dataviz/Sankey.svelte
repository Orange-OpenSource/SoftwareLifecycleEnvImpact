<!-- BSD 3-Clause License

Copyright (c) 2017, Orange
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { select } from 'd3-selection';
	import * as d3Sankey from 'd3-sankey';
	import * as d3 from 'd3';
	import type { D3JSLink } from './d3js';
	import { exportSvg } from '$lib/utils';

	/*Bound var*/
	export let links: D3JSLink[];
	$: links, drawSankey();

	let width = 1000,
		height = 500,
		marginTop = 5,
		marginRight = 5,
		marginBottom = 5,
		marginLeft = 5;

	let sankeySVG: SVGSVGElement;

	function drawSankey() {
		if (links && links.length > 0) {
			// Clear data for redraw
			select(sankeySVG).selectAll('*').remove();

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
				.text((d) => d.id + ' (' + Math.round(d.value * 100) / 100 + ')');

			// Create link object
			const link = svg
				.append('g')
				.attr('fill', 'none')
				.attr('stroke-opacity', 0.5)
				.selectAll('g')
				.data(links)
				.join('g')
				.style('mix-blend-mode', 'normal')
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
				.attr('stroke-width', (d) => Math.max(0.1, d.width))
				.append('title') // Node hover text
				.text((d) => Math.round(d.value * 100) / 100 + ' kgCO2e');
		}
	}

	function exportSankey() {
		exportSvg(sankeySVG.outerHTML, 'sankey');
	}

	onMount(function () {
		drawSankey();
	});
</script>

{#if links && links.length > 0}
	<svg bind:this={sankeySVG} viewBox="0 0 {width + marginLeft + marginRight} {height + marginBottom + marginTop}" preserveAspectRatio="xMidYMid meet" />
	<div class="d-flex justify-content-end">
		<button class="btn btn-outline-primary" on:click|stopPropagation={exportSankey} type="button">Export</button>
	</div>
{/if}
