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
	import { scaleLinear, scaleOrdinal, schemeSet3, treemap, type HierarchyNode } from 'd3';
	import { select } from 'd3-selection';
	import { onMount } from 'svelte';
	import type { D3JSHierarchyNode } from './d3js';

	export let hierarchy: HierarchyNode<D3JSHierarchyNode>;
	$: hierarchy, drawTreeMap();

	let svgElement: SVGSVGElement;

	// set the dimensions and margins of the graph
	const margin = { top: 10, right: 10, bottom: 10, left: 10 },
		width = 445 - margin.left - margin.right,
		height = 445 - margin.top - margin.bottom;

	const titleFontSize = 0.8;
	const valueFontSize = 0.7;

	function drawTreeMap() {
		// Clear data for redraw
		select(svgElement).selectAll('*').remove();

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
