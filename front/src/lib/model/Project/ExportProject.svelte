<script lang="ts">
	import type { Project } from '$lib/model/api/model/project';
	import Error from '$lib/Error.svelte';
	import Icon from '@iconify/svelte';
	import { exportProjectRequest } from '$lib/model/api/project';
	import { exportJson } from '$lib/utils';

	export let project: Project;

	let error = '';

	async function exportProject() {
		error = '';
		try {
			const data = await exportProjectRequest(project.id);
			exportJson(data, project.name);
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={exportProject} class="btn btn-light">Export</button>
{#if error}
	<Error message={error} />
{/if}
