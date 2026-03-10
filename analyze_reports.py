#!/usr/bin/env python3
"""
分析股票报告，找出内容较少的报告（文件少于2个或总行数少于300行）
"""
import os
from pathlib import Path

def count_file_lines(file_path):
    """计算文件的行数"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception as e:
        return 0

def analyze_stock_folder(folder_path):
    """分析单个股票报告文件夹"""
    stock_name = os.path.basename(folder_path)

    # 获取所有文件
    files = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) and not item.startswith('.'):
            files.append(item_path)

    # 计算总行数
    total_lines = 0
    file_details = []
    for file_path in files:
        lines = count_file_lines(file_path)
        total_lines += lines
        file_details.append({
            'name': os.path.basename(file_path),
            'lines': lines
        })

    return {
        'stock_name': stock_name,
        'file_count': len(files),
        'total_lines': total_lines,
        'file_details': sorted(file_details, key=lambda x: x['lines'], reverse=True)
    }

def main():
    base_dir = r"E:\恒生科技"
    poor_reports = []

    # 获取所有STOCK_开头的文件夹
    stock_folders = []
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and item.startswith('STOCK_'):
            stock_folders.append(item_path)

    print(f"Found {len(stock_folders)} stock report folders")
    print("=" * 80)

    # 分析每个文件夹
    all_reports = []
    for folder in stock_folders:
        report = analyze_stock_folder(folder)
        all_reports.append(report)

        # 判断是否为差的报告
        if report['file_count'] < 2 or report['total_lines'] < 300:
            poor_reports.append(report)

    # 按总行数排序
    all_reports.sort(key=lambda x: x['total_lines'])
    poor_reports.sort(key=lambda x: x['total_lines'])

    # 输出结果
    print(f"\n总计分析 {len(all_reports)} 个股票报告")
    print(f"发现 {len(poor_reports)} 个差报告（文件<2个 或 总行数<300行）")
    print("=" * 80)

    # 生成报告文档
    output_file = os.path.join(base_dir, "差报告分析.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 股票报告质量分析\n\n")
        f.write(f"**分析时间**: 2026-03-10\n\n")
        f.write(f"**总计**: {len(all_reports)} 个股票报告\n\n")
        f.write(f"**差报告数量**: {len(poor_reports)} 个（文件<2个 或 总行数<300行）\n\n")
        f.write("---\n\n")

        f.write("## 差报告列表（按总行数排序）\n\n")
        f.write("| # | 股票代码 | 文件数 | 总行数 | 详细 |\n")
        f.write("|---|---------|-------|--------|------|\n")

        for i, report in enumerate(poor_reports, 1):
            reason = []
            if report['file_count'] < 2:
                reason.append(f"文件仅{report['file_count']}个")
            if report['total_lines'] < 300:
                reason.append(f"仅{report['total_lines']}行")
            f.write(f"| {i} | {report['stock_name']} | {report['file_count']} | {report['total_lines']} | {', '.join(reason)} |\n")

        f.write("\n---\n\n")
        f.write("## 差报告详细分析\n\n")

        for i, report in enumerate(poor_reports, 1):
            f.write(f"### {i}. {report['stock_name']}\n\n")
            f.write(f"- **文件数量**: {report['file_count']}\n")
            f.write(f"- **总行数**: {report['total_lines']}\n")
            f.write(f"- **问题**: ")
            issues = []
            if report['file_count'] < 2:
                issues.append(f"文件数量不足（仅{report['file_count']}个）")
            if report['total_lines'] < 300:
                issues.append(f"内容过少（仅{report['total_lines']}行）")
            f.write(f"{', '.join(issues)}\n\n")

            f.write("**文件列表**:\n\n")
            if report['file_details']:
                for detail in report['file_details']:
                    f.write(f"- `{detail['name']}`: {detail['lines']} 行\n")
            else:
                f.write("*无文件*\n")
            f.write("\n")

        f.write("---\n\n")
        f.write("## 所有报告统计（按行数排序，前20和后20）\n\n")

        f.write("### 内容最少的前20个报告\n\n")
        f.write("| 排名 | 股票代码 | 文件数 | 总行数 |\n")
        f.write("|------|---------|-------|--------|\n")
        for i, report in enumerate(all_reports[:20], 1):
            f.write(f"| {i} | {report['stock_name']} | {report['file_count']} | {report['total_lines']} |\n")

        f.write("\n### 内容最多的后20个报告\n\n")
        f.write("| 排名 | 股票代码 | 文件数 | 总行数 |\n")
        f.write("|------|---------|-------|--------|\n")
        for i, report in enumerate(all_reports[-20:], len(all_reports)-19):
            f.write(f"| {i} | {report['stock_name']} | {report['file_count']} | {report['total_lines']} |\n")

    print(f"\n报告已生成: {output_file}")

    # 在终端也显示差报告列表
    print("\n" + "=" * 80)
    print("差报告列表:")
    print("=" * 80)
    for i, report in enumerate(poor_reports, 1):
        issues = []
        if report['file_count'] < 2:
            issues.append(f"文件{report['file_count']}个")
        if report['total_lines'] < 300:
            issues.append(f"{report['total_lines']}行")
        print(f"{i:3}. {report['stock_name']:50} | 文件:{report['file_count']:2} | 行数:{report['total_lines']:4} | 问题: {', '.join(issues)}")

if __name__ == "__main__":
    main()
