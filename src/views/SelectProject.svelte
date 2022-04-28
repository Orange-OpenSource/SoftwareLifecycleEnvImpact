<script>
	import { Link } from "svelte-navigator";
	import { onMount } from "svelte";
	import {getOriginalModelId, getProjects, getModels, getModelInformations} from '../controllers/RequestController';
    import RootTreeView from '../components/RootTreeView.svelte';

	let projects = [], models = [], modelsContent = [];
	let modify = false;
	let model_id, rootTreeView;

	async function updatePreview(idProject) {
		model_id = await getOriginalModelId(idProject);
		
        await rootTreeView.updateTree();
	}

	async function updatePreviewModel(idModel) {
		model_id = idModel;
		
        await rootTreeView.updateTree();
	}

	onMount(async function () {
		projects = await getProjects();
		model_id = await getOriginalModelId(1);
		models = await getModels(1);
		for (var i = 0; i < models.length; i++) {
  			let content = await getModelInformations(models[i]);
			modelsContent.push(content);
		}
		modelsContent = modelsContent;
		await rootTreeView.updateTree();
	});
</script>

<div class="container">
    <div class="row">
		<div class="col-3 border-right">
			<h2 class="title">My projects</h2>

			<ul class="list-group list-group-flush ">
				{#each projects as project}
					<li class="list-group-item d-flex justify-content-between">
						<Link to="view/{project.id}" style="color:black;">{project.name}</Link>
						<button type="button" on:click={updatePreview(project.id)}>Preview</button>
					</li>
				{/each}
			</ul>

			<button type="button">
				<Link to="../modify" style="color:black; text-decoration: none; ">New project</Link>
			</button>
      	</div>
		<div class="col-3 border-right">
			<h2 class="title">My models</h2>

			<ul class="list-group list-group-flush">
                {#each modelsContent as model}
                    <li class="list-group-item d-flex justify-content-between">
                        <Link to="../../modify/{model.id}" style="color:black;">{model.name}</Link>
                        <button type="button" on:click={updatePreviewModel(model.id)}>Preview</button>
                    </li>
                {/each}
            </ul>
		</div>
      	<div class="col">
        	<h2 class="title">Preview</h2>

			<RootTreeView bind:this={rootTreeView} {modify} {model_id}></RootTreeView>
      	</div>
    </div>
</div>