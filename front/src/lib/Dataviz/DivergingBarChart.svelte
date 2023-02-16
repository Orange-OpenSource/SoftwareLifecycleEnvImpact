<script lang="ts">
	import { onMount } from 'svelte';
	import * as d3 from 'd3';
	import { exportSvg } from '$lib/utils';
	import { select } from 'd3';
	import type { D3JsDivergingData } from './d3js';

	export let chartData: D3JsDivergingData[];

	let absolute = true;

	let groupedBarChartSVG: SVGSVGElement;

	let width = 640,
		height = 0,
		marginTop = 30,
		marginRight = 10,
		marginBottom = 30,
		marginLeft = 65;

	function drawDivergingBar() {
		if (chartData && chartData.length > 0) {
			console.log('chartData', chartData);
			//Define functions
			const xFunction = absolute ? (d: D3JsDivergingData) => d.second - d.first : (d: D3JsDivergingData) => d.second / d.first - 1;

			// Compute values
			const X = d3.map(chartData, xFunction);
			const Y = d3.map(chartData, (d) => d.name);

			// Compute default domains
			let xDomain = d3.extent(X);
			// Sort y domain
			let yDomain = d3.groupSort(
				chartData,
				([d]) => d.second - d.first,
				(d) => d.name
			);
			// Unique values in Y Domain
			yDomain = new d3.InternSet(yDomain);

			// Omit any data not present in the y-domain.
			const I = d3.range(X.length).filter((i) => yDomain.has(Y[i]));

			// Create color scale
			const colors = d3.schemeRdBu[3];

			// Compute the default height.
			const yPadding = 0.1; // amount of y-range to reserve to separate bars
			height = Math.ceil((yDomain.size + yPadding) * 25) + marginTop + marginBottom;

			// Define ranges [xMin, xMax]
			let xRange = [marginLeft, width - marginRight]; // [left, right]
			let yRange = [marginTop, height - marginBottom];

			// Construct scales, axes
			let xFormat = absolute ? '+,d' : '+%';
			const xScale = d3.scaleLinear(xDomain, xRange);
			const yScale = d3.scaleBand(yDomain, yRange).padding(yPadding);
			const xAxis = d3.axisTop(xScale).ticks(width / 80, xFormat);
			const yAxis = d3.axisLeft(yScale).tickSize(0).tickPadding(6);

			// Compute titles.
			const format = xScale.tickFormat(100, xFormat);
			let title = (i) => `${Y[i]}\n${format(X[i])}`;

			// Function to align text left or right
			const textAlignement = d3.rollup(
				I,
				([i]) => X[i],
				(i) => Y[i]
			);

			// Create SVG
			const svg = select(groupedBarChartSVG);
			let xLabel = 'tons CO2e';

			svg
				.append('g')
				.attr('transform', `translate(0,${marginTop})`)
				.call(xAxis)
				.call((g) => g.select('.domain').remove())
				.call((g) =>
					g
						.selectAll('.tick line')
						.clone()
						.attr('y2', height - marginTop - marginBottom)
						.attr('stroke-opacity', 0.1)
				)
				.call((g) =>
					g
						.append('text')
						.attr('x', xScale(0))
						.attr('y', -(marginTop-20))
						.attr('fill', 'currentColor')
						.attr('text-anchor', 'center')
						.text(xLabel)
				);

			const bar = svg
				.append('g')
				.selectAll('rect')
				.data(I)
				.join('rect')
				.attr('fill', (i) => colors[X[i] < 0 ? colors.length - 1 : 0])
				.attr('x', (i) => Math.min(xScale(0), xScale(X[i])))
				.attr('y', (i) => yScale(Y[i]))
				.attr('width', (i) => Math.abs(xScale(X[i]) - xScale(0)))
				.attr('height', yScale.bandwidth());

			if (title) bar.append('title').text(title);

			svg
				.append('g')
				.attr('text-anchor', 'end')
				.attr('font-family', 'sans-serif')
				.attr('font-size', 10)
				.selectAll('text')
				.data(I)
				.join('text')
				.attr('text-anchor', (i) => (X[i] < 0 ? 'end' : 'start'))
				.attr('x', (i) => xScale(X[i]) + Math.sign(X[i] - 0) * 4)
				.attr('y', (i) => yScale(Y[i]) + yScale.bandwidth() / 2)
				.attr('dy', '0.35em')
				.text((i) => format(X[i]));

			svg
				.append('g')
				.attr('transform', `translate(${xScale(0)},0)`)
				.call(yAxis)
				.call((g) =>
					g
						.selectAll('.tick text')
						.filter((y) => textAlignement.get(y) < 0)
						.attr('text-anchor', 'start')
						.attr('x', 6)
				);
		}
	}
	function exportGroupedBarChart() {
		exportSvg(groupedBarChartSVG.outerHTML, 'groupedBarChart');
	}

	onMount(function () {
		drawDivergingBar();
	});
</script>

<svg bind:this={groupedBarChartSVG} viewBox="0 0 {width + marginLeft + marginRight} {height + marginBottom + marginTop}" preserveAspectRatio="xMidYMid meet" />
<div class="d-flex justify-content-end">
	<button class="btn btn-outline-primary" on:click|stopPropagation={exportGroupedBarChart} type="button">Export</button>
</div>
