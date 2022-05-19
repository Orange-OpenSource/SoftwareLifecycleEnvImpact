<script lang="ts">
	import { page } from '$app/stores';
	import { onMount, tick } from 'svelte';
	import { getModels, getTemplates, getModelImpact } from '$lib/controllers/RequestController';
	import HeaderButtonsModel from '$lib/components/HeaderButtonsModel.svelte';
	import { checkIfLogged } from '$lib/controllers/LoginController';
	import TiDelete from 'svelte-icons/ti/TiDelete.svelte';
	import TiPencil from 'svelte-icons/ti/TiPencil.svelte';
	import ModalConfirmDelete from '$lib/components/modals/ModalConfirmDelete.svelte';
	import { Chart, registerables } from 'chart.js';
	import { getLastUpdate } from '$lib/utils/dates';
	import { get2RowsSplitObject, get3RowsSplitObject } from '$lib/utils/splitobj';
	import { getChart } from '$lib/utils/chartobj';

	checkIfLogged();

	let CURRENT_MODEL_ID: number; // Id of the model which has to be displayed in the treeview and chart
	let CURRENT_MODEL_NAME: string; // Name of the model which has to be displayed in the root task of treeview
	let LIST_MODELS: any[] = []; // List of models which has to be displayed in "My models"

	let modify: boolean = false; // true if modifications are allowed (when "editing mode" is checked)
	let compare_screen: boolean = false; // true if user is on the comparaison screen (after click on "compare models")

	/* Components var */
	let ModalCreationModel: any;
	let ModalRenameModel: any;
	let RootTreeView: any;

	/* Var needed for chartjs */
	let labels: string[] = [];
	let data: any[] = [];
	let ctx: CanvasRenderingContext2D;
	let myChart: Chart;

	let splitjs: any; // Splitjs object

	let idProject = $page.params.id; // id of project clicked on (arg in URL "/view/X")
	let rootTreeView: any; // bound to component RootTreeView (to access function "updateTree" when needed)
	let templates: any; // var which contains all task templates when user want to create task or modify task name.

	/**
	 * Update chart when a modification in the treeview is detected.
	 *
	 * @param event	event details
	 */
	async function handleMessage(event: { detail: { text: any } }) {
		await updateChart();
	}

	/**
	 * Reload all the models and tasks informations.
	 */
	async function updateElements() {
		LIST_MODELS = await getModels(idProject);
		CURRENT_MODEL_ID = LIST_MODELS[0].id;
		CURRENT_MODEL_NAME = LIST_MODELS[0].name;
		if (!compare_screen) await rootTreeView.updateTree();
	}

	/**
	 * Update the model for which we want to see the treeview and impact.
	 *
	 * @param id	The id of the model (which will be linked to the tree and impact).
	 * @param name 	The name of the model (which will be linked to the root task input).
	 */
	async function updateModelId(id: any, name: string) {
		if (!compare_screen) {
			CURRENT_MODEL_ID = id;
			CURRENT_MODEL_NAME = name;

			await updateChart();
			await rootTreeView.updateTree();
		}
	}

	/**
	 * Switch to comparaison screen or goes back to initial screen
	 */
	async function comparePage() {
		if (!compare_screen) {
			splitjs.destroy();
			compare_screen = true;
			await tick();
			splitjs = get2RowsSplitObject(document);

			/*TODO handle comparaison charts depending on checked models
			let inputs = document.getElementsByClassName('modelsInput');

			for (var i = 0; i < inputs.length; i++) {
				// @ts-ignore
				console.log(inputs[i].value + ' ' + inputs[i].checked);
			}
			*/
		} else {
			splitjs.destroy();
			compare_screen = false;
			await tick();
			splitjs = get3RowsSplitObject(document);

			// @ts-ignore
			ctx = document.getElementById('myChart').getContext('2d');
			myChart = getChart(ctx, labels, data);
			await rootTreeView.updateTree();
		}
	}

	/**
	 * Update the charts when a checkbox is checked.
	 */
	async function updateComparaison() {
		let inputs = document.getElementsByClassName('modelsInput');

		/*TODO handle comparaison charts depending on checked models
		for (var i = 0; i < inputs.length; i++) {
			// @ts-ignore
			console.log(inputs[i].value + ' ' + inputs[i].checked);
		}
		*/
	}

	/**
	 * Update the chart with the new data.
	 */
	async function updateChart() {
		labels = [];
		data = [];
		let res: any = await getModelImpact(CURRENT_MODEL_ID);

		let dict: any = {};

		/* Run recursively through tree to get all task id and their corresponding impact in dictionary */
		function pushEachTaskAndImpactIntoDict(array: any) {
			dict[array.task.id] = array.environmental_impact;

			for (let i = 0; i < array.subtasks_impacts.length; i++) pushEachTaskAndImpactIntoDict(array.subtasks_impacts[i]);
		}

		pushEachTaskAndImpactIntoDict(res);

		if (res.task.subtasks.length) {
			for (let i in res.task.subtasks) {
				// if the subtask has an impact (some tasks still have empty `environmental_impact` field)
				if (Object.keys(dict[res.task.subtasks[i].id]).length) {
					let climate_change = dict[res.task.subtasks[i].id]['Climate change'].split(' ')[0];
					data.push(+climate_change);
					labels.push(res.task.subtasks[i].name);
				}
			}
		} else {
			// if the task has no subtask (= chart filled with 100% of task)
			if (Object.keys(dict[res.task.id]).length) {
				let climate_change = dict[res.task.id]['Climate change'].split(' ')[0];
				data.push(+climate_change);
				labels.push(res.task.name);
			}
		}

		labels = labels;
		data = data;

		myChart.data.labels = labels;
		myChart.data.datasets[0].data = data;
		myChart.update();
	}

	onMount(async function () {
		if (document.querySelector('div.modal-backdrop.fade.show')) document.querySelector('div.modal-backdrop.fade.show')!.remove();

		templates = await getTemplates();

		const moduletreeview = await import('$lib/components/RootTreeView.svelte');
		RootTreeView = moduletreeview.default;

		await updateElements();

		const module = await import('$lib/components/modals/ModalCreationModel.svelte');
		ModalCreationModel = module.default;

		const moduleRename = await import('$lib/components/modals/ModalRenameModel.svelte');
		ModalRenameModel = moduleRename.default;

		splitjs = get3RowsSplitObject(document);

		Chart.register(...registerables);
		// @ts-ignore
		ctx = document.getElementById('myChart').getContext('2d');
		myChart = getChart(ctx, labels, data);

		await updateChart();
	});
