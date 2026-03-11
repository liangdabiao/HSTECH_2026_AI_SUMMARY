#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime

def count_lines_in_folder(folder_path):
    total_lines = 0
    file_count = 0
    file_details = []
    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path) and not item.startswith('.'):
                if item.endswith('.md') or item.endswith('.txt'):
                    with open(item_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        total_lines += lines
                        file_count += 1
                        file_details.append((item, lines))
    except Exception as e:
        pass
    return file_count, total_lines, file_details

# 获取所有STOCK_开头的文件夹
folders = [d for d in os.listdir('.') if d.startswith('STOCK_') and os.path.isdir(d)]

results = []
for folder in folders:
    file_count, total_lines, file_details = count_lines_in_folder(folder)
    results.append({
        'folder': folder,
        'file_count': file_count,
        'total_lines': total_lines,
        'file_details': file_details
    })

# 按总行数排序
results.sort(key=lambda x: x['total_lines'])

# 找出差报告：文件<2个 或 总行数<200行
poor_reports = [r for r in results if r['file_count'] < 2 or r['total_lines'] < 200]

# 生成Markdown报告
md_lines = []
md_lines.append("# 股票报告质量分析（200行标准）")
md_lines.append("")
md_lines.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
md_lines.append("")
md_lines.append(f"**总计**: {len(results)} 个股票报告")
md_lines.append("")
md_lines.append(f"**差报告数量**: {len(poor_reports)} 个（文件<2个 或 总行数<200行）")
md_lines.append("")
md_lines.append("---")
md_lines.append("")
md_lines.append("## 差报告列表（按总行数排序）")
md_lines.append("")
md_lines.append("| # | 股票代码 | 文件数 | 总行数 | 详细 |")
md_lines.append("|---|---------|-------|--------|------|")

for i, r in enumerate(poor_reports, 1):
    detail = ''
    if r['file_count'] < 2:
        detail = f'文件仅{r["file_count"]}个'
    if r['total_lines'] < 200:
        if detail:
            detail += f', 仅{r["total_lines"]}行'
        else:
            detail = f'仅{r["total_lines"]}行'
    md_lines.append(f"| {i} | {r['folder']} | {r['file_count']} | {r['total_lines']} | {detail} |")

md_lines.append("")
md_lines.append("---")
md_lines.append("")
md_lines.append("## 差报告详细分析")
md_lines.append("")

for i, r in enumerate(poor_reports, 1):
    md_lines.append(f"### {i}. {r['folder']}")
    md_lines.append("")
    md_lines.append(f"- **文件数量**: {r['file_count']}")
    md_lines.append(f"- **总行数**: {r['total_lines']}")
    problems = []
    if r['file_count'] < 2:
        problems.append(f"文件数量不足（仅{r['file_count']}个）")
    if r['total_lines'] < 200:
        problems.append(f"内容过少（仅{r['total_lines']}行）")
    md_lines.append(f"- **问题**: {', '.join(problems)}")
    md_lines.append("")
    md_lines.append("**文件列表**:")
    md_lines.append("")
    if r['file_details']:
        for filename, lines in r['file_details']:
            md_lines.append(f"- `{filename}`: {lines} 行")
    else:
        md_lines.append("*无文件*")
    md_lines.append("")

# 添加统计信息
md_lines.append("---")
md_lines.append("")
md_lines.append("## 所有报告统计")
md_lines.append("")
md_lines.append("### 内容最少的前30个报告")
md_lines.append("")
md_lines.append("| 排名 | 股票代码 | 文件数 | 总行数 |")
md_lines.append("|------|---------|-------|--------|")

for i, r in enumerate(results[:30], 1):
    md_lines.append(f"| {i} | {r['folder']} | {r['file_count']} | {r['total_lines']} |")

md_lines.append("")
md_lines.append("### 内容最多的后30个报告")
md_lines.append("")
md_lines.append("| 排名 | 股票代码 | 文件数 | 总行数 |")
md_lines.append("|------|---------|-------|--------|")

for i, r in enumerate(results[-30:], len(results) - 29):
    md_lines.append(f"| {i} | {r['folder']} | {r['file_count']} | {r['total_lines']} |")

# 写入文件
output_path = '差报告分析_200行标准.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print(f"报告已生成: {output_path}")
print(f"总计: {len(results)} 个文件夹")
print(f"差报告: {len(poor_reports)} 个")
