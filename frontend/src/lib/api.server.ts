import { PRIVATE_BACKEND_URL } from '$env/static/private';

const DEFAULT_URL = 'http://localhost:8000';

export async function backendFetchServer(fetchFn: typeof fetch, path: string, init?: RequestInit) {
	const base = PRIVATE_BACKEND_URL || DEFAULT_URL;
	const res = await fetchFn(base + path, {
		...init,
		headers: { 'content-type': 'application/json', ...(init?.headers || {}) }
	});
	if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
	return res;
}