</script>

<svelte:head>
	<title>Models</title>
</svelte:head>

<div class="split">
	<div id="split-0">
		<h2 class="title">My models</h2>

		<div class="list-group list-group-flush" style="margin-bottom : 5px;">
			{#each LIST_MODELS as model, i}
				<button type="button" class="list-group-item list-group-item-action model-content" on:click|stopPropagation={() => updateModelId(model.id, model.name)} style="padding-bottom: 20px">
					<div class="card-body d-flex justify-content-between" style="padding-bottom:0px">
						<div>
							<input on:click={updateComparaison} type="checkbox" class="modelsInput" value={model.id} name={model.id} />
							<span class="underline-on-hover">
								{model.name}
								{#if i == 0}
									<strong>(default)</strong>
								{/if}
							</span>
						</div>
						<div class="d-flex justify-content-center">
							<div on:click|stopPropagation={() => {}} type="button" data-bs-toggle="modal" data-bs-target="#modalRenameModel{model.id}" class="icon-grey">
								<TiPencil />
							</div>

							{#if i != 0}
								<div on:click|stopPropagation={() => {}} data-bs-toggle="modal" data-bs-target="#modalDeleteModel{model.id}" class="icon-red">
									<TiDelete />
								</div>
							{/if}
						</div>
					</div>
					<span class="d-flex align-items-start" style="color:grey; font-size : 12px">Last modified : {getLastUpdate(model)}</span>
				</button>

				<svelte:component this={ModalRenameModel} bind:LIST_MODELS bind:idProject bind:model bind:CURRENT_MODEL_NAME />

				<ModalConfirmDelete bind:CURRENT_MODEL_ID bind:CURRENT_MODEL_NAME bind:LIST_MODELS bind:idProject bind:model bind:rootTreeView />
			{/each}
		</div>

		<div class="row d-flex justify-content-evenly">
			<svelte:component this={ModalCreationModel} bind:CURRENT_MODEL_ID bind:CURRENT_MODEL_NAME bind:rootTreeView bind:modify bind:idProject bind:LIST_MODELS />
			<button on:click={comparePage} type="button" class="col-5 btn btn-outline-primary">Compare models</button>
		</div>
	</div>

	{#if !compare_screen}
		<div id="split-1">
			<HeaderButtonsModel bind:CURRENT_MODEL_ID bind:CURRENT_MODEL_NAME bind:modify bind:LIST_MODELS bind:idProject />

			<svelte:component this={RootTreeView} on:message={handleMessage} bind:this={rootTreeView} bind:modify bind:CURRENT_MODEL_ID bind:templates bind:myChart />
		</div>

		<div id="split-2">
			<h2 class="title">Impact by task</h2>

			<canvas id="myChart" width="400" height="400" />
		</div>
	{:else}
		<div id="split-1">
			<h2 class="title">Differences</h2>

			<!-- TODO canvas elements to show comparaison charts -->
		</div>
	{/if}
</div>
