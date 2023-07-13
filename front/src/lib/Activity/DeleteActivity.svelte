<!-- BSD 3-Clause License

Copyright (c) 2017, Orange
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. -->
<script lang="ts">
	import { deleteActivityRequest } from '$lib/api/activity';
	import Modal from '$lib/Modal.svelte';
	import Error from '$lib/Error.svelte';
	import type { Activity } from '$lib/api/dataModel';
	import Icon from '@iconify/svelte';

	/* Bound var */
	export let parentActivity: Activity;
	export let selectedActivity: Activity;

	export let activity: Activity;

	let showModal = false;

	let error = '';
	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
	}

	async function deleteActivity() {
		error = '';
		try {
			await deleteActivityRequest(activity);
			parentActivity.subactivities = parentActivity.subactivities.filter((s) => s.id != activity.id);
			/*Redondant assignment to force Svelte to update components*/
			parentActivity.subactivities = parentActivity.subactivities;
			if (activity.id == selectedActivity.id) {
				selectedActivity = parentActivity;
			}
			showModal = false;
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button class="btn" on:click|stopPropagation={() => (showModal = true)}>
	<Icon icon="ion:trash-outline" width="25" height="25" alt="Delete" loading="lazy" />
</button>
<Modal bind:showModal>
	<span slot="title">Confirm delete</span>

	<form slot="body" on:submit|preventDefault={deleteActivity}>
		<div class="row g-3">
			<div class="col-12">
				<p>Are you sure you want to delete activity <strong>{activity.name}</strong> ?</p>
			</div>

			<div class="col-12">
				<button type="submit" data-dismiss="modal" class="btn btn-danger">Delete</button>
			</div>
		</div>
		{#if error}
			<Error message={error} />
		{/if}
	</form>
</Modal>
