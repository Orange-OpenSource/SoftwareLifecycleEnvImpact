<script lang="ts">
	import { onMount } from 'svelte';
	import { select } from 'd3-selection';
	import * as d3 from 'd3';
	import { exportSvg } from '$lib/utils';
	import type { D3JGroupedData } from './d3js';

	export let chartData: D3JGroupedData[];

	let groupedBarChartSVG: SVGSVGElement;

	let width = 640,
		height = 400,
		marginTop = 30,
		marginRight = 0,
		marginBottom = 30,
		marginLeft = 65;

	function drawGroupedBar() {
		if (chartData && chartData.length > 0) {
			// Compute values
			const X = d3.map(chartData, (d) => d.resourceName);
			const Y = d3.map(chartData, (d) => d.value);
			const Z = d3.map(chartData, (d) => d.modelName);

			// Compute default domains, and unique them
			const xDomain = new d3.InternSet(X);
			const yDomain = [0, d3.max(Y)]; // [ymin, ymax]
			const zDomain = new d3.InternSet(Z);

			// Omit any data not present in the x- and z-domain.
			const I = d3.range(Y.length).filter((i) => xDomain.has(X[i]) && zDomain.has(Z[i]));

			// Create color scale
			const colors = d3.schemeSet2; // array of colors

			// Define ranges [xMin, xMax]
			const xRange = [marginLeft, width - marginRight];
			const yRange = [height - marginBottom, marginTop];

			// Construct scales, axes, and formats
			const xScale = d3.scaleBand(xDomain, xRange).paddingInner(0.5);
			const xzScale = d3.scaleBand(zDomain, [0, xScale.bandwidth()]).padding(0.05);
			const yScale = d3.scaleLinear(yDomain, yRange);
			const zScale = d3.scaleOrdinal(zDomain, colors);
			const xAxis = d3.axisBottom(xScale).tickSizeOuter(0);
			const yAxis = d3.axisLeft(yScale).ticks(height / 60);

			// Compute titles.
			const formatValue = yScale.tickFormat(100);
			const title = (i) => `${X[i]}\n${Z[i]}\n${formatValue(Y[i])}`;

			// Create SVG
			const svg = select(groupedBarChartSVG);

			svg
				.append('g')
				.attr('transform', `translate(${marginLeft},0)`)
				.call(yAxis)
				.call((g) => g.select('.domain').remove())
				.call((g) =>
					g
						.selectAll('.tick line')
						.clone()
						.attr('x2', width - marginLeft - marginRight)
						.attr('stroke-opacity', 0.1)
				);
			// .call((g) => g.append('text').attr('x', -marginLeft).attr('y', 10).attr('fill', 'currentColor').attr('text-anchor', 'start').text(yLabel));

			const bar = svg
				.append('g')
				.selectAll('rect')
				.data(I)
				.join('rect')
				.attr('x', (i) => xScale(X[i]) + xzScale(Z[i]))
				.attr('y', (i) => yScale(Y[i]))
				.attr('width', xzScale.bandwidth())
				.attr('height', (i) => yScale(0) - yScale(Y[i]))
				.attr('fill', (i) => zScale(Z[i]));

			if (title) bar.append('title').text(title);

			// Add upper legend
			svg
				.append('g')
				.attr('transform', `translate(0,${height - marginBottom})`)
				.call(xAxis)
				.call((g) => g.select('.domain').remove())
				.selectAll('text')
				// .attr('x', 0)
				// .attr('y', 0)
				.style('text-anchor', 'end')
				.attr('transform', 'rotate(-45)');
		}
	}

	function exportGroupedBarChart() {
		exportSvg(groupedBarChartSVG.outerHTML, 'groupedBarChart');
	}

	onMount(function () {
		drawGroupedBar();
	});
</script>

<svg bind:this={groupedBarChartSVG} viewBox="0 0 {width + marginLeft + marginRight} {height + marginBottom + marginTop}" preserveAspectRatio="xMidYMid meet" />
<div class="d-flex justify-content-end">
	<button class="btn btn-outline-primary" on:click|stopPropagation={exportGroupedBarChart} type="button">Export</button>
</div>
