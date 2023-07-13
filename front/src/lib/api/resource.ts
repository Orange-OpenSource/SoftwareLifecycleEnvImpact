/*
 * BSD 3-Clause License
 *
 * Copyright (c) 2017, Orange
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * * Redistributions of source code must retain the above copyright notice, this
 *   list of conditions and the following disclaimer.
 *
 * * Redistributions in binary form must reproduce the above copyright notice,
 *   this list of conditions and the following disclaimer in the documentation
 *   and/or other materials provided with the distribution.
 *
 * * Neither the name of the copyright holder nor the names of its
 *   contributors may be used to endorse or promote products derived from
 *   this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
import { type PatchDocument, type ImpactSource, type Resource, TIME_UNITS } from '$lib/api/dataModel';
import { patch, post, del } from './api';

export async function renameResourceRequest(resource: Resource, newName: string): Promise<Resource> {
	const patchDocument: PatchDocument = {
		op: 'replace',
		path: '/name',
		value: newName
	};
	const res = await patch('resources/' + resource.id, [patchDocument]);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function addResourceRequest(activityId: number, impact_source: ImpactSource) {
	let period;
	let amount = { value: 1, unit: impact_source.unit }; // create the quantity
	// Check if time needed
	impact_source.unit.split(/[*,/]/).forEach(function (unit) {
		unit = unit.trim();
		if (TIME_UNITS.indexOf(unit) > -1) {
			period = { value: 1, unit: unit }; // create the quantity for period
		} else {
			amount = { value: 1, unit: unit }; // redefine amount quantity without period
		}
	});

	const res = await post('resources', {
		name: impact_source.name,
		activity_id: activityId,
		impact_source_id: impact_source.id,
		amount: amount,
		period: period
	});
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function deleteResourceRequest(resource: Resource): Promise<Resource> {
	const res = await del('resources/' + resource.id);
	return res.text().then((json: string) => {
		return JSON.parse(json);
	});
}

export async function updateResourceAmountRequest(resource: Resource): Promise<Resource> {
	const patchDocument: PatchDocument[] = [
		{
			op: 'replace',
			path: '/amount',
			value: { value: resource.amount.value, unit: resource.amount.unit }
		}
	];
	if (resource.duration && resource.duration.value != undefined && resource.duration.unit != undefined)
		patchDocument.push({
			op: 'replace',
			path: '/duration',
			value: { value: resource.duration.value, unit: resource.duration.unit }
		});
	if (resource.frequency && resource.frequency.value != undefined && resource.frequency.unit != undefined)
		patchDocument.push({
			op: 'replace',
			path: '/frequency',
			value: { value: resource.frequency.value, unit: resource.frequency.unit }
		});
	if (resource.period && resource.period.value != undefined && resource.period.unit != undefined)
		patchDocument.push({
			op: 'replace',
			path: '/period',
			value: { value: resource.period.value, unit: resource.period.unit }
		});

	try {
		const res = await patch('resources/' + resource.id, patchDocument);
		return res.text().then((json: string) => {
			return JSON.parse(json);
		});
	} catch (e) {
		return Promise.reject({
			errors: JSON.parse(e.message)
		});
	}
}
