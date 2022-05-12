<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { getModels, getModelInformations, deleteModel, getTemplates, getImpactByResource } from '$lib/controllers/RequestController';
	import RootTreeView from '$lib/components/RootTreeView.svelte';
	import HeaderButtonsModel from '$lib/components/HeaderButtonsModel.svelte';
	import { checkIfLogged } from '$lib/controllers/LoginController';
	import Split from 'split.js';
	import { browser } from '$app/env';
	import { goto } from '$app/navigation';
	import TiDelete from 'svelte-icons/ti/TiDelete.svelte';
	import TiPencil from 'svelte-icons/ti/TiPencil.svelte';
	import ModalConfirmDelete from '$lib/components/modals/ModalConfirmDelete.svelte';
	import { Chart, registerables } from 'chart.js';

	checkIfLogged();

	let idProject = $page.params.id;
	let models: string | any[] = [];
	let modelsContent: any = [];
	let modify = false;
	let model_id: any;
	let rootTreeView: any;
	let model_name: string;
	let ModalCreationModel: any;
	let ModalRenameModel: any;
	let templates: any;
	let labels: any[] = [];
	let data: any[] = [];
	let ctx: any;
	let myChart: any;

	/**
	 * Reload all the models and tasks informations.
	 */
	async function updateElements() {
		models = await getModels(idProject);
		modelsContent = [];
		for (var i = 0; i < models.length; i++) {
			let content = await getModelInformations(models[i].id);
			modelsContent.push(content);
		}
		modelsContent = modelsContent;
		model_id = models[0].id;
		model_name = models[0].name;
		await rootTreeView.updateTree();
	}

	/**
	 * Update the model for which we want to see the treeview.
	 *
	 * @param id	The id of the model (linked to the tree).
	 * @param name 	The name of the model (linked to the input).
	 */
	async function updateModelId(id: any, name: string) {
		model_id = id;
		model_name = name;
		await rootTreeView.updateTree();
	}

	function comparePage() {
		if (browser) {
			goto('/compare/' + idProject);
		}
	}

	function getDate(model: any) {
		let date;

		if (model.updated_at) {
			date = new Date(model.updated_at);
		} else {
			date = new Date(model.created_at);
		}

		return (
			(date.getDate() < 10 ? '0' : '') +
			date.getDate() +
			'/' +
			(date.getMonth() + 1 < 10 ? '0' : '') +
			(date.getMonth() + 1) +
			'/' +
			date.getFullYear() +
			' ' +
			date.getHours() +
			':' +
			(date.getMinutes() < 10 ? '0' : '') +
			date.getMinutes()
		);
	}

	/**
	 * Update the chart with the new data.
	 */
	function updateChart() {
		myChart.data.labels = labels;
		myChart.data.datasets[0].data = data;
		myChart.update();
	}

	onMount(async function () {
		if (document.querySelector('div.modal-backdrop.fade.show')) document.querySelector('div.modal-backdrop.fade.show')!.remove();

		await updateElements();
		templates = await getTemplates();

		const module = await import('$lib/components/modals/ModalCreationModel.svelte');
		ModalCreationModel = module.default;

		const moduleRename = await import('$lib/components/modals/ModalRenameModel.svelte');
		ModalRenameModel = moduleRename.default;

		Split(['#split-0', '#split-1', '#split-2'], {
			sizes: [25, 50, 25],
			minSize: 0,
			snapOffset: 150,
			onDrag: function () {
				for (let i = 0; i < 3; i++) {
					let element = document.getElementById('split-' + i);
					if (element!.offsetWidth === 0) {
						element!.style.visibility = 'hidden';
					} else {
						element!.style.visibility = 'visible';
					}
				}
			}
		});

		Chart.register(...registerables);

		labels = [];
		data = [];
		let res: any = await getImpactByResource(1);

		for (var item in res) {
			labels.push(item);
			data.push(res[item]);
		}
		labels = labels;
		data = data;

		// @ts-ignore
		ctx = document.getElementById('myChart').getContext('2d');
		myChart = new Chart(ctx, {
			type: 'pie',
			data: {
				labels: labels,
				datasets: [
					{
						label: 'My First Dataset',
						data: data,
						backgroundColor: ['rgb(255, 99, 132)', 'rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(153, 102, 255)', 'rgb(75, 192, 192)'],
						hoverOffset: 4
					}
				]
			}
		});
	});
</script>

<svelte:head>
	<title>Models</title>
</svelte:head>

<div class="split">
	<div id="split-0">
		<h2 class="title">My models</h2>

		<div class="list-group list-group-flush" style="margin-bottom : 5px;">
			{#each modelsContent as model, i}
				<button type="button" class="list-group-item list-group-item-action model-content" on:click|stopPropagation={() => updateModelId(model.id, model.name)} style="padding-bottom: 20px">
					<div class="card-body d-flex justify-content-between" style="padding-bottom:0px">
						<div>
							<input type="checkbox" class="modelsInput" name={model.id} />
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
					<span class="d-flex align-items-start" style="color:grey; font-size : 12px">Last modified : {getDate(model)}</span>
				</button>

				<svelte:component this={ModalRenameModel} bind:modelsContent bind:models bind:idProject bind:model bind:model_name />

				<ModalConfirmDelete bind:model_id bind:model_name bind:modelsContent bind:models bind:idProject bind:model bind:rootTreeView />
			{/each}
		</div>

		<div class="row d-flex justify-content-evenly">
			<svelte:component this={ModalCreationModel} bind:model_id bind:model_name bind:rootTreeView bind:modify bind:idProject bind:models bind:modelsContent />
			<button on:click={comparePage} type="button" class="col-5 btn btn-outline-primary">Compare models</button>
		</div>
	</div>

	<div id="split-1">
		<HeaderButtonsModel bind:model_id bind:model_name bind:modify bind:modelsContent bind:models bind:idProject />

		<RootTreeView bind:this={rootTreeView} bind:modify bind:model_id bind:templates bind:myChart />
	</div>

	<div id="split-2">
		<h2 class="title">Impact by resource</h2>

		<canvas id="myChart" width="400" height="400" />
	</div>
</div>
