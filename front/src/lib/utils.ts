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
import type { Model } from '$lib/api/dataModel';
import type { Project } from '$lib/api/dataModel';

/**
 * Returns the last updated date (or creation date if null).
 *
 * @param model the model or project with `created_at` and `updated_at` fields.
 * @returns 	the date under format : DD/MM/YYYY XX:XX
 */
export function getLastUpdate(model: Model | Project) {
	let date: Date;

	if (model.updated_at) {
		date = new Date(model.updated_at);
	} else {
		date = new Date(model.created_at);
	}

	return (
		(date.getDate() < 10 ? '0' : '') +
		date.getDate() +
		'/' +
		(date.getMonth() + 1 < 10 ? '0' : '') +
		(date.getMonth() + 1) +
		'/' +
		date.getFullYear() +
		' ' +
		(date.getHours() + 2) +
		':' +
		(date.getMinutes() < 10 ? '0' : '') +
		date.getMinutes()
	);
}

export function exportJson(data: string, fileName: string) {
	//Used to generate file only on click
	if (data == null || !data.length) {
		return null;
	}

	const blob = new Blob([data]);
	const link = document.createElement('a');
	if (link.download !== undefined) {
		const url = URL.createObjectURL(blob);
		link.setAttribute('href', url);
		link.setAttribute('download', fileName + '.json');
		link.style.visibility = 'hidden';
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}
}

export function exportSvg(data: string, fileName: string) {
	//Used to generate file only on click
	if (data == null || !data.length) {
		return null;
	}

	const blob = new Blob([data]);
	const link = document.createElement('a');
	if (link.download !== undefined) {
		const url = URL.createObjectURL(blob);
		link.setAttribute('href', url);
		link.setAttribute('download', fileName + '.svg');
		link.style.visibility = 'hidden';
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}
}
