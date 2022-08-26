<script lang="ts">
	export let models: Model[];
</script>

{#each models as model}
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
{/each}
