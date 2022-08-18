import type { PatchDocument } from 'src/model/patchDocument';

const base = 'http://127.0.0.1:5000/api/v1';

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
	if (!res.ok) throw new Error((await res.json())['detail']);
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

export async function patch(path: string, data: PatchDocument) {
	return send('PATCH', path, [data]); // Json patch has to be in an array
}
