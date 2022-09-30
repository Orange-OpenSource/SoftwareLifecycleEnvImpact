<script lang="ts">
	import type { Project } from 'src/model/project';
	import Error from '$lib/Error.svelte';
	import Icon from '@iconify/svelte';
	import { exportProjectRequest } from '$lib/api/project';
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

<button on:click|stopPropagation={exportProject} class="btn btn-light"
	>Export
	<Icon icon="fluent:save-28-regular" /></button
>
{#if error}
	<Error message={error} />
{/if}
