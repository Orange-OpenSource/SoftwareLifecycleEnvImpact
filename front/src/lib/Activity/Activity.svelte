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
	import type { Model, Activity } from '$lib/api/dataModel';
	import { changeActivityParent } from '$lib/api/activity';
	import ResourceList from '$lib/Resource/ResourceList.svelte';

	import CreateActivity from './CreateActivity.svelte';
	import DeleteActivity from './DeleteActivity.svelte';
	import RenameActivity from './RenameActivity.svelte';

	/* Bound vars */
	export let activity: Activity;
	export let selectedActivity: Activity;
	export let parentActivity: Activity;

	export let modify: boolean;
	export let selectedModel: Model;

	export let draggedObject: DragObject = {};

	let draggingOver = false;

	$: dragging = draggedObject.activity != undefined;

	$: activity, updateImpact();

	function updateImpact() {
		// Little hack to trigger a re-draw of impacts by updating
		// the selectedActivity even if another one is modified
		selectedActivity = selectedActivity;
	}

	interface DragObject {
		activity?: Activity;
		oldParent?: Activity;
	}

	function handleDragOver(e) {
		draggingOver = true;
	}

	function handleDragLeave(e) {
		draggingOver = false;
	}

	function handleMouseDown(e) {
		// The the activity as draggable only when cliking on the header
		e.target.parentNode.setAttribute('draggable', 'true');
	}

	function handleMouseUp(e) {
		// When click on header over, activity is not draggable anymore
		e.target.parentNode.setAttribute('draggable', 'false');
	}

	function handleDragStart(e: any) {
		e.dataTransfer.dropEffect = 'move';
		draggedObject = {
			activity: activity,
			oldParent: parentActivity
		};
		// e.dataTransfer.setData('text', JSON.stringify(draggingObject));
	}

	async function handleDragDrop(e: any) {
		if (draggedObject.oldParent != undefined && draggedObject.activity != undefined) {
			let oldParent = draggedObject.oldParent!;
			let activityToMove = draggedObject.activity!;

			const res = await changeActivityParent(activityToMove, activity);
			if (res) {
				activityToMove.subactivities.forEach((_, index) => {
					activityToMove.subactivities[index].parent_activity_id = oldParent.id;
				});
				// Move card to this activity subactivities
				activity.subactivities.push(activityToMove);
				// Remove the card to move from its old parent
				oldParent.subactivities = oldParent.subactivities.filter((t) => t.id != activityToMove.id);

				/*Redondant assignment to force Svelte to update components*/
				activity.subactivities = activity.subactivities;
				oldParent.subactivities = oldParent.subactivities;

				// Clear the bound object
				draggedObject = {};
			}
		}
	}

	function handleDragEnd(e: any) {
		draggedObject = {};
		e.target.setAttribute('draggable', 'false'); //Activity not draggable anymore
	}
</script>

# BSD-3-Clause License # # Copyright 2017 Orange # # Redistribution and use in source and binary forms, with or without # modification, are permitted provided that the following conditions are met: #
# 1. Redistributions of source code must retain the above copyright notice, # this list of conditions and the following disclaimer. # # 2. Redistributions in binary form must reproduce the above
copyright notice, # this list of conditions and the following disclaimer in the documentation # and/or other materials provided with the distribution. # # 3. Neither the name of the copyright holder
nor the names of its contributors # may be used to endorse or promote products derived from this software # without specific prior written permission. # # THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT
HOLDERS AND CONTRIBUTORS "AS IS" # AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE # IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE # ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE # LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR # CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF # SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS # INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN # CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) # ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE # POSSIBILITY OF SUCH DAMAGE.

<div class={activity.parent_activity_id != null ? 'activity' : ''}>
	<!--Do not display the root activity as a nomrmal one but only its subactivities-->
	{#if activity.parent_activity_id != null}
		<!--Highlight border if activity selected-->
		<div
			on:click|stopPropagation={() => (selectedActivity = activity)}
			class="card bg-light {selectedActivity.id == activity.id ? 'border-primary' : ''}"
			on:dragstart={handleDragStart}
			on:dragend={handleDragEnd}
			style="width: fit-content;"
		>
			<div id="mydivheader" class="card-header" hidden={!modify || dragging}>
				<div class="d-flex justify-content-between">
					<div class="col-8" style="cursor: move;" on:mousedown={handleMouseDown} on:mouseup={handleMouseUp}>Click here to drag</div>
					<div class="col-2"><DeleteActivity {activity} bind:parentActivity bind:selectedActivity /></div>
				</div>
			</div>
			<div class="card-body">
				<div class="card-title">
					<div class="d-flex flex-row">
						<div class="p-0"><h5>{activity.name}</h5></div>
						{#if modify && !dragging}
							<div class="p-0">
								<RenameActivity bind:activity />
							</div>
						{/if}
					</div>
				</div>

				{#if !dragging}
					{#if activity.resources.length > 0 || modify}
						<ResourceList bind:activity {modify} />
					{/if}
				{/if}
			</div>
		</div>
	{/if}

	{#each activity.subactivities as subactivity}
		<svelte:self bind:activity={subactivity} bind:draggedObject bind:selectedActivity bind:parentActivity={activity} {modify} {selectedModel} />
	{/each}

	{#if draggedObject.activity != undefined && draggedObject.activity != activity && draggedObject.activity.parent_activity_id != activity.id}
		<div class="activity" on:drop={handleDragDrop} on:dragover={handleDragOver} on:dragleave={handleDragLeave}>
			<div class="col-8 card {draggingOver ? 'border-success' : ''}" style="min-width: 15rem;">
				<div class="card-body ">
					<small>Drop here</small>
				</div>
			</div>
		</div>
	{:else if modify}
		<!--"Add Activity" button as a activity in the tree-->
		<div class="activity">
			<CreateActivity bind:parentActivity={activity} />
		</div>
	{/if}
</div>
