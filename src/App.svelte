<script lang="ts">
	import { Router, Route, Link } from "svelte-navigator";

	import SelectProject from "./views/SelectProject.svelte";
	import CompareModels from "./views/CompareModels.svelte";
	import Login from "./views/Login.svelte";
	import ViewProject from "./views/ViewProject.svelte";
	import ModifyModel from "./views/ModifyModel.svelte";
	import { store } from './stores';


	function logOut(){
		$store = null;
	}
</script>

<Router>
	<main>
		<header>
			<nav class="navbar navbar-expand-lg navbar-light indigo">
				<div class="container-fluid">
				  Software Lifecycle Environmental Impact
				  {#if $store != null }
				  <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				  </button>
				  <div class="collapse navbar-collapse" id="navbarNav">
					<ul class="navbar-nav">
					  <li class="nav-item">
						<Link class="nav-link" style="color:white;" to="/">Home</Link>
					  </li>
					  <li class="nav-item">
						<Link class="nav-link" style="color:white;" to="compare">Comparaison modèle</Link>
					  </li>
					  <li class="nav-item">
						
						<button type="button" on:click={logOut}>Log out</button>
						
					  </li>
					</ul>
				  </div>
				  {/if}
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
				<ViewProject idProject={params.id}/>
			</Route>
		{:else }
			<Login />
		{/if}
	</main>
</Router>