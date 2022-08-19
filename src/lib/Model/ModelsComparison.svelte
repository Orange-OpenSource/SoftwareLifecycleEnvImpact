<script lang="ts">
	import type { Model } from 'src/model/model';
	export let models: Model[];
</script>

{#each models as model}
	{model.name}
{/each}
