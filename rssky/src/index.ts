import {
	HTML_BAD_REQUEST,
	HTML_METHOD_NOT_ALLOWED,
	HTML_NOT_FOUND_MISSING_FILE,
	HTML_NOT_FOUND_ROUTE,
} from './templates/4xx';

import { HTML_ROOT } from './templates/root';

export default {
	async fetch(
		request: Request, 
		env: Env,
		ctx: ExecutionContext
	): Promise<Response> {
		// 输入验证
		if (!request || !request.url) {
			return new Response(HTML_BAD_REQUEST, {
				status: 400,
				headers: { 'Content-Type': 'text/html; charset=UTF-8' },
			});
		}

		if (request.method !== 'GET') {
			return new Response(HTML_METHOD_NOT_ALLOWED, {
				status: 405,
				headers: { 'Content-Type': 'text/html; charset=UTF-8' },
			});
		}

		const url = new URL(request.url);
		const { pathname } = url;

		// 处理根路径
		if (pathname === '/') {
			return new Response(HTML_ROOT, {
				headers: { 'Content-Type': 'text/html; charset=UTF-8' },
			});
		}

		// 路由与文件名解析
		const lastSlashIndex: number = pathname.lastIndexOf('/');
		let route: string;
		let fileName: string;

		if (lastSlashIndex === -1) {
			route = pathname;
			fileName = '';
		} else {
			route = pathname.substring(0, lastSlashIndex);
			fileName = pathname.substring(lastSlashIndex + 1);
		}

		// 检查 fileName 是否符合 *.* 格式
		if (!fileName.includes('.')) {
			return new Response(HTML_NOT_FOUND_MISSING_FILE, {
				status: 404,
				headers: { 'Content-Type': 'text/html; charset=UTF-8' },
			});
		}

		try {
			// 从 KV 存储获取目标基础 URL
			const targetBaseUrl: string | null = await env.KV_ROUTES.get(route);

			if (!targetBaseUrl) {
				return new Response(HTML_NOT_FOUND_ROUTE, {
					status: 404,
					headers: { 'Content-Type': 'text/html; charset=UTF-8' },
				});
			}

			// 构建目标 URL 并进行重定向
			const targetUrl: string = targetBaseUrl + fileName;
			return Response.redirect(targetUrl, 302);
		} catch (err) {
			return new Response(HTML_NOT_FOUND_ROUTE, {
				status: 404,
				headers: { 'Content-Type': 'text/html; charset=UTF-8' },
			});
		}
	},
};

