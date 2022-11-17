<script lang="ts">
	import type { Model } from '$lib/api/model/model';

	export let models: Model[];
</script>

<!-- TODO -->
<!-- {#each models as model}
	{#if impactByResource != undefined}
		<ul>
			{#each Object.entries(impactByResource) as [key, value]}
				<li>
					{key}
					<ImpactByIndicator impact={value} />
				</li>
			{/each}
		</ul>
	{/if}
{/each} -->
