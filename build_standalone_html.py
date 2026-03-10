#!/usr/bin/env python3
"""
生成包含嵌入数据的独立HTML文件
"""

import json
from pathlib import Path

# 配置
BASE_DIR = Path(r"E:\恒生科技")
JSON_FILE = BASE_DIR / "reports_data.json"
OUTPUT_FILE = BASE_DIR / "reader_standalone.html"

# HTML模板 (分两部分)
HTML_PART1 = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>股票报告阅读器 (独立版)</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
            background: #0f0f14;
            color: #e0e0e0;
            height: 100vh;
            overflow: hidden;
        }

        .reader-container {
            display: flex;
            height: 100vh;
        }

        .sidebar {
            width: 300px;
            min-width: 300px;
            background: #1a1a1f;
            border-right: 1px solid #2a2a2f;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .sidebar-header {
            padding: 1rem;
            background: #1f1f25;
            border-bottom: 1px solid #2a2a2f;
        }

        .sidebar-header h1 {
            font-size: 1.1rem;
            color: #fff;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .search-box {
            position: relative;
        }

        .search-box input {
            width: 100%;
            padding: 0.6rem 0.8rem 0.6rem 2rem;
            font-size: 0.85rem;
            border: 1px solid #2a2a2f;
            border-radius: 8px;
            background: #0f0f14;
            color: #e0e0e0;
            outline: none;
            transition: all 0.2s;
        }

        .search-box input:focus {
            border-color: #4a9eff;
            box-shadow: 0 0 0 3px rgba(74, 158, 255, 0.1);
        }

        .search-icon {
            position: absolute;
            left: 0.75rem;
            top: 50%;
            transform: translateY(-50%);
            width: 14px;
            height: 14px;
            color: #666;
        }

        .nav-tabs {
            display: flex;
            border-bottom: 1px solid #2a2a2f;
            background: #1f1f25;
        }

        .nav-tab {
            flex: 1;
            padding: 0.6rem;
            text-align: center;
            cursor: pointer;
            border: none;
            background: transparent;
            color: #666;
            font-size: 0.75rem;
            transition: all 0.2s;
        }

        .nav-tab:hover {
            color: #999;
            background: #25252b;
        }

        .nav-tab.active {
            color: #4a9eff;
            background: #25252b;
            border-bottom: 2px solid #4a9eff;
        }

        .sidebar-content {
            flex: 1;
            overflow-y: auto;
            padding: 0.5rem;
        }

        .sidebar-content::-webkit-scrollbar {
            width: 6px;
        }

        .sidebar-content::-webkit-scrollbar-track {
            background: #0f0f14;
        }

        .sidebar-content::-webkit-scrollbar-thumb {
            background: #3a3a3f;
            border-radius: 3px;
        }

        .section-title {
            padding: 0.75rem 0.5rem 0.5rem;
            font-size: 0.7rem;
            color: #555;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
        }

        .tree-item {
            margin: 0.2rem 0;
        }

        .tree-header {
            display: flex;
            align-items: center;
            padding: 0.5rem 0.6rem;
            cursor: pointer;
            border-radius: 6px;
            transition: background 0.15s;
            user-select: none;
        }

        .tree-header:hover {
            background: #25252b;
        }

        .tree-header.active {
            background: #2a2a35;
        }

        .tree-icon {
            width: 18px;
            height: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 0.5rem;
            font-size: 0.65rem;
            color: #555;
            transition: transform 0.2s;
        }

        .tree-icon.expanded {
            transform: rotate(90deg);
            color: #4a9eff;
        }

        .tree-label {
            flex: 1;
            font-size: 0.85rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .tree-badge {
            font-size: 0.65rem;
            padding: 0.15rem 0.4rem;
            background: #2a2a2f;
            border-radius: 10px;
            color: #666;
        }

        .tree-children {
            margin-left: 0.75rem;
            display: none;
        }

        .tree-children.expanded {
            display: block;
        }

        .file-item {
            padding: 0.4rem 0.6rem 0.4rem 1.75rem;
            cursor: pointer;
            border-radius: 6px;
            font-size: 0.8rem;
            color: #888;
            transition: all 0.15s;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .file-item:hover {
            background: #25252b;
            color: #e0e0e0;
        }

        .file-item.active {
            background: #4a9eff;
            color: #fff;
        }

        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background: #0f0f14;
        }

        .content-header {
            padding: 0.75rem 1.5rem;
            background: #1a1a1f;
            border-bottom: 1px solid #2a2a2f;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.85rem;
            color: #666;
        }

        .breadcrumb span.current {
            color: #e0e0e0;
        }

        .breadcrumb-separator {
            color: #3a3a3f;
        }

        .btn {
            padding: 0.45rem 0.85rem;
            font-size: 0.8rem;
            border: 1px solid #2a2a2f;
            border-radius: 6px;
            background: #1f1f25;
            color: #999;
            cursor: pointer;
            transition: all 0.15s;
        }

        .btn:hover {
            background: #2a2a2f;
            border-color: #3a3a3f;
            color: #e0e0e0;
        }

        .content-body {
            flex: 1;
            overflow-y: auto;
            padding: 1.5rem;
        }

        .content-body::-webkit-scrollbar {
            width: 8px;
        }

        .markdown-content {
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.8;
            color: #b8b8b8;
        }

        .markdown-content h1 {
            font-size: 1.85rem;
            margin: 1.25rem 0 0.75rem;
            color: #fff;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #2a2a2f;
        }

        .markdown-content h2 {
            font-size: 1.45rem;
            margin: 1.5rem 0 0.75rem;
            color: #f0f0f0;
        }

        .markdown-content h3 {
            font-size: 1.2rem;
            margin: 1.25rem 0 0.5rem;
            color: #e8e8e8;
        }

        .markdown-content p {
            margin: 0.6rem 0;
        }

        .markdown-content a {
            color: #4a9eff;
            text-decoration: none;
        }

        .markdown-content code {
            background: #2a2a2f;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-family: 'Consolas', monospace;
            font-size: 0.85em;
            color: #e8b878;
        }

        .markdown-content pre {
            background: #1a1a1f;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1rem 0;
            border: 1px solid #2a2a2f;
        }

        .markdown-content pre code {
            background: transparent;
            padding: 0;
        }

        .markdown-content ul, .markdown-content ol {
            margin: 0.6rem 0;
            padding-left: 1.75rem;
        }

        .markdown-content blockquote {
            border-left: 3px solid #4a9eff;
            padding-left: 1rem;
            margin: 1rem 0;
            color: #666;
        }

        .markdown-content hr {
            border: none;
            border-top: 1px solid #2a2a2f;
            margin: 2rem 0;
        }

        .markdown-content table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 0.9rem;
        }

        .markdown-content th,
        .markdown-content td {
            border: 1px solid #2a2a2f;
            padding: 0.6rem 0.75rem;
            text-align: left;
        }

        .markdown-content th {
            background: #1f1f25;
            font-weight: 600;
            color: #e0e0e0;
        }

        .markdown-content tr:hover td {
            background: #1a1a1f;
        }

        .markdown-content strong {
            color: #fff;
        }

        .welcome-page {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            text-align: center;
            color: #666;
        }

        .welcome-page h2 {
            font-size: 1.5rem;
            color: #e0e0e0;
            margin-bottom: 1rem;
        }

        .loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #666;
        }

        .spinner {
            width: 36px;
            height: 36px;
            border: 3px solid #2a2a2f;
            border-top-color: #4a9eff;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 1rem;
            color: #555;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <div class="reader-container">
        <div class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <h1><span style="font-size: 1.2rem;">📊</span> 股票报告阅读器</h1>
                <div class="search-box">
                    <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                    <input type="text" id="searchInput" placeholder="搜索报告..." />
                </div>
            </div>

            <div class="nav-tabs">
                <button class="nav-tab active" data-tab="all">全部</button>
                <button class="nav-tab" data-tab="hk">港股</button>
                <button class="nav-tab" data-tab="us">美股</button>
                <button class="nav-tab" data-tab="cn">A股</button>
                <button class="nav-tab" data-tab="industry">行业</button>
            </div>

            <div class="sidebar-content" id="sidebarContent"></div>
        </div>

        <div class="main-content">
            <div class="content-header">
                <div class="breadcrumb" id="breadcrumb">
                    <span class="current">请选择一个文档开始阅读</span>
                </div>
                <div class="content-actions">
                    <button class="btn" id="toggleSidebar">导航</button>
                </div>
            </div>

            <div class="content-body" id="contentBody">
                <div class="welcome-page">
                    <div style="font-size: 3rem; margin-bottom: 1.25rem; opacity: 0.4;">📚</div>
                    <h2>股票报告阅读器</h2>
                    <p>从左侧导航栏选择一个报告文件夹</p>
                    <p>点击文档开始阅读</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        const EMBEDDED_DATA =
'''

HTML_PART2 = ''';

        let reportsData = EMBEDDED_DATA.reports;
        let filesContent = EMBEDDED_DATA.files;
        let currentTab = 'all';
        let expandedFolders = new Set();
        let currentReport = null;
        let currentFile = null;

        const sidebarContent = document.getElementById('sidebarContent');
        const contentBody = document.getElementById('contentBody');
        const breadcrumb = document.getElementById('breadcrumb');
        const searchInput = document.getElementById('searchInput');
        const toggleSidebar = document.getElementById('toggleSidebar');

        function init() {
            renderTree();
            setupEventListeners();
            console.log('已加载 ' + reportsData.length + ' 个报告，' + Object.keys(filesContent).length + ' 个文件');
        }

        function renderTree(filter) {
            sidebarContent.innerHTML = '';
            const filtered = filterReports(filter);
            if (filtered.length === 0) {
                sidebarContent.innerHTML = '<div class="empty-state"><div>没有找到匹配的报告</div></div>';
                return;
            }
            let lastMarket = '';
            filtered.forEach(report => {
                if (currentTab === 'all' && report.market !== lastMarket) {
                    const names = { hk: '港股', us: '美股', cn: 'A股', industry: '行业分析', other: '其他' };
                    const div = document.createElement('div');
                    div.className = 'section-title';
                    div.textContent = names[report.market] || report.market;
                    sidebarContent.appendChild(div);
                    lastMarket = report.market;
                }
                sidebarContent.appendChild(createReportItem(report));
            });
        }

        function createReportItem(report) {
            const item = document.createElement('div');
            item.className = 'tree-item';
            const expanded = expandedFolders.has(report.id);
            item.innerHTML = '<div class="tree-header ' + (expanded ? 'active' : '') + '" data-report="' + report.id + '">' +
                '<span class="tree-icon ' + (expanded ? 'expanded' : '') + '">▶</span>' +
                '<span class="tree-label">' + report.name + '</span>' +
                '<span class="tree-badge">' + report.files.length + '</span>' +
                '</div>' +
                '<div class="tree-children ' + (expanded ? 'expanded' : '') + '" id="children-' + report.id + '"></div>';
            item.querySelector('.tree-header').addEventListener('click', () => toggleFolder(report, item));
            return item;
        }

        function toggleFolder(report, item) {
            const children = item.querySelector('.tree-children');
            const icon = item.querySelector('.tree-icon');
            const header = item.querySelector('.tree-header');
            if (expandedFolders.has(report.id)) {
                expandedFolders.delete(report.id);
                children.classList.remove('expanded');
                icon.classList.remove('expanded');
                header.classList.remove('active');
            } else {
                expandedFolders.add(report.id);
                children.classList.add('expanded');
                icon.classList.add('expanded');
                header.classList.add('active');
                loadFiles(report, children);
            }
        }

        function loadFiles(report, container) {
            container.innerHTML = '';
            if (report.files.length === 0) {
                container.innerHTML = '<div class="empty-state"><div>该文件夹没有文档</div></div>';
                return;
            }
            const sorted = [...report.files].sort((a, b) => {
                if (a.displayName === '概述') return -1;
                if (b.displayName === '概述') return 1;
                const aNum = parseInt(a.name.match(/^\\d+/));
                const bNum = parseInt(b.name.match(/^\\d+/));
                if (!isNaN(aNum) && !isNaN(bNum)) return aNum - bNum;
                return a.displayName.localeCompare(b.displayName, 'zh');
            });
            sorted.forEach(file => {
                const div = document.createElement('div');
                div.className = 'file-item';
                div.dataset.path = file.path;
                div.innerHTML = '<span style="opacity:0.5">📄</span>' + file.displayName;
                div.addEventListener('click', () => loadDocument(report, file));
                container.appendChild(div);
            });
        }

        function loadDocument(report, file) {
            document.querySelectorAll('.file-item').forEach(i => i.classList.remove('active'));
            const active = document.querySelector('[data-path="' + file.path + '"]');
            if (active) active.classList.add('active');
            contentBody.innerHTML = '<div class="loading"><div class="spinner"></div></div>';
            breadcrumb.innerHTML = '<span>' + report.name + '</span><span class="breadcrumb-separator">/</span><span class="current">' + file.displayName + '</span>';
            const content = filesContent[file.path];
            if (content) {
                // 获取当前文件的文件夹路径
                const folderPath = file.path.substring(0, file.path.lastIndexOf('/'));
                contentBody.innerHTML = '<div class="markdown-content">' + parseMarkdown(content, folderPath) + '</div>';
                contentBody.scrollTop = 0;
            }
        }

        function parseMarkdownTable(html) {
            const lines = html.split('\\n');
            let result = [];
            let i = 0;

            while (i < lines.length) {
                const line = lines[i].trim();

                // 检测是否是管道符表格行（以|开头和结尾，且包含至少一个|）
                if (line.match(/^\\|.+\\|$/)) {
                    let tableRows = [];

                    // 检查是否是分隔行（只包含 |、-、:、空格）
                    const isSeparator = line.replace(/\\|/g, '').match(/^[\\s\\-:]*$/);

                    if (!isSeparator) {
                        // 如果第一行不是分隔行，开始收集表格行
                        tableRows.push(line);
                        i++;

                        while (i < lines.length) {
                            const nextLine = lines[i].trim();
                            if (!nextLine.match(/^\\|.+\\|$/)) {
                                break; // 不是表格行了，退出
                            }

                            // 检查是否是分隔行
                            const isNextSeparator = nextLine.replace(/\\|/g, '').match(/^[\\s\\-:]*$/);

                            if (isNextSeparator) {
                                i++; // 跳过分隔行
                            } else {
                                tableRows.push(nextLine);
                                i++;
                            }
                        }

                        // 生成表格HTML
                        if (tableRows.length > 0) {
                            // 表格前添加双换行（段落分隔）
                            if (result.length > 0 && result[result.length - 1] !== '') {
                                result.push('');
                            }
                            result.push('<table>');
                            tableRows.forEach((row, idx) => {
                                // 移除开头和结尾的|，然后按|分割
                                const cells = row.substring(1, row.length - 1).split('\\|').map(c => c.trim());
                                const tag = idx === 0 ? 'th' : 'td';
                                result.push('<tr>');
                                cells.forEach(cell => {
                                    result.push('<' + tag + '>' + cell + '</' + tag + '>');
                                });
                                result.push('</tr>');
                            });
                            result.push('</table>');
                            // 表格后添加双换行（段落分隔）
                            if (i < lines.length && lines[i].trim() !== '') {
                                result.push('');
                            }
                        }
                    } else {
                        // 第一行就是分隔行，当作普通文本处理
                        result.push(line);
                        i++;
                    }
                } else {
                    result.push(line);
                    i++;
                }
            }

            return result.join('\\n');
        }

        function parseMarkdown(md, folderPath) {
            // 先处理表格（生成HTML）
            let html = parseMarkdownTable(md);

            // 使用占位符保护已生成的HTML标签（使用不包含< >的占位符）
            const placeholders = [];
            const protectHTML = (text) => {
                return text.replace(/<[^>]+>/g, (match) => {
                    placeholders.push(match);
                    return '[[HTML' + (placeholders.length - 1) + ']]';
                });
            };

            // 保护表格HTML
            html = protectHTML(html);

            // 进行HTML转义（占位符不会被转义，因为没有< >）
            html = html.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

            // 恢复HTML标签
            html = html.replace(/\\[\\[HTML(\\d+)\\]\\]/g, (match, idx) => {
                return placeholders[idx];
            });

            // 处理代码块
            html = html.replace(/```(\\w*)\\n?([\\s\\S]*?)```/g, '<pre><code>$2</code></pre>');
            html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
            html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
            html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
            html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
            html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
            html = html.replace(/\\*\\*\\*(.+?)\\*\\*\\*/g, '<strong><em>$1</em></strong>');
            html = html.replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
            html = html.replace(/\\*(.+?)\\*/g, '<em>$1</em>');
            // 处理链接，添加文件夹路径
            html = html.replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, (match, text, url) => {
                // 如果是相对路径（不以http、https、#开头），添加文件夹路径
                if (!url.match(/^(https?:|\\/)/) && folderPath) {
                    url = './' + folderPath + '/' + url;
                }
                return '<a href="' + url + '" target="_blank">' + text + '</a>';
            });
            const lines = html.split('\\n');
            let inUl = false, result = [];
            for (let i = 0; i < lines.length; i++) {
                if (lines[i].match(/^\\* /) || lines[i].match(/^- /)) {
                    if (!inUl) { result.push('<ul>'); inUl = true; }
                    result.push('<li>' + lines[i].replace(/^[\\*\\-] /, '') + '</li>');
                } else {
                    if (inUl) { result.push('</ul>'); inUl = false; }
                    result.push(lines[i]);
                }
            }
            if (inUl) result.push('</ul>');
            html = result.join('\\n');
            html = html.replace(/^(\\d+)\\. (.+)$/gm, '<li>$2</li>');
            html = html.replace(/(<li>.*<\\/li>\\n?)+/g, '<ol>$&</ol>');
            html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');
            html = html.replace(/^---$/gm, '<hr>');
            html = html.replace(/\\n\\n/g, '</p><p>');
            html = '<p>' + html + '</p>';
            html = html.replace(/<p>\\s*<\\/p>/g, '');
            html = html.replace(/<p>(<h[1-6]>)/g, '$1');
            html = html.replace(/(<\\/h[1-6]>)<\\/p>/g, '$1');
            html = html.replace(/<p>(<ul>)/g, '$1');
            html = html.replace(/(<\\/ul>)<\\/p>/g, '$1');
            html = html.replace(/<p>(<ol>)/g, '$1');
            html = html.replace(/(<\\/ol>)<\\/p>/g, '$1');
            html = html.replace(/<p>(<pre>)/g, '$1');
            html = html.replace(/(<\\/pre>)<\\/p>/g, '$1');
            html = html.replace(/<p>(<blockquote>)/g, '$1');
            html = html.replace(/(<\\/blockquote>)<\\/p>/g, '$1');
            html = html.replace(/<p>(<hr>)<\\/p>/g, '$1');
            html = html.replace(/<p>(<li>)/g, '$1');
            html = html.replace(/<p>(<table>)/g, '$1');
            html = html.replace(/(<\\/table>)<\\/p>/g, '$1');

            // 将剩余换行转为br
            html = html.replace(/\\n/g, '<br>');

            // 彻底清理表格周围的 <br> 和 <p> 标签
            // 清理表格前的所有内容
            html = html.replace(/(<br>)*<\\/p><p>(<br>)*<table>/g, '<table>');
            html = html.replace(/<p>(<br>)*<table>/g, '<table>');
            html = html.replace(/(<br>)*<table>/g, '<table>');
            // 清理表格后的所有内容
            html = html.replace(/(<\\/table>)(<br>)*<p><p>(<br>)*/g, '</p></p>$1');
            html = html.replace(/(<\\/table>)(<br>)*<\\/p>/g, '$1</p>');
            html = html.replace(/(<\\/table>)(<br>)*/g, '$1');

            // 清理段落间多余的 <br>
            html = html.replace(/(<br>)*<\\/p><p>(<br>)*/g, '</p><p>');
            // 清理开头和结尾的 <br>
            html = html.replace(/^(<br>)+/, '');
            html = html.replace(/(<br>)+$/, '');
            return html;
        }

        function filterReports(filter) {
            let filtered = reportsData;
            if (currentTab !== 'all') filtered = filtered.filter(r => r.market === currentTab);
            if (filter) {
                const lower = filter.toLowerCase();
                filtered = filtered.filter(r => r.name.toLowerCase().includes(lower) || r.folder.toLowerCase().includes(lower));
            }
            return filtered;
        }

        function setupEventListeners() {
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.addEventListener('click', () => {
                    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    currentTab = tab.dataset.tab;
                    renderTree(searchInput.value);
                });
            });
            searchInput.addEventListener('input', (e) => renderTree(e.target.value));
            toggleSidebar.addEventListener('click', () => document.getElementById('sidebar').classList.toggle('open'));
        }

        init();
    </script>
</body>
</html>'''

def main():
    print("正在读取JSON数据...")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        json_data = f.read()

    print(f"JSON数据大小: {len(json_data) / (1024 * 1024):.2f} MB")
    print("正在生成独立HTML文件...")

    # 组合HTML
    html_content = HTML_PART1 + json_data + HTML_PART2

    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

    file_size = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"完成! 独立HTML文件: {OUTPUT_FILE}")
    print(f"文件大小: {file_size:.2f} MB")
    print(f"\n现在可以直接双击打开 {OUTPUT_FILE.name} 使用！")

if __name__ == '__main__':
    main()
