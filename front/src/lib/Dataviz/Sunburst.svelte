<script lang="ts">
	import { onMount } from 'svelte';
	import { select } from 'd3-selection';
	import { arc, scaleOrdinal, partition, type HierarchyNode, schemeSet3, selectAll } from 'd3';

	export let hierarchy: HierarchyNode;

	let svgElement: SVGSVGElement;

	const margin = { top: 10, right: 10, bottom: 10, left: 10 },
		widthMin = 500 - margin.left - margin.right,
		heightMin = 500 - margin.left - margin.right,
		radius = heightMin / 2;

	async function drawSunburst() {
		// Construct svg attributes
		const vis = select(svgElement)
			.append('g')
			.attr('id', 'container')
			.attr('transform', 'translate(' + widthMin / 2 + ',' + heightMin / 2 + ')');

		// Add defs to fill each segment differently
		vis.append('defs').attr('id', 'defs');

		// Add text box middle
		addTextElement(vis);

		// Init the arc
		var svgArc = arc()
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
		var partitionSvg = partition().size([2 * Math.PI, radius * radius]);

		// Adding middle circle
		vis.append('circle').attr('r', radius).style('opacity', 0);

		// Classifying elements
		var root = hierarchy
			.sum((d: { value: any }) => d.value)
			.sort(function (a, b) {
				// 2
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

		// prepare a color scale
		const color = scaleOrdinal().domain(names).range(schemeSet3);

		// Create nodes
		var nodes = partitionSvg(root)
			.descendants()
			.filter(function (d) {
				return d.x1 - d.x0 > 0.005; // 0.005 radians = 0.29 degrees
			});

		var path = vis
			.selectAll('path')
			.data(nodes)
			.enter()
			.append('path')
			.attr('display', function (d) {
				return d.depth ? null : 'none'; // Do not dislay ùiddle circle
			})
			.attr('d', svgArc)
			.style('fill', (d) => {
				while (d.depth > 1) d = d.parent;
				return color(d.data.name);
			})
			.on('mouseover', (event, d) => {
				var sequenceArray = d.ancestors().reverse();
				sequenceArray.shift(); // suppression de la racine

				vis.select('#nameMiddle').text(d.data.name);
				vis.select('#valueMiddle').text(d.data.value);

				vis
					.selectAll('path') // Grey all segments
					.style('opacity', 0.3);

				vis
					.selectAll('path') // Ensuite on met en valeur uniquement ceux qui sont ancêtres de la sélection
					.filter(function (node) {
						return sequenceArray.indexOf(node) >= 0;
					})
					.style('opacity', 1);
			}); // 5

		// select('#chart-container').on('mouseleave', mouseleave);
	}

	function addTextElement(vis) {
		var textGroup = vis.append('g');

		textGroup.append('text').attr('id', 'nameMiddle').attr('y', -100).attr('class', 'entreprise').attr('text-anchor', 'middle');

		// textGroup.append('text').attr('id', 'type-amount').attr('y', -80).attr('class', 'type-amount').attr('text-anchor', 'middle');
		// textGroup.append('text').attr('id', 'category-amount').attr('y', -60).attr('class', 'category-amount').attr('text-anchor', 'middle');
		textGroup.append('text').attr('id', 'valueMiddle').attr('class', 'amount').attr('text-anchor', 'middle');
	}

	onMount(function () {
		drawSunburst();
	});
</script>

<div>
	<!-- <svg width={widthMin} height={heightMin} bind:this={svgElement} /> -->
	<svg bind:this={svgElement} viewBox="0 0 {widthMin + margin.left + margin.right} {heightMin + margin.left + margin.right}" preserveAspectRatio="xMidYMid meet" />
</div>
