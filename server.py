#!/usr/bin/env python3
"""
简单的HTTP服务器，用于提供股票报告文件访问
"""

import http.server
import socketserver
import os
import json
from pathlib import Path
import urllib.parse

PORT = 8000
DIRECTORY = Path(r"E:\恒生科技")

class ReportHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 允许跨域请求（如果需要）
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # 解析请求路径
        parsed_path = urllib.parse.urlparse(self.path)
        request_path = parsed_path.path.lstrip('/')

        # 处理根路径
        if request_path == '' or request_path == 'index.html' or request_path == 'reader.html':
        self.serve_file('reader_server.html')
        elif request_path == 'api/list':
            self.serve_file_list()
        elif request_path == 'api/file':
            self.serve_file_content(request_path)
        else:
            # 尝试直接提供文件
            file_path = DIRECTORY / request_path
            if file_path.exists() and file_path.is_file():
                self.serve_file_direct(file_path)
            else:
                self.send_error(404, "File not found")

    def serve_file(self, filename):
        file_path = DIRECTORY / filename
        if file_path.exists():
            self.serve_file_direct(file_path)
        else:
            self.send_error(404, f"File not found: {filename}")

    def serve_file_direct(self, file_path):
        """直接提供文件"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            # 确定内容类型
            if file_path.suffix == '.html':
                content_type = 'text/html; charset=utf-8'
            elif file_path.suffix == '.css':
                content_type = 'text/css; charset=utf-8'
            elif file_path.suffix == '.js':
                content_type = 'application/javascript; charset=utf-8'
            elif file_path.suffix == '.md':
                content_type = 'text/markdown; charset=utf-8'
            elif file_path.suffix == '.json':
                content_type = 'application/json; charset=utf-8'
            else:
                content_type = 'text/plain; charset=utf-8'

            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error serving file: {e}")

    def serve_file_list(self):
        """返回文件列表"""
        reports_data = []

        # 扫描所有报告文件夹
        for item in DIRECTORY.iterdir():
            if not item.is_dir():
                continue

            folder_name = item.name
            if not folder_name.startswith('STOCK_') and not folder_name.startswith('CHINA_'):
                continue

            # 扫描文件夹中的md文件
            md_files = []
            for md_file in item.rglob('*.md'):
                rel_path = md_file.relative_to(DIRECTORY)
                md_files.append({
                    'name': md_file.name,
                    'displayName': self.get_display_name(md_file.name),
                    'path': str(rel_path).replace('\\', '/'),
                    'size': md_file.stat().st_size
                })

            if md_files:
                reports_data.append({
                    'id': folder_name,
                    'name': self.get_report_name(folder_name),
                    'folder': folder_name,
                    'files': md_files
                })

        response = json.dumps(reports_data, ensure_ascii=False, indent=2)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def serve_file_content(self, request_path):
        """返回文件内容"""
        # 从查询参数获取文件路径
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(request_path).query)
        file_path = query_params.get('path', [''])[0]

        full_path = DIRECTORY / file_path

        if full_path.exists() and full_path.is_file():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                self.send_response(200)
                self.send_header('Content-Type', 'text/markdown; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Error reading file: {e}")
        else:
            self.send_error(404, f"File not found: {file_path}")

    def get_display_name(self, filename):
        """获取文件的友好显示名称"""
        display_names = {
            'README.md': '概述',
            '00_Executive_Summary.md': '00_执行摘要',
            '01_Business_Foundation.md': '01_业务基础',
            '02_Industry_Analysis.md': '02_行业分析',
            '03_Business_Breakdown.md': '03_业务分解',
            '04_Financial_Quality.md': '04_财务质量',
            '05_Governance_Analysis.md': '05_治理分析',
            '06_Market_Sentiment.md': '06_市场情绪',
            '07_Valuation_Moat.md': '07_估值护城河',
            '08_Final_Synthesis.md': '08_综合分析',
            '2025_Financial_Update.md': '2025财务更新',
        }
        return display_names.get(filename, filename.replace('.md', ''))

    def get_report_name(self, folder_name):
        """获取报告的友好名称"""
        # 这里可以添加一个映射，或者直接使用文件夹名
        return folder_name

def main():
    os.chdir(DIRECTORY)

    print(f"Starting server at http://localhost:{PORT}")
    print(f"Serving directory: {DIRECTORY}")
    print("Press Ctrl+C to stop")

    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(('', PORT), ReportHTTPRequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == '__main__':
    main()
