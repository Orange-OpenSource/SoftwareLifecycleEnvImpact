<script lang="ts">
	import { createActivityFromTemplateRequest, createActivityRequest } from '$lib/api/activity';
	import { getActivityTemplateRequest } from '$lib/api/activityTemplates';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import Modal from '$lib/Modal.svelte';
	import type { Activity, ActivityTemplate } from '$lib/api/dataModel';

	/* Bound var */
	export let parentActivity: Activity;

	let activityTemplates = getActivityTemplateRequest();
	let selectedTemplate: ActivityTemplate;
	let showModal = false;

	let activityName: string;

	let error: string = '';

	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
		activityName = '';
	}

	async function createActivity() {
		error = '';
		try {
			let res;
			if (selectedTemplate != null) {
				res = await createActivityFromTemplateRequest(activityName != undefined && activityName != '' ? activityName : selectedTemplate.name, parentActivity.id, selectedTemplate.id);
			} else if (activityName != undefined && activityName != '') {
				res = await createActivityRequest(activityName, parentActivity.id);
			}

			if (res) {
				parentActivity.subactivities.push(res);
				/*Redondant assignment to force Svelte to update components*/
				parentActivity.subactivities = parentActivity.subactivities;
				showModal = false;
			}
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-primary">Add subactivity</button>

<Modal bind:showModal>
	<span slot="title">Create new activity :</span>

	<form slot="body" on:submit|preventDefault={createActivity}>
		{#await activityTemplates}
			<Spinner />
		{:then activityTemplates}
			<div class="row g-3">
				<div class="col-12">
					<select id="templateSelect" class="form-select" bind:value={selectedTemplate}>
						<option value={null} disabled selected class="form-check-input"> -- Templates -- </option>
						{#each activityTemplates as template}
							<option value={template}>{template.name}</option>
						{/each}
					</select>
				</div>
				<div class="line-around">OR</div>
				<div class="col-12">
					<input placeholder="Activity name" class="form-control" bind:value={activityName} />
				</div>
				<div class="col-12">
					<button type="submit" class="btn btn-primary">Create activity</button>
				</div>
			</div>
			{#if error}
				<Error message={error} />
			{/if}
		{:catch error}
			<Error message={error.message} />
		{/await}
	</form>
</Modal>
