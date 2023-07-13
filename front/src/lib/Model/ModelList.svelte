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
	import { getLastUpdate } from '$lib/utils';
	import type { Model, Project } from '$lib/api/dataModel';

	import CreateModel from './CreateModel.svelte';
	import DeleteModel from './DeleteModel.svelte';
	import DuplicateModel from './DuplicateModel.svelte';
	import RenameModel from './RenameModel.svelte';

	/*Bound vars*/
	export let selectedModel: Model;
	export let project: Project;
	export let selectedModels: Model[];
	export let compareModels: boolean;
</script>

<div class="col">
	<div class="row">
		<div class="list-group list-group-flush">
			{#if project != undefined && project.models != undefined}
				{#each project.models as model, i}
					<button type="button" class="list-group-item list-group-item-action {selectedModel == model ? 'list-group-item-info' : ''}" on:click|stopPropagation={() => (selectedModel = model)}>
						<div class="row">
							<div class="col-1">
								<input type="checkbox" class="form-check-input" value={model} bind:group={selectedModels} name={String(model.id)} on:click|stopPropagation={() => {}} />
							</div>
							<div class="col-5">
								<h5>
									{model.name}
								</h5>
								<small>{getLastUpdate(model)}</small>
							</div>
							<div class="col-6">
								<RenameModel bind:model />
								{#if i != 0}
									<DeleteModel {model} bind:models={project.models} />
								{/if}
								<DuplicateModel {model} bind:models={project.models} bind:selectedModel />
							</div>
						</div>
					</button>
				{/each}
			{:else}
				No model
			{/if}

			<div class="list-group-item">
				<div class="row justify-content-center">
					<div class="col-5">
						<button on:click|stopPropagation={() => (compareModels = true)} type="button" class="btn btn-outline-primary" disabled={selectedModels.length <= 1}> Compare </button>
					</div>
					<div class="col-5">
						<CreateModel bind:project bind:selectedModel />
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
