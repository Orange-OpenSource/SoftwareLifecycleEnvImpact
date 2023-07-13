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
	import { createActivityRequest } from '$lib/api/activity';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import Modal from '$lib/Modal.svelte';
	import type { Activity } from '$lib/api/dataModel';

	/* Bound var */
	export let parentActivity: Activity;

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
			let res = await createActivityRequest(activityName, parentActivity.id);

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
		<div class="row g-3">
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
	</form>
</Modal>
