<script lang="ts">
	import type { Model } from '$lib/api/dataModel';
	import Impact from '$lib/Impact/Impact.svelte';

	export let models: Model[];
</script>

<div class="row">
	{#each models as model}
		<div class="col">
			<Impact selectedTask={model.root_task} />
		</div>
	{/each}
</div>
