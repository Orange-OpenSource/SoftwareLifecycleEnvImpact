<script>
	import { page } from '$app/stores';
</script>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
	<div class="container-fluid">
		<a class="navbar-brand" href="/">
			<img src="/orange-logo.svg" width="50" height="50" alt="Orange logo" loading="lazy" />
		</a>
		<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon" />
		</button>
		<div class="collapse navbar-collapse" id="navbarNav">
			<ul class="navbar-nav">
				<li class="nav-item">
					<a rel="prefetch" href="/" class="nav-link" class:active={$page.url.pathname === '/'}>
						<i class="ion-compose" />Projects
					</a>
				</li>
			</ul>
		</div>
	</div>
</nav>
