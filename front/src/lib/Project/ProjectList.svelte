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
	import { onMount } from 'svelte';
	import { getLastUpdate } from '$lib/utils';
	import DeleteProject from './DeleteProject.svelte';
	import type { Project } from '$lib/api/dataModel';
	import ErrorComponent from '$lib/Error.svelte';
	import Spinner from '$lib/Spinner.svelte';
	import ExportProject from './ExportProject.svelte';
	import { getProjectsRequest } from '$lib/api/project';
	import RenameProject from './RenameProject.svelte';
	import CreateProject from './CreateProject.svelte';

	let projects: Project[];
	let error: string;

	onMount(async () => {
		/**
		 * Cannot use svelte promise logic as result cannot be binded to component
		 * (projects to delete project from list here)
		 */
		try {
			projects = await getProjectsRequest();
		} catch (e: any) {
			error = e.message;
		}
	});
</script>

<div class="col">
	<div class="row">
		{#if error}
			<ErrorComponent message={error} />
		{:else if projects}
			<div class="list-group list-group-flush">
				{#each projects as project}
					<div class="list-group-item list-group-item-action">
						<div class="row">
							<div class="col-8">
								<a id="redirect{project.id}" href="/project/{project.id}">
									<h5 class="mb-1">
										{project.name}
									</h5>
									<small>{getLastUpdate(project)}</small>
								</a>
							</div>

							<div class="col-4">
								<RenameProject bind:project />
								<DeleteProject bind:projects {project} />
								<ExportProject {project} />
							</div>
						</div>
					</div>
				{/each}
				<div class="list-group-item">
					<div class="row">
						<div class="col">
							<CreateProject />
						</div>
					</div>
				</div>
			</div>
		{:else}
			<Spinner />
		{/if}
	</div>
</div>
