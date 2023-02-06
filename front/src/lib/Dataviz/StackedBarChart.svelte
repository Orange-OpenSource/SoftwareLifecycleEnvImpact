<script lang="ts">
	import { onMount } from 'svelte';
	import { select } from 'd3-selection';
	import * as d3 from 'd3';
	import type { D3JStackedData } from './d3js';
	import { exportSvg } from '$lib/utils';

	export let chartData: D3JStackedData[];

	let stackedBarChartSVG: SVGSVGElement;

	let width = 640,
		height = 400,
		marginTop = 0,
		marginRight = 10,
		marginBottom = 10,
		marginLeft = 0;

	// function drawStackedBar() {
	// 	if (chartData && chartData.length > 0) {
	// 		// Compute values
	// 		const X = d3.map(chartData, (d) => d.value);
	// 		const Y = d3.map(chartData, (d) => d.impactCategory);
	// 		const Z = d3.map(chartData, (d) => d.category);

	// 		// Compute default y- and z-domains, and unique them
	// 		let yDomain = new d3.InternSet(Y);
	// 		let zDomain = new d3.InternSet(Array.from(d3.union(Z))); // Unique category names

	// 		// Create color scale
	// 		let colors = d3.schemeSpectral[zDomain.size];

	// 		// Omit any data not present in the y- and z-domains.
	// 		const I = d3.range(X.length).filter((i) => yDomain.has(Y[i]) && zDomain.has(Z[i]));

	// 		// If the height is not specified, derive it from the y-domain.
	// 		height = yDomain.size * 25 + marginTop + marginBottom;
	// 		let yRange = [height - marginBottom, marginTop];

	// 		// Compute a nested array of series where each series is [[x1, x2], [x1, x2],
	// 		// [x1, x2], …] representing the x-extent of each stacked rect. In addition,
	// 		// each tuple has an i (index) property so that we can refer back to the
	// 		// original data point (data[i]). This code assumes that there is only one
	// 		// data point for a given unique y- and z-value.
	// 		const series = d3
	// 			.stack()
	// 			.keys(zDomain)
	// 			.value(([, I], z) => X[I.get(z)])
	// 			.order(d3.stackOrderNone)
	// 			.offset(d3.stackOffsetExpand)(
	// 				d3.rollup(
	// 					I,
	// 					([i]) => i,
	// 					(i) => Y[i],
	// 					(i) => Z[i]
	// 				)
	// 			)
	// 			.map((s) => s.map((d) => Object.assign(d, { i: d.data[1].get(s.key) })));

	// 		// Compute the default y-domain. Note: diverging stacks can be negative.
	// 		let xDomain = d3.extent(series.flat(2));

	// 		// Construct scales, axes, and formats.
	// 		const xScale = d3.scaleLinear(xDomain, [marginLeft, width + marginLeft - marginRight]);
	// 		const yScale = d3.scaleBand(yDomain, yRange).paddingInner(0.2);
	// 		const color = d3.scaleOrdinal(zDomain, colors);
	// 		const xAxis = d3.axisTop(xScale).ticks(width / 80, '%');
	// 		const yAxis = d3.axisLeft(yScale).tickSizeOuter(0);

	// 		// Create SVG
	// 		const svg = select(stackedBarChartSVG);

	// 		// Create bars
	// 		const bar = svg
	// 			.append('g')
	// 			.selectAll('g')
	// 			.data(series)
	// 			.join('g')
	// 			.attr('fill', ([{ i }]) => color(Z[i]))
	// 			.selectAll('rect')
	// 			.data((d) => d)
	// 			.join('rect')
	// 			.attr('x', ([x1, x2]) => Math.min(xScale(x1), xScale(x2)))
	// 			.attr('y', ({ i }) => yScale(Y[i]))
	// 			.attr('width', ([x1, x2]) => Math.abs(xScale(x1) - xScale(x2)))
	// 			.attr('height', yScale.bandwidth())
	// 			.append('title') // Node hover text
	// 			.text(function (d) {
	// 				return Z[d.i] + ': ' + X[d.i];
	// 			});
	// 		// .text((d) => Math.round(d.value * 100) / 100 + ' kgCO2e');

	// 		// Add upper legend
	// 		svg
	// 			.append('g')
	// 			.attr('transform', `translate(0,${marginTop})`)
	// 			.call(xAxis)
	// 			.call((g) => g.select('.domain').remove())
	// 			.call((g) =>
	// 				g
	// 					.append('text')
	// 					.attr('x', width - marginRight)
	// 					.attr('y', -22)
	// 					.attr('fill', 'currentColor')
	// 			);

	// 		// Add left legend
	// 		svg
	// 			.append('g')
	// 			.attr('transform', `translate(${xScale(0)},0)`)
	// 			.call(yAxis);
	// 	}
	// }

	function testStackedBar() {
		if (chartData && chartData.length > 0) {
			// Compute values
			const X = d3.map(chartData, (d) => d.impactCategory);
			const Y = d3.map(chartData, (d) => d.value);
			const Z = d3.map(chartData, (d) => d.category);

			// Compute default x- and z-domains, and unique them
			let xDomain = new d3.InternSet(X);
			let zDomain = new d3.InternSet(Array.from(d3.union(Z))); // Unique category names

			// Create color scale
			let colors = d3.schemeSpectral[zDomain.size];

			// Omit any data not present in the x- and z-domains.
			const I = d3.range(Y.length).filter((i) => xDomain.has(X[i]) && zDomain.has(Z[i]));

			// If the height is not specified, derive it from the x-domain.
			// height = xDomain.size * 25 + marginTop + marginBottom;
			let topLegendHeight = 20;
			let leftLegendWidth = 40;
			let xRange = [leftLegendWidth, width - marginRight];
			let yRange = [topLegendHeight, height - marginBottom];
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
			const yAxis = d3.axisLeft(yScale).ticks(width / 80, '%'); // ICI TOP
			const xAxis = d3.axisTop(xScale).tickSizeOuter(0); // ICI LEFT

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
				.call((g) =>
					g
						.append('text')
						.attr('x', width - marginRight)
						.attr('y', 0)
						.attr('fill', 'currentColor')
				);

			// Add left legend
			svg.append('g').attr('transform', `translate(${leftLegendWidth},0)`).call(yAxis);

			// Add legend under
			const legendHeight = 100;

			var legend = svg
				.append('g')
				.attr('class', 'legend')
				.attr('transform', 'translate(' + (marginLeft + 12) + ',' + (height - legendHeight) + ')');

			legend
				.selectAll('rect')
				.data(series)
				.enter()
				.append('rect')
				.attr('x', 0)
				.attr('y', function (d, i) {
					return i * 18;
				})
				.attr('width', 12)
				.attr('height', 12)
				.attr('fill', ([{ i }]) => color(Z[i]));

			legend
				.selectAll('text')
				.data(series)
				.enter()
				.append('text')
				.text(function (d) {
					console.log(d);
					return Z[d.i] + ': ' + Y[d.i];
				})
				.attr('x', 15)
				.attr('y', function (d, i) {
					return i * 18;
				})
				.attr('text-anchor', 'start')
				.attr('alignment-baseline', 'hanging');
		}
	}

	function drawLegend(vis, nodes, color) {
		vis
			.selectAll('mydots')
			.data(nodes)
			.enter()
			.append('circle')
			.attr('display', function (d) {
				return d.depth ? null : 'none'; // Do not dislay root node
			})
			.attr('cx', 120)
			.attr('cy', function (d, i) {
				return sunburstWidth / 2 + i * legendLineHeight;
			})
			.attr('r', 7)
			.style('fill', function (d) {
				return color(d.data.name);
			});

		// Add one dot in the legend for each name.
		vis
			.selectAll('mylabels')
			.data(nodes)
			.enter()
			.append('text')
			.attr('display', function (d) {
				return d.depth ? null : 'none'; // Do not dislay ùiddle circle
			})
			.attr('x', 140)
			.attr('y', function (d, i) {
				return sunburstWidth / 2 + i * legendLineHeight + 4;
			})
			.style('fill', function (d) {
				return 'black';
			})
			.text(function (d) {
				return d.data.name;
			});
	}

	function exportStackedBar() {
		exportSvg(stackedBarChartSVG.outerHTML, 'stackedBarChart');
	}

	onMount(function () {
		// drawStackedBar();
		testStackedBar();
	});
</script>

{#if chartData && chartData.length > 0}
	<svg bind:this={stackedBarChartSVG} viewBox="0 0 {width + marginLeft + marginRight} {height + marginBottom + marginTop}" preserveAspectRatio="xMidYMid meet" />
	<div class="d-flex justify-content-end">
		<button class="btn" on:click|stopPropagation={exportStackedBar} type="button">Export</button>
	</div>
{/if}
