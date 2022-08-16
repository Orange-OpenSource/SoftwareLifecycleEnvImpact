const base = 'http://127.0.0.1:5000/api/v1';

async function send(method: string, path: string, data = '') {
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
	return await fetch(`${base}/${path}`, opts);
}

export async function get(path: string) {
	return send('GET', path);
}

export async function del(path: string) {
	return send('DELETE', path);
}

export async function post(path: string, data: any) {
	return send('POST', path, data);
}

export async function put(path: string, data: any) {
	return send('PUT', path, data);
}

export async function patch(path: string, data: any) {
	return send('PATCH', path, data);
}
