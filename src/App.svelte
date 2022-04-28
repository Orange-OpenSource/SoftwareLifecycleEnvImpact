<script lang="ts">
	import { Router, Route } from "svelte-navigator";
    import { store } from './stores';
	import SelectProject from "./views/SelectProject.svelte";
	import CompareModels from "./views/CompareModels.svelte";
	import Login from "./views/Login.svelte";
	import ViewProject from "./views/ViewProject.svelte";
	import ModifyModel from "./views/ModifyModel.svelte";
	import TopBarComponent from "./components/TopBarComponent.svelte";

	let modelsContent = [];
	let model_id;
</script>

<Router>
	<main>
		<header>
			<nav class="navbar navbar-expand-lg navbar-light indigo">
				<div class="container-fluid">
				  Software Lifecycle Environmental Impact
				  <TopBarComponent bind:model_id={model_id} bind:modelsContent={modelsContent}></TopBarComponent>
				</div>
			</nav>
		</header>
 
		{#if $store != null }
			<Route path="/">
				<SelectProject />
			</Route>

			<Route path="compare">
				<CompareModels />
			</Route>

			<Route path="modify/:id" let:params>
				<ModifyModel idModels={params.id}/>
			</Route>

			<Route path="modify">
				<ModifyModel idModels={-1}/>
			</Route>

			<Route path="view/:id" let:params>
				<ViewProject bind:model_id={model_id} idProject={params.id} bind:modelsContent={modelsContent}/>
			</Route>
		{:else }
			<Login />
		{/if}
	</main>
</Router>