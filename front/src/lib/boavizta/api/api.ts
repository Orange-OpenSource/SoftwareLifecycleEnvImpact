const base = 'https://api.boavizta.org';

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

export async function post(path: string, data) {
	return send('POST', path, data);
}
