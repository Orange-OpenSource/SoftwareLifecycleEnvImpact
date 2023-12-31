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
	import * as d3 from 'd3';
	import type { D3JSHierarchyNode } from './d3js';
	import type { Activity } from '$lib/api/dataModel';
	import { exportSvg } from '$lib/utils';

	/*Bound var*/
	export let selectedActivity: Activity;

	export let hierarchy: d3.HierarchyNode<D3JSHierarchyNode>;

	$: hierarchy, drawSunburst();

	let sunburstSVG: SVGSVGElement;

	const margin = { top: 10, right: 10, bottom: 10, left: 10 },
		sunburstWidth = 500 - margin.left - margin.right,
		sunburstHeight = 500 - margin.left - margin.right,
		radius = sunburstHeight / 2;

	async function drawSunburst() {
		if (hierarchy && hierarchy.children && hierarchy.children.length > 0) {
			// Clear data for redraw
			select(sunburstSVG).selectAll('*').remove();

			// Construct svg attributes
			const vis = select(sunburstSVG)
				.append('g')
				.attr('id', 'container')
				.attr('transform', 'translate(' + sunburstWidth / 2 + ',' + sunburstHeight / 2 + ')');
			// vis.selectAll('*').remove();

			// Add defs to fill each segment differently
			vis.append('defs').attr('id', 'defs');

			// Init the arc
			const svgArc = d3
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

			// prepare a color scale
			// Different color scale if selected activity is defined or not
			const color = d3
				.scaleOrdinal()
				.domain(names)
				.range(selectedActivity != undefined ? d3.schemeSet2 : d3.schemeSet3);
			// const color = scaleOrdinal(quantize(interpolateRainbow, names.length + 1))

			// Create nodes
			const nodes = partitionSvg(root)
				.descendants()
				.filter(function (d) {
					return d.x1 - d.x0 > 0.005; // 0.005 radians = 0.29 degrees
				});

			const path = vis
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
					// Select clicked activity
					if (d.data.activity != undefined) {
						selectedActivity = d.data.activity;
					}
				});
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

	function exportSunburst() {
		exportSvg(sunburstSVG.outerHTML, 'sunburst');
	}

	onMount(function () {
		drawSunburst();
	});
</script>

{#if hierarchy && hierarchy.children && hierarchy.children.length > 0}
	<svg bind:this={sunburstSVG} viewBox="0 0 {sunburstWidth + margin.left + margin.right} {sunburstHeight + margin.left + margin.right}" preserveAspectRatio="xMidYMid meet" />
	<div class="d-flex justify-content-end">
		<button class="btn btn-outline-primary" on:click|stopPropagation={exportSunburst} type="button">Export</button>
	</div>
{/if}
