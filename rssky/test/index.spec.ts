import { describe, it, expect } from 'vitest';
import handler from '../src/index';

import {
	HTML_BAD_REQUEST,
	HTML_METHOD_NOT_ALLOWED,
	HTML_NOT_FOUND_MISSING_FILE,
	HTML_NOT_FOUND_ROUTE,
} from '../src/templates/4xx';

import { HTML_ROOT } from '../src/templates/root';

describe('fetch handler', () => {
const env = {
	KV_ROUTES: {
		get: async (route: string) => {
			if (route === '/valid-route') {
				return 'https://example.com/';
			}
			return null;
		},
	},
};

it('should return 400 for invalid request', async () => {
	const response = await handler.fetch(null as any, env, {} as any);
	expect(response.status).toBe(400);
	expect(await response.text()).toBe(HTML_BAD_REQUEST);
});

it('should return 405 for non-GET request', async () => {
	const request = new Request('https://example.com', { method: 'POST' });
	const response = await handler.fetch(request, env, {} as any);
	expect(response.status).toBe(405);
	expect(await response.text()).toBe(HTML_METHOD_NOT_ALLOWED);
});

it('should return HTML_ROOT for root path', async () => {
	const request = new Request('https://example.com/');
	const response = await handler.fetch(request, env, {} as any);
	expect(response.status).toBe(200);
	expect(await response.text()).toBe(HTML_ROOT);
});

it('should return 404 for missing file in path', async () => {
	const request = new Request('https://example.com/route/');
	const response = await handler.fetch(request, env, {} as any);
	expect(response.status).toBe(404);
	expect(await response.text()).toBe(HTML_NOT_FOUND_MISSING_FILE);
});

it('should return 404 for route not found', async () => {
	const request = new Request('https://example.com/unknown-route/file.txt');
	const response = await handler.fetch(request, env, {} as any);
	expect(response.status).toBe(404);
	expect(await response.text()).toBe(HTML_NOT_FOUND_ROUTE);
});

it('should redirect to target URL for valid route and file', async () => {
	const request = new Request('https://example.com/valid-route/file.txt');
	const response = await handler.fetch(request, env, {} as any);
	expect(response.status).toBe(302);
	expect(response.headers.get('Location')).toBe('https://example.com/file.txt');
});
});