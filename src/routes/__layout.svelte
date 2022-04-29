<script lang="ts">
	import '../app.css';
</script>

<main>
	<header>
		<nav class="navbar navbar-expand-lg navbar-light indigo">
			<div id="header" class="container-fluid">
				Software Lifecycle Environmental Impact <span
					><a style="color:white; margin-right: 10px;" sveltekit:prefetch href="/login">Profile</a>
					<a style="color:white;" sveltekit:prefetch href="/">Home</a></span
				>
			</div>
		</nav>
	</header>

	<slot />
</main>
