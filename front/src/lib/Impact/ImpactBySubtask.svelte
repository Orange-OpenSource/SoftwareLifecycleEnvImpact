<script lang="ts">
	import type { Task, TaskImpact } from '$lib/api/dataModel';
	import { hierarchy, type HierarchyNode } from 'd3-hierarchy';
	import Sunburst from '$lib/Dataviz/Sunburst.svelte';
	import type { D3JSLink, D3JSHierarchyNode } from '$lib/Dataviz/d3js';
	import Sankey from '$lib/Dataviz/Sankey.svelte';
	import StackedBarChart from '$lib/Dataviz/StackedBarChart.svelte';

	export let impactBySubtask: TaskImpact[];

	/*Bound var*/
	export let selectedTask: Task;

	$: subtaskHierarchy = hierarchy({
		name: 'root',
		children: getHierarchyChildrenNodes(selectedTask, impactBySubtask)
	});

	$: subtasksLinks = constructLinks();

	function getHierarchyChildrenNodes(parentTask: Task, taskImpacts: TaskImpact[]): D3JSHierarchyNode[] {
		let returnValue: D3JSHierarchyNode[] = [];
		for (const taskImpact of taskImpacts) {
			/*Retrieve task object from its id*/
			let task = parentTask.subtasks.find((s) => s.id == Number(taskImpact.task_id))!;

			if (task != undefined) {
				// If retrieved, create node
				if (taskImpact.task_impact.impacts['Climate change'] != undefined) {
					/**For each task push it with its associated impact*/
					returnValue.push({
						name: task.name,
						task: task,
						impact: taskImpact.task_impact,
						// value: taskImpact.task_impact.impacts['Climate change'].value,
						co2: taskImpact.task_impact.impacts['Climate change'].value,
						children: getHierarchyChildrenNodes(task, taskImpact.subtasks)
					});
				}
			}
		}
		return returnValue;
	}

	function constructSubLinksRecursive(links: D3JSLink[], parentTask: Task, taskImpacts: TaskImpact[]) {
		for (const taskImpact of taskImpacts) {
			/*Retrieve task object from its id*/
			let task = parentTask.subtasks.find((s) => s.id == Number(taskImpact.task_id))!;

			if (task != undefined) {
				// If retrieved, create node
				links.push({
					source: parentTask.name,
					target: task.name,
					value: taskImpact.task_impact.impacts['Climate change'].value
				});

				/*Add for each impact*/
				for (const [resourceName, resourceImpact] of Object.entries(taskImpact.resources)) {
					links.push({
						source: parentTask.name,
						target: resourceName,
						value: resourceImpact.impacts['Climate change'].value
					});
				}

				// Recursive call
				constructSubLinksRecursive(links, task, taskImpact.subtasks);
			}
		}
	}

	function constructLinks(): D3JSLink[] {
		let links: D3JSLink[] = [];
		constructSubLinksRecursive(links, selectedTask, impactBySubtask);
		return links;
	}

	function mockStackedBarData() {
		return [
				{
					impactCategory: 'AL',
					category: '<10',
					value: 598478
				},
				{
					impactCategory: 'AK',
					category: '<10',
					value: 106741
				},
				{
					impactCategory: 'AZ',
					category: '<10',
					value: 892083
				},
				{
					impactCategory: 'AR',
					category: '<10',
					value: 392177
				},
				{
					impactCategory: 'CA',
					category: '<10',
					value: 5038433
				},
				{
					impactCategory: 'CO',
					category: '<10',
					value: 690830
				},
				{
					impactCategory: 'CT',
					category: '<10',
					value: 399369
				},
				{
					impactCategory: 'DE',
					category: '<10',
					value: 112177
				},
				{
					impactCategory: 'DC',
					category: '<10',
					value: 74377
				},
				{
					impactCategory: 'FL',
					category: '<10',
					value: 2211012
				},
				{
					impactCategory: 'GA',
					category: '<10',
					value: 1363631
				},
				{
					impactCategory: 'HI',
					category: '<10',
					value: 176484
				},
				{
					impactCategory: 'ID',
					category: '<10',
					value: 236658
				},
				{
					impactCategory: 'IL',
					category: '<10',
					value: 1619682
				},
				{
					impactCategory: 'IN',
					category: '<10',
					value: 863029
				},
				{
					impactCategory: 'IA',
					category: '<10',
					value: 401712
				},
				{
					impactCategory: 'KS',
					category: '<10',
					value: 401751
				},
				{
					impactCategory: 'KY',
					category: '<10',
					value: 555615
				},
				{
					impactCategory: 'LA',
					category: '<10',
					value: 622061
				},
				{
					impactCategory: 'ME',
					category: '<10',
					value: 137954
				},
				{
					impactCategory: 'MD',
					category: '<10',
					value: 741952
				},
				{
					impactCategory: 'MA',
					category: '<10',
					value: 737748
				},
				{
					impactCategory: 'MI',
					category: '<10',
					value: 1181424
				},
				{
					impactCategory: 'MN',
					category: '<10',
					value: 711604
				},
				{
					impactCategory: 'MS',
					category: '<10',
					value: 400288
				},
				{
					impactCategory: 'MO',
					category: '<10',
					value: 763948
				},
				{
					impactCategory: 'MT',
					category: '<10',
					value: 126020
				},
				{
					impactCategory: 'NE',
					category: '<10',
					value: 263518
				},
				{
					impactCategory: 'NV',
					category: '<10',
					value: 369362
				},
				{
					impactCategory: 'NH',
					category: '<10',
					value: 138762
				},
				{
					impactCategory: 'NJ',
					category: '<10',
					value: 1079136
				},
				{
					impactCategory: 'NM',
					category: '<10',
					value: 276468
				},
				{
					impactCategory: 'NY',
					category: '<10',
					value: 2319945
				},
				{
					impactCategory: 'NC',
					category: '<10',
					value: 1250298
				},
				{
					impactCategory: 'ND',
					category: '<10',
					value: 99477
				},
				{
					impactCategory: 'OH',
					category: '<10',
					value: 1422838
				},
				{
					impactCategory: 'OK',
					category: '<10',
					value: 534481
				},
				{
					impactCategory: 'OR',
					category: '<10',
					value: 474456
				},
				{
					impactCategory: 'PA',
					category: '<10',
					value: 1458931
				},
				{
					impactCategory: 'RI',
					category: '<10',
					value: 111377
				},
				{
					impactCategory: 'SC',
					category: '<10',
					value: 599591
				},
				{
					impactCategory: 'SD',
					category: '<10',
					value: 120366
				},
				{
					impactCategory: 'TN',
					category: '<10',
					value: 818404
				},
				{
					impactCategory: 'TX',
					category: '<10',
					value: 3983091
				},
				{
					impactCategory: 'UT',
					category: '<10',
					value: 513515
				},
				{
					impactCategory: 'VT',
					category: '<10',
					value: 63768
				},
				{
					impactCategory: 'VA',
					category: '<10',
					value: 1033629
				},
				{
					impactCategory: 'WA',
					category: '<10',
					value: 895790
				},
				{
					impactCategory: 'WV',
					category: '<10',
					value: 207017
				},
				{
					impactCategory: 'WI',
					category: '<10',
					value: 705648
				},
				{
					impactCategory: 'WY',
					category: '<10',
					value: 78217
				},
				{
					impactCategory: 'PR',
					category: '<10',
					value: 389428
				},
				{
					impactCategory: 'AL',
					category: '10-19',
					value: 638789
				},
				{
					impactCategory: 'AK',
					category: '10-19',
					value: 99926
				},
				{
					impactCategory: 'AZ',
					category: '10-19',
					value: 912735
				},
				{
					impactCategory: 'AR',
					category: '10-19',
					value: 397185
				},
				{
					impactCategory: 'CA',
					category: '10-19',
					value: 5170341
				},
				{
					impactCategory: 'CO',
					category: '10-19',
					value: 697447
				},
				{
					impactCategory: 'CT',
					category: '10-19',
					value: 481065
				},
				{
					impactCategory: 'DE',
					category: '10-19',
					value: 117854
				},
				{
					impactCategory: 'DC',
					category: '10-19',
					value: 62783
				},
				{
					impactCategory: 'FL',
					category: '10-19',
					value: 2331102
				},
				{
					impactCategory: 'GA',
					category: '10-19',
					value: 1421557
				},
				{
					impactCategory: 'HI',
					category: '10-19',
					value: 163559
				},
				{
					impactCategory: 'ID',
					category: '10-19',
					value: 239509
				},
				{
					impactCategory: 'IL',
					category: '10-19',
					value: 1715984
				},
				{
					impactCategory: 'IN',
					category: '10-19',
					value: 905594
				},
				{
					impactCategory: 'IA',
					category: '10-19',
					value: 418667
				},
				{
					impactCategory: 'KS',
					category: '10-19',
					value: 402092
				},
				{
					impactCategory: 'KY',
					category: '10-19',
					value: 575866
				},
				{
					impactCategory: 'LA',
					category: '10-19',
					value: 613633
				},
				{
					impactCategory: 'ME',
					category: '10-19',
					value: 155774
				},
				{
					impactCategory: 'MD',
					category: '10-19',
					value: 764730
				},
				{
					impactCategory: 'MA',
					category: '10-19',
					value: 862371
				},
				{
					impactCategory: 'MI',
					category: '10-19',
					value: 1324071
				},
				{
					impactCategory: 'MN',
					category: '10-19',
					value: 714399
				},
				{
					impactCategory: 'MS',
					category: '10-19',
					value: 421329
				},
				{
					impactCategory: 'MO',
					category: '10-19',
					value: 792935
				},
				{
					impactCategory: 'MT',
					category: '10-19',
					value: 126294
				},
				{
					impactCategory: 'NE',
					category: '10-19',
					value: 257610
				},
				{
					impactCategory: 'NV',
					category: '10-19',
					value: 360263
				},
				{
					impactCategory: 'NH',
					category: '10-19',
					value: 167495
				},
				{
					impactCategory: 'NJ',
					category: '10-19',
					value: 1153625
				},
				{
					impactCategory: 'NM',
					category: '10-19',
					value: 282662
				},
				{
					impactCategory: 'NY',
					category: '10-19',
					value: 2445591
				},
				{
					impactCategory: 'NC',
					category: '10-19',
					value: 1310398
				},
				{
					impactCategory: 'ND',
					category: '10-19',
					value: 91069
				},
				{
					impactCategory: 'OH',
					category: '10-19',
					value: 1530264
				},
				{
					impactCategory: 'OK',
					category: '10-19',
					value: 522282
				},
				{
					impactCategory: 'OR',
					category: '10-19',
					value: 485345
				},
				{
					impactCategory: 'PA',
					category: '10-19',
					value: 1608018
				},
				{
					impactCategory: 'RI',
					category: '10-19',
					value: 136885
				},
				{
					impactCategory: 'SC',
					category: '10-19',
					value: 619144
				},
				{
					impactCategory: 'SD',
					category: '10-19',
					value: 113383
				},
				{
					impactCategory: 'TN',
					category: '10-19',
					value: 842873
				},
				{
					impactCategory: 'TX',
					category: '10-19',
					value: 3910528
				},
				{
					impactCategory: 'UT',
					category: '10-19',
					value: 479126
				},
				{
					impactCategory: 'VT',
					category: '10-19',
					value: 79351
				},
				{
					impactCategory: 'VA',
					category: '10-19',
					value: 1065461
				},
				{
					impactCategory: 'WA',
					category: '10-19',
					value: 882812
				},
				{
					impactCategory: 'WV',
					category: '10-19',
					value: 218547
				},
				{
					impactCategory: 'WI',
					category: '10-19',
					value: 755224
				},
				{
					impactCategory: 'WY',
					category: '10-19',
					value: 75535
				},
				{
					impactCategory: 'PR',
					category: '10-19',
					value: 479749
				},
				{
					impactCategory: 'AL',
					category: '20-29',
					value: 661666
				},
				{
					impactCategory: 'AK',
					category: '20-29',
					value: 120674
				},
				{
					impactCategory: 'AZ',
					category: '20-29',
					value: 939804
				},
				{
					impactCategory: 'AR',
					category: '20-29',
					value: 399698
				},
				{
					impactCategory: 'CA',
					category: '20-29',
					value: 5809455
				},
				{
					impactCategory: 'CO',
					category: '20-29',
					value: 780508
				},
				{
					impactCategory: 'CT',
					category: '20-29',
					value: 462323
				},
				{
					impactCategory: 'DE',
					category: '20-29',
					value: 127554
				},
				{
					impactCategory: 'DC',
					category: '20-29',
					value: 136976
				},
				{
					impactCategory: 'FL',
					category: '20-29',
					value: 2597830
				},
				{
					impactCategory: 'GA',
					category: '20-29',
					value: 1418696
				},
				{
					impactCategory: 'HI',
					category: '20-29',
					value: 204336
				},
				{
					impactCategory: 'ID',
					category: '20-29',
					value: 218684
				},
				{
					impactCategory: 'IL',
					category: '20-29',
					value: 1789739
				},
				{
					impactCategory: 'IN',
					category: '20-29',
					value: 905590
				},
				{
					impactCategory: 'IA',
					category: '20-29',
					value: 419456
				},
				{
					impactCategory: 'KS',
					category: '20-29',
					value: 406956
				},
				{
					impactCategory: 'KY',
					category: '20-29',
					value: 593819
				},
				{
					impactCategory: 'LA',
					category: '20-29',
					value: 683606
				},
				{
					impactCategory: 'ME',
					category: '20-29',
					value: 156359
				},
				{
					impactCategory: 'MD',
					category: '20-29',
					value: 815346
				},
				{
					impactCategory: 'MA',
					category: '20-29',
					value: 971340
				},
				{
					impactCategory: 'MI',
					category: '20-29',
					value: 1338179
				},
				{
					impactCategory: 'MN',
					category: '20-29',
					value: 728222
				},
				{
					impactCategory: 'MS',
					category: '20-29',
					value: 414195
				},
				{
					impactCategory: 'MO',
					category: '20-29',
					value: 831725
				},
				{
					impactCategory: 'MT',
					category: '20-29',
					value: 136346
				},
				{
					impactCategory: 'NE',
					category: '20-29',
					value: 260646
				},
				{
					impactCategory: 'NV',
					category: '20-29',
					value: 392834
				},
				{
					impactCategory: 'NH',
					category: '20-29',
					value: 167554
				},
				{
					impactCategory: 'NJ',
					category: '20-29',
					value: 1139927
				},
				{
					impactCategory: 'NM',
					category: '20-29',
					value: 289801
				},
				{
					impactCategory: 'NY',
					category: '20-29',
					value: 2894266
				},
				{
					impactCategory: 'NC',
					category: '20-29',
					value: 1350242
				},
				{
					impactCategory: 'ND',
					category: '20-29',
					value: 124509
				},
				{
					impactCategory: 'OH',
					category: '20-29',
					value: 1535538
				},
				{
					impactCategory: 'OK',
					category: '20-29',
					value: 552528
				},
				{
					impactCategory: 'OR',
					category: '20-29',
					value: 538596
				},
				{
					impactCategory: 'PA',
					category: '20-29',
					value: 1712448
				},
				{
					impactCategory: 'RI',
					category: '20-29',
					value: 153674
				},
				{
					impactCategory: 'SC',
					category: '20-29',
					value: 667523
				},
				{
					impactCategory: 'SD',
					category: '20-29',
					value: 116748
				},
				{
					impactCategory: 'TN',
					category: '20-29',
					value: 895337
				},
				{
					impactCategory: 'TX',
					category: '20-29',
					value: 3946447
				},
				{
					impactCategory: 'UT',
					category: '20-29',
					value: 465219
				},
				{
					impactCategory: 'VT',
					category: '20-29',
					value: 81765
				},
				{
					impactCategory: 'VA',
					category: '20-29',
					value: 1170634
				},
				{
					impactCategory: 'WA',
					category: '20-29',
					value: 1004428
				},
				{
					impactCategory: 'WV',
					category: '20-29',
					value: 232027
				},
				{
					impactCategory: 'WI',
					category: '20-29',
					value: 760961
				},
				{
					impactCategory: 'WY',
					category: '20-29',
					value: 82898
				},
				{
					impactCategory: 'PR',
					category: '20-29',
					value: 480184
				},
				{
					impactCategory: 'AL',
					category: '30-39',
					value: 603013
				},
				{
					impactCategory: 'AK',
					category: '30-39',
					value: 102008
				},
				{
					impactCategory: 'AZ',
					category: '30-39',
					value: 857054
				},
				{
					impactCategory: 'AR',
					category: '30-39',
					value: 372998
				},
				{
					impactCategory: 'CA',
					category: '30-39',
					value: 5354112
				},
				{
					impactCategory: 'CO',
					category: '30-39',
					value: 766382
				},
				{
					impactCategory: 'CT',
					category: '30-39',
					value: 424890
				},
				{
					impactCategory: 'DE',
					category: '30-39',
					value: 114063
				},
				{
					impactCategory: 'DC',
					category: '30-39',
					value: 121520
				},
				{
					impactCategory: 'FL',
					category: '30-39',
					value: 2416176
				},
				{
					impactCategory: 'GA',
					category: '30-39',
					value: 1357210
				},
				{
					impactCategory: 'HI',
					category: '30-39',
					value: 187590
				},
				{
					impactCategory: 'ID',
					category: '30-39',
					value: 209500
				},
				{
					impactCategory: 'IL',
					category: '30-39',
					value: 1721954
				},
				{
					impactCategory: 'IN',
					category: '30-39',
					value: 827086
				},
				{
					impactCategory: 'IA',
					category: '30-39',
					value: 383638
				},
				{
					impactCategory: 'KS',
					category: '30-39',
					value: 368732
				},
				{
					impactCategory: 'KY',
					category: '30-39',
					value: 558201
				},
				{
					impactCategory: 'LA',
					category: '30-39',
					value: 615411
				},
				{
					impactCategory: 'ME',
					category: '30-39',
					value: 147695
				},
				{
					impactCategory: 'MD',
					category: '30-39',
					value: 784097
				},
				{
					impactCategory: 'MA',
					category: '30-39',
					value: 847306
				},
				{
					impactCategory: 'MI',
					category: '30-39',
					value: 1162186
				},
				{
					impactCategory: 'MN',
					category: '30-39',
					value: 715583
				},
				{
					impactCategory: 'MS',
					category: '30-39',
					value: 374724
				},
				{
					impactCategory: 'MO',
					category: '30-39',
					value: 763002
				},
				{
					impactCategory: 'MT',
					category: '30-39',
					value: 125004
				},
				{
					impactCategory: 'NE',
					category: '30-39',
					value: 244236
				},
				{
					impactCategory: 'NV',
					category: '30-39',
					value: 390261
				},
				{
					impactCategory: 'NH',
					category: '30-39',
					value: 151409
				},
				{
					impactCategory: 'NJ',
					category: '30-39',
					value: 1143452
				},
				{
					impactCategory: 'NM',
					category: '30-39',
					value: 260579
				},
				{
					impactCategory: 'NY',
					category: '30-39',
					value: 2605355
				},
				{
					impactCategory: 'NC',
					category: '30-39',
					value: 1268976
				},
				{
					impactCategory: 'ND',
					category: '30-39',
					value: 94713
				},
				{
					impactCategory: 'OH',
					category: '30-39',
					value: 1398724
				},
				{
					impactCategory: 'OK',
					category: '30-39',
					value: 501392
				},
				{
					impactCategory: 'OR',
					category: '30-39',
					value: 537767
				},
				{
					impactCategory: 'PA',
					category: '30-39',
					value: 1520409
				},
				{
					impactCategory: 'RI',
					category: '30-39',
					value: 126503
				},
				{
					impactCategory: 'SC',
					category: '30-39',
					value: 596491
				},
				{
					impactCategory: 'SD',
					category: '30-39',
					value: 105499
				},
				{
					impactCategory: 'TN',
					category: '30-39',
					value: 837313
				},
				{
					impactCategory: 'TX',
					category: '30-39',
					value: 3770534
				},
				{
					impactCategory: 'UT',
					category: '30-39',
					value: 436010
				},
				{
					impactCategory: 'VT',
					category: '30-39',
					value: 70092
				},
				{
					impactCategory: 'VA',
					category: '30-39',
					value: 1112111
				},
				{
					impactCategory: 'WA',
					category: '30-39',
					value: 970613
				},
				{
					impactCategory: 'WV',
					category: '30-39',
					value: 220494
				},
				{
					impactCategory: 'WI',
					category: '30-39',
					value: 714479
				},
				{
					impactCategory: 'WY',
					category: '30-39',
					value: 76912
				},
				{
					impactCategory: 'PR',
					category: '30-39',
					value: 441842
				},
				{
					impactCategory: 'AL',
					category: '40-49',
					value: 625599
				},
				{
					impactCategory: 'AK',
					category: '40-49',
					value: 91539
				},
				{
					impactCategory: 'AZ',
					category: '40-49',
					value: 833290
				},
				{
					impactCategory: 'AR',
					category: '40-49',
					value: 370157
				},
				{
					impactCategory: 'CA',
					category: '40-49',
					value: 5179258
				},
				{
					impactCategory: 'CO',
					category: '40-49',
					value: 705450
				},
				{
					impactCategory: 'CT',
					category: '40-49',
					value: 496265
				},
				{
					impactCategory: 'DE',
					category: '40-49',
					value: 117588
				},
				{
					impactCategory: 'DC',
					category: '40-49',
					value: 80570
				},
				{
					impactCategory: 'FL',
					category: '40-49',
					value: 2575576
				},
				{
					impactCategory: 'GA',
					category: '40-49',
					value: 1404698
				},
				{
					impactCategory: 'HI',
					category: '40-49',
					value: 176904
				},
				{
					impactCategory: 'ID',
					category: '40-49',
					value: 194678
				},
				{
					impactCategory: 'IL',
					category: '40-49',
					value: 1697069
				},
				{
					impactCategory: 'IN',
					category: '40-49',
					value: 844059
				},
				{
					impactCategory: 'IA',
					category: '40-49',
					value: 370719
				},
				{
					impactCategory: 'KS',
					category: '40-49',
					value: 344427
				},
				{
					impactCategory: 'KY',
					category: '40-49',
					value: 580553
				},
				{
					impactCategory: 'LA',
					category: '40-49',
					value: 571991
				},
				{
					impactCategory: 'ME',
					category: '40-49',
					value: 176908
				},
				{
					impactCategory: 'MD',
					category: '40-49',
					value: 815875
				},
				{
					impactCategory: 'MA',
					category: '40-49',
					value: 916106
				},
				{
					impactCategory: 'MI',
					category: '40-49',
					value: 1283122
				},
				{
					impactCategory: 'MN',
					category: '40-49',
					value: 692201
				},
				{
					impactCategory: 'MS',
					category: '40-49',
					value: 377165
				},
				{
					impactCategory: 'MO',
					category: '40-49',
					value: 750989
				},
				{
					impactCategory: 'MT',
					category: '40-49',
					value: 116502
				},
				{
					impactCategory: 'NE',
					category: '40-49',
					value: 222479
				},
				{
					impactCategory: 'NV',
					category: '40-49',
					value: 387272
				},
				{
					impactCategory: 'NH',
					category: '40-49',
					value: 182703
				},
				{
					impactCategory: 'NJ',
					category: '40-49',
					value: 1254602
				},
				{
					impactCategory: 'NM',
					category: '40-49',
					value: 244346
				},
				{
					impactCategory: 'NY',
					category: '40-49',
					value: 2617327
				},
				{
					impactCategory: 'NC',
					category: '40-49',
					value: 1357746
				},
				{
					impactCategory: 'ND',
					category: '40-49',
					value: 80327
				},
				{
					impactCategory: 'OH',
					category: '40-49',
					value: 1490959
				},
				{
					impactCategory: 'OK',
					category: '40-49',
					value: 469410
				},
				{
					impactCategory: 'OR',
					category: '40-49',
					value: 507826
				},
				{
					impactCategory: 'PA',
					category: '40-49',
					value: 1645291
				},
				{
					impactCategory: 'RI',
					category: '40-49',
					value: 137892
				},
				{
					impactCategory: 'SC',
					category: '40-49',
					value: 619792
				},
				{
					impactCategory: 'SD',
					category: '40-49',
					value: 96288
				},
				{
					impactCategory: 'TN',
					category: '40-49',
					value: 866343
				},
				{
					impactCategory: 'TX',
					category: '40-49',
					value: 3545746
				},
				{
					impactCategory: 'UT',
					category: '40-49',
					value: 328569
				},
				{
					impactCategory: 'VT',
					category: '40-49',
					value: 79982
				},
				{
					impactCategory: 'VA',
					category: '40-49',
					value: 1134928
				},
				{
					impactCategory: 'WA',
					category: '40-49',
					value: 921205
				},
				{
					impactCategory: 'WV',
					category: '40-49',
					value: 238218
				},
				{
					impactCategory: 'WI',
					category: '40-49',
					value: 732280
				},
				{
					impactCategory: 'WY',
					category: '40-49',
					value: 68464
				},
				{
					impactCategory: 'PR',
					category: '40-49',
					value: 456009
				},
				{
					impactCategory: 'AL',
					category: '50-59',
					value: 673864
				},
				{
					impactCategory: 'AK',
					category: '50-59',
					value: 104569
				},
				{
					impactCategory: 'AZ',
					category: '50-59',
					value: 834858
				},
				{
					impactCategory: 'AR',
					category: '50-59',
					value: 395070
				},
				{
					impactCategory: 'CA',
					category: '50-59',
					value: 5042094
				},
				{
					impactCategory: 'CO',
					category: '50-59',
					value: 725661
				},
				{
					impactCategory: 'CT',
					category: '50-59',
					value: 546361
				},
				{
					impactCategory: 'DE',
					category: '50-59',
					value: 133331
				},
				{
					impactCategory: 'DC',
					category: '50-59',
					value: 74779
				},
				{
					impactCategory: 'FL',
					category: '50-59',
					value: 2762983
				},
				{
					impactCategory: 'GA',
					category: '50-59',
					value: 1337985
				},
				{
					impactCategory: 'HI',
					category: '50-59',
					value: 188438
				},
				{
					impactCategory: 'ID',
					category: '50-59',
					value: 205170
				},
				{
					impactCategory: 'IL',
					category: '50-59',
					value: 1773366
				},
				{
					impactCategory: 'IN',
					category: '50-59',
					value: 911778
				},
				{
					impactCategory: 'IA',
					category: '50-59',
					value: 427554
				},
				{
					impactCategory: 'KS',
					category: '50-59',
					value: 389834
				},
				{
					impactCategory: 'KY',
					category: '50-59',
					value: 623164
				},
				{
					impactCategory: 'LA',
					category: '50-59',
					value: 631936
				},
				{
					impactCategory: 'ME',
					category: '50-59',
					value: 215787
				},
				{
					impactCategory: 'MD',
					category: '50-59',
					value: 862778
				},
				{
					impactCategory: 'MA',
					category: '50-59',
					value: 979128
				},
				{
					impactCategory: 'MI',
					category: '50-59',
					value: 1454462
				},
				{
					impactCategory: 'MN',
					category: '50-59',
					value: 782655
				},
				{
					impactCategory: 'MS',
					category: '50-59',
					value: 400164
				},
				{
					impactCategory: 'MO',
					category: '50-59',
					value: 857534
				},
				{
					impactCategory: 'MT',
					category: '50-59',
					value: 149800
				},
				{
					impactCategory: 'NE',
					category: '50-59',
					value: 250911
				},
				{
					impactCategory: 'NV',
					category: '50-59',
					value: 373757
				},
				{
					impactCategory: 'NH',
					category: '50-59',
					value: 217950
				},
				{
					impactCategory: 'NJ',
					category: '50-59',
					value: 1307263
				},
				{
					impactCategory: 'NM',
					category: '50-59',
					value: 280363
				},
				{
					impactCategory: 'NY',
					category: '50-59',
					value: 2755620
				},
				{
					impactCategory: 'NC',
					category: '50-59',
					value: 1356117
				},
				{
					impactCategory: 'ND',
					category: '50-59',
					value: 98688
				},
				{
					impactCategory: 'OH',
					category: '50-59',
					value: 1677794
				},
				{
					impactCategory: 'OK',
					category: '50-59',
					value: 512850
				},
				{
					impactCategory: 'OR',
					category: '50-59',
					value: 534421
				},
				{
					impactCategory: 'PA',
					category: '50-59',
					value: 1881378
				},
				{
					impactCategory: 'RI',
					category: '50-59',
					value: 156127
				},
				{
					impactCategory: 'SC',
					category: '50-59',
					value: 663408
				},
				{
					impactCategory: 'SD',
					category: '50-59',
					value: 117012
				},
				{
					impactCategory: 'TN',
					category: '50-59',
					value: 904272
				},
				{
					impactCategory: 'TX',
					category: '50-59',
					value: 3344930
				},
				{
					impactCategory: 'UT',
					category: '50-59',
					value: 301596
				},
				{
					impactCategory: 'VT',
					category: '50-59',
					value: 99521
				},
				{
					impactCategory: 'VA',
					category: '50-59',
					value: 1162028
				},
				{
					impactCategory: 'WA',
					category: '50-59',
					value: 970407
				},
				{
					impactCategory: 'WV',
					category: '50-59',
					value: 269346
				},
				{
					impactCategory: 'WI',
					category: '50-59',
					value: 848672
				},
				{
					impactCategory: 'WY',
					category: '50-59',
					value: 81018
				},
				{
					impactCategory: 'PR',
					category: '50-59',
					value: 452503
				},
				{
					impactCategory: 'AL',
					category: '60-69',
					value: 548376
				},
				{
					impactCategory: 'AK',
					category: '60-69',
					value: 70473
				},
				{
					impactCategory: 'AZ',
					category: '60-69',
					value: 737884
				},
				{
					impactCategory: 'AR',
					category: '60-69',
					value: 329734
				},
				{
					impactCategory: 'CA',
					category: '60-69',
					value: 3737461
				},
				{
					impactCategory: 'CO',
					category: '60-69',
					value: 563376
				},
				{
					impactCategory: 'CT',
					category: '60-69',
					value: 400995
				},
				{
					impactCategory: 'DE',
					category: '60-69',
					value: 110822
				},
				{
					impactCategory: 'DC',
					category: '60-69',
					value: 56984
				},
				{
					impactCategory: 'FL',
					category: '60-69',
					value: 2404659
				},
				{
					impactCategory: 'GA',
					category: '60-69',
					value: 998253
				},
				{
					impactCategory: 'HI',
					category: '60-69',
					value: 164957
				},
				{
					impactCategory: 'ID',
					category: '60-69',
					value: 179429
				},
				{
					impactCategory: 'IL',
					category: '60-69',
					value: 1326121
				},
				{
					impactCategory: 'IN',
					category: '60-69',
					value: 704523
				},
				{
					impactCategory: 'IA',
					category: '60-69',
					value: 344037
				},
				{
					impactCategory: 'KS',
					category: '60-69',
					value: 300759
				},
				{
					impactCategory: 'KY',
					category: '60-69',
					value: 495736
				},
				{
					impactCategory: 'LA',
					category: '60-69',
					value: 488846
				},
				{
					impactCategory: 'ME',
					category: '60-69',
					value: 179540
				},
				{
					impactCategory: 'MD',
					category: '60-69',
					value: 636309
				},
				{
					impactCategory: 'MA',
					category: '60-69',
					value: 737805
				},
				{
					impactCategory: 'MI',
					category: '60-69',
					value: 1148131
				},
				{
					impactCategory: 'MN',
					category: '60-69',
					value: 577313
				},
				{
					impactCategory: 'MS',
					category: '60-69',
					value: 319443
				},
				{
					impactCategory: 'MO',
					category: '60-69',
					value: 668878
				},
				{
					impactCategory: 'MT',
					category: '60-69',
					value: 130977
				},
				{
					impactCategory: 'NE',
					category: '60-69',
					value: 195705
				},
				{
					impactCategory: 'NV',
					category: '60-69',
					value: 309651
				},
				{
					impactCategory: 'NH',
					category: '60-69',
					value: 164287
				},
				{
					impactCategory: 'NJ',
					category: '60-69',
					value: 946399
				},
				{
					impactCategory: 'NM',
					category: '60-69',
					value: 239044
				},
				{
					impactCategory: 'NY',
					category: '60-69',
					value: 2095207
				},
				{
					impactCategory: 'NC',
					category: '60-69',
					value: 1095320
				},
				{
					impactCategory: 'ND',
					category: '60-69',
					value: 73825
				},
				{
					impactCategory: 'OH',
					category: '60-69',
					value: 1320776
				},
				{
					impactCategory: 'OK',
					category: '60-69',
					value: 404704
				},
				{
					impactCategory: 'OR',
					category: '60-69',
					value: 490894
				},
				{
					impactCategory: 'PA',
					category: '60-69',
					value: 1491536
				},
				{
					impactCategory: 'RI',
					category: '60-69',
					value: 117653
				},
				{
					impactCategory: 'SC',
					category: '60-69',
					value: 579856
				},
				{
					impactCategory: 'SD',
					category: '60-69',
					value: 92824
				},
				{
					impactCategory: 'TN',
					category: '60-69',
					value: 741045
				},
				{
					impactCategory: 'TX',
					category: '60-69',
					value: 2431494
				},
				{
					impactCategory: 'UT',
					category: '60-69',
					value: 230007
				},
				{
					impactCategory: 'VT',
					category: '60-69',
					value: 82136
				},
				{
					impactCategory: 'VA',
					category: '60-69',
					value: 881763
				},
				{
					impactCategory: 'WA',
					category: '60-69',
					value: 784208
				},
				{
					impactCategory: 'WV',
					category: '60-69',
					value: 243108
				},
				{
					impactCategory: 'WI',
					category: '60-69',
					value: 645015
				},
				{
					impactCategory: 'WY',
					category: '60-69',
					value: 67484
				},
				{
					impactCategory: 'PR',
					category: '60-69',
					value: 411924
				},
				{
					impactCategory: 'AL',
					category: '70-79',
					value: 316598
				},
				{
					impactCategory: 'AK',
					category: '70-79',
					value: 28422
				},
				{
					impactCategory: 'AZ',
					category: '70-79',
					value: 466153
				},
				{
					impactCategory: 'AR',
					category: '70-79',
					value: 197985
				},
				{
					impactCategory: 'CA',
					category: '70-79',
					value: 2011678
				},
				{
					impactCategory: 'CO',
					category: '70-79',
					value: 274466
				},
				{
					impactCategory: 'CT',
					category: '70-79',
					value: 217827
				},
				{
					impactCategory: 'DE',
					category: '70-79',
					value: 65369
				},
				{
					impactCategory: 'DC',
					category: '70-79',
					value: 31362
				},
				{
					impactCategory: 'FL',
					category: '70-79',
					value: 1615547
				},
				{
					impactCategory: 'GA',
					category: '70-79',
					value: 528108
				},
				{
					impactCategory: 'HI',
					category: '70-79',
					value: 85345
				},
				{
					impactCategory: 'ID',
					category: '70-79',
					value: 97621
				},
				{
					impactCategory: 'IL',
					category: '70-79',
					value: 728821
				},
				{
					impactCategory: 'IN',
					category: '70-79',
					value: 384788
				},
				{
					impactCategory: 'IA',
					category: '70-79',
					value: 197223
				},
				{
					impactCategory: 'KS',
					category: '70-79',
					value: 166104
				},
				{
					impactCategory: 'KY',
					category: '70-79',
					value: 273961
				},
				{
					impactCategory: 'LA',
					category: '70-79',
					value: 266123
				},
				{
					impactCategory: 'ME',
					category: '70-79',
					value: 97899
				},
				{
					impactCategory: 'MD',
					category: '70-79',
					value: 330736
				},
				{
					impactCategory: 'MA',
					category: '70-79',
					value: 401931
				},
				{
					impactCategory: 'MI',
					category: '70-79',
					value: 619722
				},
				{
					impactCategory: 'MN',
					category: '70-79',
					value: 312906
				},
				{
					impactCategory: 'MS',
					category: '70-79',
					value: 181195
				},
				{
					impactCategory: 'MO',
					category: '70-79',
					value: 388086
				},
				{
					impactCategory: 'MT',
					category: '70-79',
					value: 70528
				},
				{
					impactCategory: 'NE',
					category: '70-79',
					value: 107650
				},
				{
					impactCategory: 'NV',
					category: '70-79',
					value: 173499
				},
				{
					impactCategory: 'NH',
					category: '70-79',
					value: 84791
				},
				{
					impactCategory: 'NJ',
					category: '70-79',
					value: 523620
				},
				{
					impactCategory: 'NM',
					category: '70-79',
					value: 135013
				},
				{
					impactCategory: 'NY',
					category: '70-79',
					value: 1160055
				},
				{
					impactCategory: 'NC',
					category: '70-79',
					value: 609234
				},
				{
					impactCategory: 'ND',
					category: '70-79',
					value: 41348
				},
				{
					impactCategory: 'OH',
					category: '70-79',
					value: 728158
				},
				{
					impactCategory: 'OK',
					category: '70-79',
					value: 239887
				},
				{
					impactCategory: 'OR',
					category: '70-79',
					value: 255809
				},
				{
					impactCategory: 'PA',
					category: '70-79',
					value: 850897
				},
				{
					impactCategory: 'RI',
					category: '70-79',
					value: 63359
				},
				{
					impactCategory: 'SC',
					category: '70-79',
					value: 322073
				},
				{
					impactCategory: 'SD',
					category: '70-79',
					value: 50398
				},
				{
					impactCategory: 'TN',
					category: '70-79',
					value: 414939
				},
				{
					impactCategory: 'TX',
					category: '70-79',
					value: 1291486
				},
				{
					impactCategory: 'UT',
					category: '70-79',
					value: 123674
				},
				{
					impactCategory: 'VT',
					category: '70-79',
					value: 42978
				},
				{
					impactCategory: 'VA',
					category: '70-79',
					value: 475141
				},
				{
					impactCategory: 'WA',
					category: '70-79',
					value: 401094
				},
				{
					impactCategory: 'WV',
					category: '70-79',
					value: 138134
				},
				{
					impactCategory: 'WI',
					category: '70-79',
					value: 350772
				},
				{
					impactCategory: 'WY',
					category: '70-79',
					value: 32819
				},
				{
					impactCategory: 'PR',
					category: '70-79',
					value: 268783
				},
				{
					impactCategory: 'AL',
					category: '≥80',
					value: 174781
				},
				{
					impactCategory: 'AK',
					category: '≥80',
					value: 12503
				},
				{
					impactCategory: 'AZ',
					category: '≥80',
					value: 254716
				},
				{
					impactCategory: 'AR',
					category: '≥80',
					value: 113468
				},
				{
					impactCategory: 'CA',
					category: '≥80',
					value: 1311374
				},
				{
					impactCategory: 'CO',
					category: '≥80',
					value: 155175
				},
				{
					impactCategory: 'CT',
					category: '≥80',
					value: 159475
				},
				{
					impactCategory: 'DE',
					category: '≥80',
					value: 35937
				},
				{
					impactCategory: 'DC',
					category: '≥80',
					value: 19658
				},
				{
					impactCategory: 'FL',
					category: '≥80',
					value: 1019566
				},
				{
					impactCategory: 'GA',
					category: '≥80',
					value: 269182
				},
				{
					impactCategory: 'HI',
					category: '≥80',
					value: 66060
				},
				{
					impactCategory: 'ID',
					category: '≥80',
					value: 54234
				},
				{
					impactCategory: 'IL',
					category: '≥80',
					value: 478948
				},
				{
					impactCategory: 'IN',
					category: '≥80',
					value: 243131
				},
				{
					impactCategory: 'IA',
					category: '≥80',
					value: 143583
				},
				{
					impactCategory: 'KS',
					category: '≥80',
					value: 117637
				},
				{
					impactCategory: 'KY',
					category: '≥80',
					value: 155074
				},
				{
					impactCategory: 'LA',
					category: '≥80',
					value: 152063
				},
				{
					impactCategory: 'ME',
					category: '≥80',
					value: 62007
				},
				{
					impactCategory: 'MD',
					category: '≥80',
					value: 208079
				},
				{
					impactCategory: 'MA',
					category: '≥80',
					value: 288408
				},
				{
					impactCategory: 'MI',
					category: '≥80',
					value: 398303
				},
				{
					impactCategory: 'MN',
					category: '≥80',
					value: 215985
				},
				{
					impactCategory: 'MS',
					category: '≥80',
					value: 100689
				},
				{
					impactCategory: 'MO',
					category: '≥80',
					value: 242554
				},
				{
					impactCategory: 'MT',
					category: '≥80',
					value: 41920
				},
				{
					impactCategory: 'NE',
					category: '≥80',
					value: 78504
				},
				{
					impactCategory: 'NV',
					category: '≥80',
					value: 82273
				},
				{
					impactCategory: 'NH',
					category: '≥80',
					value: 52552
				},
				{
					impactCategory: 'NJ',
					category: '≥80',
					value: 367432
				},
				{
					impactCategory: 'NM',
					category: '≥80',
					value: 74393
				},
				{
					impactCategory: 'NY',
					category: '≥80',
					value: 804091
				},
				{
					impactCategory: 'NC',
					category: '≥80',
					value: 342497
				},
				{
					impactCategory: 'ND',
					category: '≥80',
					value: 32206
				},
				{
					impactCategory: 'OH',
					category: '≥80',
					value: 481890
				},
				{
					impactCategory: 'OK',
					category: '≥80',
					value: 138055
				},
				{
					impactCategory: 'OR',
					category: '≥80',
					value: 157153
				},
				{
					impactCategory: 'PA',
					category: '≥80',
					value: 615069
				},
				{
					impactCategory: 'RI',
					category: '≥80',
					value: 51021
				},
				{
					impactCategory: 'SC',
					category: '≥80',
					value: 166727
				},
				{
					impactCategory: 'SD',
					category: '≥80',
					value: 38540
				},
				{
					impactCategory: 'TN',
					category: '≥80',
					value: 227483
				},
				{
					impactCategory: 'TX',
					category: '≥80',
					value: 732179
				},
				{
					impactCategory: 'UT',
					category: '≥80',
					value: 70711
				},
				{
					impactCategory: 'VT',
					category: '≥80',
					value: 26656
				},
				{
					impactCategory: 'VA',
					category: '≥80',
					value: 274606
				},
				{
					impactCategory: 'WA',
					category: '≥80',
					value: 242589
				},
				{
					impactCategory: 'WV',
					category: '≥80',
					value: 79201
				},
				{
					impactCategory: 'WI',
					category: '≥80',
					value: 241747
				},
				{
					impactCategory: 'WY',
					category: '≥80',
					value: 19682
				},
				{
					impactCategory: 'PR',
					category: '≥80',
					value: 148963
				}
			]
	}
</script>

<StackedBarChart chartData={mockStackedBarData()} />
<Sankey links={subtasksLinks} />
<Sunburst bind:selectedTask hierarchy={subtaskHierarchy} />
