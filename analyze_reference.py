#!/usr/bin/env python3
import re

with open(r'E:\恒生科技\view-source_https___lego.348349.xyz_reports_viewer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找关键函数
# 搜索 directoryMap 初始化
idx = content.find('directoryMap')
if idx > 0:
    print("=== directoryMap ===")
    print(content[idx:idx+500])
    print()

# 搜索 onclick 处理
idx = content.find('onclick')
if idx > 0:
    print("=== onclick ===")
    print(content[idx:idx+300])
    print()

# 搜索 fetch 相关
idx = content.find('fetch(')
if idx > 0:
    print("=== fetch ===")
    print(content[idx:idx+300])
    print()

# 搜索 loadReport 函数
idx = content.find('loadReport(')
if idx > 0:
    print("=== loadReport ===")
    print(content[idx:idx+500])
    print()
