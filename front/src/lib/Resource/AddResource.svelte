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
	import Modal from '$lib/Modal.svelte';
	import { getImpactSources } from '$lib/api/impactSources';
	import { addResourceRequest } from '$lib/api/resource';
	import Error from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import type { ImpactSource, Activity } from '$lib/api/dataModel';

	/*Bound var*/
	export let activity: Activity;

	let showModal = false;

	let impactSourcesPromise = getImpactSources();
	let selectedImpactSource: ImpactSource;

	let error = '';
	$: showModal, clearModal(); //Clean error message when closing modal

	function clearModal() {
		error = '';
	}

	async function handleSubmit() {
		// TODO result not working due to async
		error = '';
		try {
			if (selectedImpactSource != null) {
				const res = await addResourceRequest(activity.id, selectedImpactSource);
				activity.resources.push(res);
				/*Redondant assignment to force Svelte to update components*/
				activity.resources = activity.resources;
				showModal = false;
			}
		} catch (e: any) {
			error = e.message;
		}
	}
</script>

<button on:click|stopPropagation={() => (showModal = true)} class="btn btn-link">Add resource</button>

<Modal bind:showModal>
	<span slot="title">Add new resource :</span>
	<form slot="body" on:submit|preventDefault={handleSubmit}>
		{#await impactSourcesPromise}
			<Spinner />
		{:then impactSources}
			<div class="row g-3">
				<div class="col-6">
					<label for="resourceName">Unit</label>
					<select class="form-select" bind:value={selectedImpactSource} required>
						{#each impactSources as impactSource}
							<option value={impactSource} class="form-check-input">{impactSource.name}</option>
						{/each}
					</select>
				</div>
				<div class="col-12">
					<button type="submit" data-dismiss="modal" class="btn btn-primary">Add resource</button>
				</div>
			</div>
		{:catch error}
			<Error message={error.message} />
		{/await}
	</form>
	{#if error}
		<Error message={error} />
	{/if}
</Modal>
