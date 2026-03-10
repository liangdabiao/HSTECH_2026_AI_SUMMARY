#!/usr/bin/env python3
"""
生成 directory_map.js - 只包含文件结构，不包含内容
用于异步加载方式
"""
import json
from pathlib import Path

DIRECTORY = Path(r"E:\恒生科技")

def build_directory_map():
    """生成目录映射"""
    directory_map = {}

    # 扫描所有报告文件夹
    for item in DIRECTORY.iterdir():
        if not item.is_dir():
            continue

        folder_name = item.name
        if not folder_name.startswith('STOCK_') and not folder_name.startswith('CHINA_'):
            continue

        # 扫描文件夹中的文件
        for file_path in item.rglob('*'):
            if file_path.is_file():
                rel_path = str(file_path.relative_to(DIRECTORY)).replace('\\', '/')

                # 添加到 directory_map
                directory_map[rel_path] = {
                    'name': file_path.name,
                    'type': 'file' if file_path.suffix == '.md' else 'folder',
                    'path': rel_path
                }

    return directory_map

def generate_report_list():
    """生成报告列表"""
    reports = []

    for item in DIRECTORY.iterdir():
        if not item.is_dir():
            continue

        folder_name = item.name
        if not folder_name.startswith('STOCK_') and not folder_name.startswith('CHINA_'):
            continue

        # 扫描文件夹中的 md 文件
        md_files = []
        for md_file in item.rglob('*.md'):
            rel_path = str(md_file.relative_to(DIRECTORY)).replace('\\', '/')
            md_files.append({
                'name': md_file.name,
                'displayName': get_display_name(md_file.name),
                'path': rel_path,
                'size': md_file.stat().st_size
            })

        if md_files:
            # 确定市场分类
            market = 'other'

            # 港股：包含 _HK_ 或 00 开头的数字代码
            if '_HK_' in folder_name or folder_name.startswith('HK_'):
                market = 'hk'
            # 美股：STOCK_ 后跟纯字母代码（如 BABA, JD, PDD, NTES, TIGR, TME）
            elif folder_name.startswith('STOCK_'):
                # 提取 STOCK_ 后的代码部分
                code_part = folder_name[7:].split('_')[0]  # 去掉 "STOCK_" 后取第一部分
                if code_part.isalpha():  # 纯字母是美股
                    market = 'us'
                else:  # 包含数字是A股或港股
                    # 检查是否是港股格式（00/01/02开头 + _HK_）
                    if '_HK_' in folder_name:
                        market = 'hk'
                    else:
                        market = 'cn'
            # A股：CHINA_ 开头
            elif folder_name.startswith('CHINA_'):
                market = 'cn'

            reports.append({
                'id': folder_name,
                'name': get_report_name(folder_name),
                'folder': folder_name,
                'market': market,
                'files': md_files
            })

    return reports

def get_display_name(filename):
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

def get_report_name(folder_name):
    """获取报告的友好名称"""
    return folder_name

def main():
    print("正在扫描文件...")

    # 生成报告列表
    reports = generate_report_list()
    print(f"找到 {len(reports)} 个报告")

    # 生成目录映射
    directory_map = build_directory_map()
    print(f"找到 {len(directory_map)} 个文件")

    # 保存为 JSON 文件
    output_data = {
        'reports': reports,
        'directoryMap': directory_map
    }

    # 生成 JavaScript 文件（供 HTML 直接加载）
    output_file = DIRECTORY / 'directory_map.js'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('const directoryData = ')
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        f.write(';')

    print(f"已生成: {output_file}")
    print(f"文件大小: {output_file.stat().st_size / 1024:.1f} KB")

if __name__ == '__main__':
    main()
