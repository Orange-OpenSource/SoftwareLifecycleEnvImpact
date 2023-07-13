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
	import { page } from '$app/stores';
	import ActivityTree from '$lib/ActivityTree/ActivityTree.svelte';
	import ModelList from '$lib/Model/ModelList.svelte';
	import Impact from '$lib/Impact/Impact.svelte';
	import Split from 'split.js';
	import { onMount } from 'svelte';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import ModelComparison from '$lib/Model/Comparison/ModelsComparison.svelte';
	import { getProjectRequest } from '$lib/api/project';
	import type { Model, Activity } from '$lib/api/dataModel';

	let projectId = $page.params.id; // id of project clicked on (arg in URL "/project/X")

	let projectPromise = getProjectRequest(+projectId).then((res) => {
		if (res.models != null) {
			selectedModel = res.models[0];
		}
		return res;
	});

	let selectedModel: Model;
	let selectedModels: Model[] = [];
	let selectedActivity: Activity;

	let split: Split.Instance;

	let compareModels = false;

	$: selectedModel, updateSelectedActivity();

	$: selectedModels, updateComparison();

	$: compareModels,
		() => {
			/*Update screen layout to two or three columns if comparison is activated*/
			if (compareModels) setTwoColumnsSplit();
			else setThreeColumnsSplit();
		};

	function updateComparison() {
		/*Deactivate model comparison if less than two are selected*/
		if (selectedModels.length < 2) compareModels = false;
	}

	function updateSelectedActivity() {
		/*Select a model root activity as selected activity to display the complete model impacts*/
		if (selectedModel != undefined) {
			selectedActivity = selectedModel.root_activity;
		}
	}

	function setTwoColumnsSplit() {
		if (split) split.destroy();
		split = Split(['#split-0', '#split-1'], {
			sizes: [25, 75],
			minSize: 0,
			snapOffset: 200
		});
	}

	async function setThreeColumnsSplit() {
		if (split) split.destroy();
		split = Split(['#split-0', '#split-1', '#split-2'], {
			sizes: [25, 50, 25],
			minSize: [0, 450, 200],
			snapOffset: 200,
			onDrag: function () {
				//Function to hide split
				for (let i = 0; i < 3; i++) {
					let element = document.getElementById('split-' + i);
					if (element != null) {
						if (element.offsetWidth === 0) {
							element.style.visibility = 'hidden';
						} else {
							element.style.visibility = 'visible';
						}
					}
				}
			}
		});
		return;
	}

	onMount(async () => {
		setThreeColumnsSplit();
	});
</script>

<svelte:head>
	<title>Models</title>
</svelte:head>

<div class="split">
	<div id="split-0">
		<div class="col ps-2 sticky-top">
			<h2 class="title">My models</h2>
			{#await projectPromise}
				<Spinner />
			{:then project}
				<ModelList bind:selectedModel bind:selectedModels bind:compareModels {project} />
			{:catch error}
				<Error message={error.message} />
			{/await}
		</div>
	</div>

	{#if !compareModels}
		<div id="split-1" class="overflow-auto">
			<div class="ps-2">
				<ActivityTree bind:selectedActivity {selectedModel} />
			</div>
		</div>

		<div id="split-2">
			<div class="ps-2">
				<h2 class="title sticky-top">Impact</h2>
				<Impact bind:selectedActivity />
			</div>
		</div>
	{:else}
		<div id="split-1">
			<div class="ps-2 ">
				<h2 class="title">Compare</h2>
				<ModelComparison models={selectedModels} />
			</div>
		</div>
	{/if}
</div>
