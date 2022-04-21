<script>
	import { Router, Route, Link } from "svelte-navigator";

	import SelectionProjet from "./SelectionProjet.svelte";
	import ComparaisonModele from "./ComparaisonModele.svelte";
	import Profil from "./Profil.svelte";
	import VisualisationProjet from "./VisualisationProjet.svelte";
	import ModificationModele from "./ModificationModele.svelte";
	
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
						<a class="nav-link" href="#"><Link to="visualisation">Visualisation projet</Link></a>
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

		<Route path="visualisation">
			<VisualisationProjet />
		</Route>
	</main>
</Router>

<style>

	main {
		text-align: center;
		padding: 0;
		max-width: 240px;
		margin: 0 auto;
		height: 100%;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

	.indigo {
		background-color: #8850e2;
		color: white;
	}
</style>