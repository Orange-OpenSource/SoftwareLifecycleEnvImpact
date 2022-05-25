const base = 'http://127.0.0.1:5000/api/v1';

async function send({ method, path, data=''}) {
	const opts = { method, headers: {} };

	if (data) {
		opts.headers['Content-Type'] = 'application/json';
		opts.body = JSON.stringify(data);
	}

    /*
	if (token) {
		opts.headers['Authorization'] = `Token ${token}`;
	}
    */

	return fetch(`${base}/${path}`, opts)
		.then((r) => r.text())
		.then((json) => {
			try {
				return JSON.parse(json);
			} catch (err) {
				return json;
			}
		});
}

export async function get(path) {
	return send({ method: 'GET', path });
}

export async function del(path) {
	return send({ method: 'DELETE', path });
}

export async function post(path, data) {
	return send({ method: 'POST', path, data });
}

export async function put(path, data) {
	return send({ method: 'PUT', path, data });
}

export async function patch(path, data) {
	return send({ method: 'PATCH', path, data });
}
