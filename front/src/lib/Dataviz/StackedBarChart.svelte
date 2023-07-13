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
	import type { D3JStackedData } from './d3js';
	import { exportSvg } from '$lib/utils';

	export let chartData: D3JStackedData[];

	let stackedBarChartSVG: SVGSVGElement;

	let width = 600,
		height = 400,
		marginTop = 0,
		marginRight = 10,
		marginBottom = 10,
		marginLeft = 0;

	const legendLineHeight = 30;
	const legendHeight = legendLineHeight * 3;

	function drawStackedBar() {
		if (chartData && chartData.length > 0) {
			// Compute values
			const X = d3.map(chartData, (d) => d.impactCategory);
			const Y = d3.map(chartData, (d) => d.value);
			const Z = d3.map(chartData, (d) => d.category);

			// Compute default x- and z-domains, and unique them
			const xDomain = new d3.InternSet(X);
			const zDomain = new d3.InternSet(Array.from(d3.union(Z))); // Unique category names

			// Create color scale
			const colorScheme: Function = d3.scaleOrdinal().domain(zDomain).range(d3.schemeSet3);
			const colors: Array<String> = [];
			zDomain.forEach((value) => {
				// Correct a problem where weren't enough colors in the scheme
				colors.push(colorScheme(value));
			});

			// Omit any data not present in the x- and z-domains.
			const I = d3.range(Y.length).filter((i) => xDomain.has(X[i]) && zDomain.has(Z[i]));

			// Define spece required for legends
			const topLegendHeight = 100;
			const leftLegendWidth = 40;

			// Define ranges [xMin, xMax]
			const xRange = [leftLegendWidth, width - marginRight];
			const yRange = [topLegendHeight, height - marginBottom];
			// [marginTop, width + marginLeft - marginRight]

			// Compute a nested array of series where each series is [[x1, x2], [x1, x2],
			// [x1, x2], …] representing the x-extent of each stacked rect. In addition,
			// each tuple has an i (index) property so that we can refer back to the
			// original data point (data[i]). This code assumes that there is only one
			// data point for a given unique y- and z-value.
			const series = d3
				.stack()
				.keys(zDomain)
				.value(([, I], z) => Y[I.get(z)])
				.order(d3.stackOrderNone)
				.offset(d3.stackOffsetExpand)(
					d3.rollup(
						I,
						([i]) => i,
						(i) => X[i],
						(i) => Z[i]
					)
				)
				.map((s) => s.map((d) => Object.assign(d, { i: d.data[1].get(s.key) })));

			// Compute the default y-domain. Note: diverging stacks can be negative.
			let yDomain = d3.extent(series.flat(2));

			// Construct scales, axes, and formats.
			const yScale = d3.scaleLinear(yDomain, yRange);
			const xScale = d3.scaleBand(xDomain, xRange).paddingInner(0.2);
			const color = d3.scaleOrdinal(zDomain, colors);
			const yAxis = d3.axisLeft(yScale).ticks(width / 80, '%'); // LEFT
			const xAxis = d3.axisTop(xScale).tickSizeOuter(0); // TOP

			// Create SVG
			const svg = select(stackedBarChartSVG);

			const maxBarWidth = 75;

			// Create bars
			const bar = svg
				.append('g')
				.selectAll('g')
				.data(series)
				.join('g')
				.attr('fill', ([{ i }]) => color(Z[i]))
				.selectAll('rect')
				.data((d) => d)
				.join('rect')
				.attr('x', ({ i }) => xScale(X[i]))
				.attr('y', ([y1, y2]) => Math.min(yScale(y1), yScale(y2)))
				.attr('width', Math.min(xScale.bandwidth(), maxBarWidth)) // ICI WIDTH
				.attr('height', ([y1, y2]) => Math.abs(yScale(y1) - yScale(y2)))
				.append('title') // Node hover text
				.text(function (d) {
					return Z[d.i] + ': ' + Y[d.i];
				});
			// .text((d) => Math.round(d.value * 100) / 100 + ' kgCO2e');

			// Add upper legend
			svg
				.append('g')
				.attr('transform', `translate(0,${topLegendHeight})`)
				.call(xAxis)
				.call((g) => g.select('.domain').remove())
				.selectAll('text')
				.attr('x', 5)
				.style('text-anchor', 'start')
				.attr('transform', 'rotate(-60)');

			// Add left legend
			svg.append('g').attr('transform', `translate(${leftLegendWidth},0)`).call(yAxis);

			// Add legend under
			const legendTextMargin = 15;
			const bottomLegendMargin = 10;

			var legend = svg
				.append('g')
				.attr('class', 'legend')
				.attr('transform', 'translate(' + (marginLeft + 12) + ',' + height + ')');

			// Colored squares
			legend
				.selectAll('rect')
				.data(series)
				.enter()
				.append('rect')
				.attr('x', function (d, i) {
					if (series.length < 5) {
						// Legend fits on one row
						return i * (width / 4);
					} else {
						// If not, do not display more than three rows
						if (i < 3) return 0;
						if (i < 6) return width / 4;
						if (i < 9) return width / 2;
						return width - width / 4;
					}
				})
				.attr('y', function (d, i) {
					if (series.length < 5) {
						return legendLineHeight;
					} else {
						// If not, do not display more than three rows
						return bottomLegendMargin + (i % 3) * legendLineHeight;
					}
				})
				.attr('width', 12)
				.attr('height', 12)
				.attr('fill', ([{ i }]) => color(Z[i]));

			// Text legend
			legend
				.selectAll('text')
				.data(series)
				.enter()
				.append('text')
				.text(function (d, i) {
					return [...zDomain][i]; // Legend label
				})
				.attr('x', function (d, i) {
					if (series.length < 5) {
						// Legend fits on one row
						return marginLeft + i * (width / 4) + legendTextMargin;
					} else {
						// If not, do not display more than three rows
						if (i < 3) return 0 + legendTextMargin;
						if (i < 6) return width / 4 + legendTextMargin;
						if (i < 9) return width / 2 + legendTextMargin;
						return width - width / 4 + legendTextMargin;
					}
				})
				.attr('y', function (d, i) {
					if (series.length < 5) {
						return legendLineHeight + 11;
					} else {
						// If not, do not display more than three rows
						return bottomLegendMargin + 11 + (i % 3) * legendLineHeight;
					}
				})
				.attr('text-anchor', 'start')
				.attr('alignment-baseline', 'hanging');
		}
	}

	function exportStackedBar() {
		exportSvg(stackedBarChartSVG.outerHTML, 'stackedBarChart');
	}

	onMount(function () {
		drawStackedBar();
	});
</script>

{#if chartData && chartData.length > 0}
	<svg bind:this={stackedBarChartSVG} viewBox="0 0 {width + marginLeft + marginRight} {height + legendHeight + marginBottom + marginTop}" preserveAspectRatio="xMidYMid meet" />
	<div class="d-flex justify-content-end">
		<button class="btn btn-outline-primary" on:click|stopPropagation={exportStackedBar} type="button">Export</button>
	</div>
{/if}
