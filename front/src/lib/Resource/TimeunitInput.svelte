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
	import { TIME_UNITS } from '$lib/api/dataModel';

	/*Bound var*/
	export let inputUnit: string | undefined;

	export let isRequired: boolean;
	export let isInvalid: any;

	// Copy object to split unit string with businessDay boolean
	let inputUnitLayout = inputUnit?.replace('business_', '');
	let businessDay = inputUnit?.includes('business_');

	// Update inputUnit with business_ prefix or not following checkbox value
	$: inputUnit = businessDay ? 'business_' + inputUnitLayout : inputUnitLayout;
</script>

<select bind:value={inputUnitLayout} class="form-control {isInvalid ? 'is-invalid' : ''}" id="inputUnit" required={isRequired}>
	<option />
	{#each TIME_UNITS as unit}
		<option value={unit}>
			{unit}
		</option>
	{/each}
</select>
<!-- Only display for week month or year -->
{#if inputUnitLayout == 'week' || inputUnitLayout == 'month' || inputUnitLayout == 'year'}
	<div class="form-check">
		<input class="form-check-input" type="checkbox" bind:checked={businessDay} id="timeInputBusiness" />
		<label class="form-check-label" for="timeInputBusiness">Business day</label>
	</div>
{/if}
