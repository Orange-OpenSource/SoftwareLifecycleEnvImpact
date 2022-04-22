<script lang="ts">
	import { Router, Route, Link } from "svelte-navigator";

	import SelectProject from "./views/SelectProject.svelte";
	import CompareModels from "./views/CompareModels.svelte";
	import Login from "./views/Login.svelte";
	import ViewProject from "./views/ViewProject.svelte";
	import ModifyModel from "./views/ModifyModel.svelte";
</script>

<Router>
	<main>
		<header>
			<nav class="navbar navbar-expand-lg navbar-light indigo">
				<div class="container-fluid">
				  Software Lifecycle Environmental Impact
				  <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				  </button>
				  <div class="collapse navbar-collapse" id="navbarNav">
					<ul class="navbar-nav">
					  <li class="nav-item">
						<a class="nav-link" href="#"><Link to="/">Home</Link></a>
					  </li>
					  <li class="nav-item">
						<a class="nav-link" href="#"><Link to="login">Profil</Link></a>
					  </li>
					  <li class="nav-item">
						<a class="nav-link" href="#"><Link to="compare">Comparaison modèle</Link></a>
					  </li>
					  <li class="nav-item">
						<a class="nav-link" href="#"><Link to="modify">Modification modèle</Link></a>
					  </li>
					</ul>
				  </div>
				</div>
			  </nav>
		</header>
 
		<Route path="/">
			<SelectProject />
		</Route>

		<Route path="login">
			<Login />
		</Route>

		<Route path="compare">
			<CompareModels />
		</Route>

		<Route path="modify">
			<ModifyModel />
		</Route>

		<Route path="view/:id" let:params>
			<ViewProject idProject={params.id}/>
		</Route>
	</main>
</Router>