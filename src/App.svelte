<script lang="ts">
	import { Router, Route, Link } from "svelte-navigator";

	import SelectionProjet from "./views/SelectionProjet.svelte";
	import ComparaisonModele from "./views/ComparaisonModele.svelte";
	import Profil from "./views/Profil.svelte";
	import VisualisationProjet from "./views/VisualisationProjet.svelte";
	import ModificationModele from "./views/ModificationModele.svelte";
	
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
						<a class="nav-link" href="#"><Link to="profile">Profil</Link></a>
					  </li>
					  <li class="nav-item">
						<a class="nav-link" href="#"><Link to="comparaison">Comparaison modèle</Link></a>
					  </li>

					  <li class="nav-item">
						<a class="nav-link" href="#"><Link to="modification">Modification modèle</Link></a>
					  </li>
					</ul>
				  </div>
				</div>
			  </nav>
		</header>
 

		<Route path="/">
			<SelectionProjet />
		</Route>

		<Route path="profile">
			<Profil />
		</Route>

		<Route path="comparaison">
			<ComparaisonModele />
		</Route>

		<Route path="modification">
			<ModificationModele />
		</Route>

		<Route path="visualisation/:id" let:params>
			<VisualisationProjet idProject={params.id}/>
		</Route>
	</main>
</Router>