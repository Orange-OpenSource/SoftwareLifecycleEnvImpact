<script lang="ts">
	import { getDefaultModelsName } from './api/server';
	let defaultServers = getDefaultModelsName();
</script>

<div>
	{#await defaultServers}
		<p>...waiting</p>
	{:then number}
		<p>{number}</p>
	{:catch error}
		<p style="color: red">{error.message}</p>
	{/await}
</div>
