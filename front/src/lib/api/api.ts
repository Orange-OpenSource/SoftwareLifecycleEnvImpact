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
import { dev } from '$app/environment';
import { env } from '$env/dynamic/public';
import type { PatchDocument } from '$lib/api/dataModel';

const base = (dev ? env.PUBLIC_API_DEV_URL + ':' + env.PUBLIC_API_DEV_PORT : '') + '/api/v1';

async function send(method: string, path: string, data: unknown = undefined) {
	const opts: RequestInit = { method, headers: {} };
	opts.method = method;
	opts.headers = {
		'Content-Type': 'application/json'
	};
	if (method != 'GET') {
		opts.body = JSON.stringify(data);
	}

	/*
	if (token) {
		opts.headers['Authorization'] = `Token ${token}`;
	}
	*/
	const res = await fetch(`${base}/${path}`, opts);
	// if (!res.ok) throw new Error(await res.text());
	// if (!res.ok) throw new Error((await res.json())['detail']);

	if (!res.ok) {
		const json = await res.json();
		if (json['detail']) {
			throw new Error(json['detail']);
		}
		throw new Error(JSON.stringify(json));
	}
	return res;
}

export async function get(path: string) {
	return send('GET', path);
}

export async function del(path: string) {
	return send('DELETE', path);
}

export async function post(path: string, data: unknown) {
	return send('POST', path, data);
}

export async function put(path: string, data: unknown) {
	return send('PUT', path, data);
}

export async function patch(path: string, data: PatchDocument[]) {
	return send('PATCH', path, data); // Json patch has to be in an array
}
