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
	import AddResource from './AddResource.svelte';
	import DeleteResource from './DeleteResource.svelte';
	import Error from '$lib/Error.svelte';
	import ResourceInput from './ResourceInput.svelte';
	import type { Activity } from '$lib/api/dataModel';
	import Icon from '@iconify/svelte';

	/*Bound var*/
	export let activity: Activity;
	export let modify: boolean;

	let editResource = false;

	$: if (!modify) editResource = false;

	let error = '';
</script>

{#if error}
	<Error message={error} />
{/if}

<ul class="list-group list-group-flush list-group-numbered">
	{#if activity.resources != null}
		{#each activity.resources as resource}
			<li class="list-group-item d-flex p-0 bg-light">
				<div class="ms-2">
					<div class="d-flex justify-content-between">
						<div class="fw-bold">{resource.name}</div>
						{#if modify}
							<div class="d-flex">
								<button class="btn p-0" on:click|stopPropagation={() => (editResource = !editResource)}>
									<Icon icon="material-symbols:edit-outline" width="25" height="25" alt="Edit" loading="lazy" />
								</button>
								<DeleteResource bind:activity {resource} />
							</div>
						{/if}
					</div>
					<div class="ms-1">
						<ResourceInput bind:resource modify={editResource} />
					</div>
				</div>
			</li>
		{/each}
	{/if}
	{#if modify}
		<li class="list-group-item d-flex p-1 bg-light">
			<div class="ms-2">
				<AddResource bind:activity />
			</div>
		</li>
	{/if}
</ul>
