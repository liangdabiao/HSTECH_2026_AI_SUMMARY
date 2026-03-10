#!/usr/bin/env python3
"""
生成报告索引JSON文件
扫描所有股票报告文件夹，收集文件夹结构和文件内容
"""

import os
import json
from pathlib import Path

# 配置
BASE_DIR = Path(r"E:\恒生科技")
OUTPUT_FILE = BASE_DIR / "reports_data.json"
EXCLUDE_DIRS = {'.git', '__pycache__', 'node_modules', '.claude'}
EXCLUDE_FILES = {'build_json.py', 'reports_data.json', 'index2.html', 'reader.html', 'readme.md'}

# 报告数据映射（文件夹名 -> 中文名称）
REPORT_NAMES = {
    # 港股
    "STOCK_00700_HK_Tencent": "腾讯控股 (00700.HK)",
    "STOCK_09988_HK_Alibaba": "阿里巴巴 (09988.HK)",
    "STOCK_00772_HK_China_Literature": "阅文集团 (00772.HK)",
    "STOCK_00688_HK_China_Overseas": "中国海外 (00688.HK)",
    "STOCK_01810_HK_Xiaomi_Final": "小米集团 (01810.HK)",
    "STOCK_01024_HK_Kuaishou": "快手 (01024.HK)",
    "STOCK_03690_HK_Meituan": "美团 (03690.HK)",
    "STOCK_09618_HK_JD_com": "京东集团 (09618.HK)",
    "STOCK_02015_HK_Li_Auto": "理想汽车 (02015.HK)",
    "STOCK_09868_HK_XPeng_Fresh": "小鹏汽车 (09868.HK)",
    "STOCK_01211_HK_BYD": "比亚迪股份 (01211.HK)",
    "STOCK_00981_HK_SMIC": "中芯国际 (00981.HK)",
    "STOCK_00992_HK_Lenovo": "联想集团 (00992.HK)",
    "STOCK_03888_HK_Kingsoft": "金山软件 (03888.HK)",
    "STOCK_02269_HK_WuXi_Biologics": "药明生物 (02269.HK)",
    "STOCK_01801_HK_Innovent": "信达生物 (01801.HK)",
    "STOCK_00388_HK_HKEX": "港交所 (00388.HK)",
    "STOCK_09626_HK_Bilibili": "哔哩哔哩 (09626.HK)",
    "STOCK_00020_HK_SenseTime": "商汤科技 (00020.HK)",
    "STOCK_00285_HK_BYD_Electronic": "比亚迪电子 (00285.HK)",
    "STOCK_02158_HK_Yidu_Tech": "医脉通 (02158.HK)",
    "STOCK_06618_HK_JDHealth": "京东健康 (06618.HK)",
    "STOCK_02400_HK_XD_Inc": "心动公司 (02400.HK)",
    "STOCK_03693_HK_GDS": "万国数据 (03693.HK)",
    "STOCK_06060_HK_ZhongAn": "众安在线 (06060.HK)",
    "STOCK_00867_HK_CanSino_Biologics": "康希诺生物 (00867.HK)",
    "STOCK_00383_HK_TianAn_Medicare": "中国天保 (00383.HK)",
    "STOCK_00853_HK_MicroPort": "微创医疗 (00853.HK)",
    "STOCK_01138_HK_COSCO_Shipping_Energy": "中远海运能源 (01138.HK)",
    "STOCK_09988_HK_AliHealth": "阿里健康 (09988.HK)",
    "STOCK_09698_HK_GDS": "万国数据-SW (09698.HK)",
    "STOCK_9995_HK_RemeGen": "荣昌生物 (9995.HK)",

    # 美股
    "STOCK_BABA_Alibaba": "阿里巴巴 (BABA)",
    "STOCK_JD_JDcom": "京东 (JD)",
    "STOCK_PDD_Pinduoduo": "拼多多 (PDD)",
    "STOCK_BIDU_Baidu": "百度 (BIDU)",
    "STOCK_NTES_NetEase": "网易 (NTES)",
    "STOCK_TME_Tencent_Music": "腾讯音乐 (TME)",
    "STOCK_BILI_Bilibili": "哔哩哔哩 (BILI)",
    "STOCK_NIO_NIO": "蔚来 (NIO)",
    "STOCK_LI_LiAuto": "理想汽车 (LI)",
    "STOCK_XPEV_Xpeng": "小鹏汽车 (XPEV)",
    "STOCK_WB_Weibo": "微博 (WB)",
    "STOCK_VIPS_Vipshop": "唯品会 (VIPS)",
    "STOCK_TIGR_Tiger_Brokers": "老虎证券 (TIGR)",
    "STOCK_IQ_iQIYI": "爱奇艺 (IQ)",
    "STOCK_KC_Kingsoft_Cloud": "金山云 (KC)",
    "STOCK_ATHM_Autohome": "汽车之家 (ATHM)",
    "STOCK_MNSO_Miniso": "名创优品 (MNSO)",
    "STOCK_YUMC_Yum_China": "百胜中国 (YUMC)",
    "STOCK_EDU_NewOriental": "新东方 (EDU)",
    "STOCK_TAL_TAL_Education": "好未来 (TAL)",
    "STOCK_BEKE_Keji": "贝壳 (BEKE)",
    "STOCK_ZTO_ZTO_Express": "中通快递 (ZTO)",
    "STOCK_VNET_21Vianet": "世纪互联 (VNET)",
    "STOCK_GDS_Wanshui_Data": "万国数据 (GDS)",
    "STOCK_API_Agora": "声网 (API)",
    "STOCK_BZ_BOSS_Zhipin": "BOSS直聘 (BZ)",
    "STOCK_JOYY_Joyy": "JOYY (YY)",
    "STOCK_HUYA_Huya": "虎牙 (HUYA)",
    "STOCK_DOYU_Douyu": "斗鱼 (DOYU)",
    "STOCK_MOMO_Tantan": "陌陌 (MOMO)",
    "STOCK_FINV_LexinFintech": "信也科技 (FINV)",
    "STOCK_QFIN_Qifu_Tech": "360数科 (QFIN)",
    "STOCK_LU_Lufax": "陆金所 (LU)",
    "STOCK_HTHT_Hua_Zhu": "华住 (HTHT)",
    "STOCK_NOAH_Nuoia_Holding": "诺亚财富 (NOAH)",
    "STOCK_YRD_Yiren": "宜人贷 (YRD)",
    "STOCK_NIU_Niu": "小牛电动 (NIU)",
    "STOCK_EH_EHang": "亿航智能 (EH)",
    "STOCK_HESAI_Hesai": "禾赛科技 (HESAI)",
    "STOCK_ZK_Zeekr": "极氪 (ZK)",
    "STOCK_JKS_JinkoSolar": "晶科能源 (JKS)",
    "STOCK_CSIQ_CanadianSolar": "阿特斯太阳能 (CSIQ)",
    "STOCK_DQ_Daqo_New_Energy": "大全新能源 (DQ)",
    "STOCK_AMBO_Ambow": "安博教育 (AMBO)",
    "STOCK_BEDU_BrightScholar": "博实乐 (BEDU)",
    "STOCK_COE_51Talk": "51Talk (COE)",
    "STOCK_TEDU_Tarena": "达内教育 (TEDU)",
    "STOCK_NEW_Puxin": "朴新教育 (NEW)",
    "STOCK_ONE_OneSmart": "掌门1对1 (ONE)",
    "STOCK_STG_Sunlands": "尚德机构 (STG)",
    "STOCK_REDU_Rise": "流利说 (REDU)",
    "STOCK_SJ_Shanbay": "扇贝 (SJ)",
    "STOCK_DAO_Youdao": "有道 (DAO)",
    "STOCK_TUYA_Tuya": "涂鸦智能 (TUYA)",
    "STOCK_RLX_Relonx": "RELX雾芯科技 (RLX)",
    "STOCK_CANG_CanGo": "优信 (CANG)",
    "STOCK_BZUN_Baozun": "宝尊电商 (BZUN)",
    "STOCK_POZH_Parkha": "朴田 (POZH)",
    "STOCK_QD_Qudian": "趣店 (QD)",
    "STOCK_RERE_Ataike": "ATA (RERE)",
    "STOCK_DDL_Dingdong": "叮咚买菜 (DDL)",
    "STOCK_YMM_Full_Truck_Alliance": "满帮 (YMM)",
    "STOCK_ECAR_Ecarx": "亿咖通 (ECAR)",
    "STOCK_GHG_GreenTree": "绿城管理 (GHG)",
    "STOCK_HLG_Hailiang": "海亮教育 (HLG)",
    "STOCK_XNET_Xunlei": "迅雷 (XNET)",
    "STOCK_DL_ChinaDistance": "中国 Distance (DL)",
    "STOCK_CIC_BlueCity": "蓝城 (CIC)",
    "STOCK_GOTU_Gaosu": "高途 (GOTU)",
    "STOCK_ZH_Zhihu": "知乎 (ZH)",
    "STOCK_LX_Lexin": "陆金所 (LX)",
    "STOCK_JFIN_Jiayin": "嘉银金科 (JFIN)",
    "STOCK_ZLAB_Zai_Lab": "再鼎医药 (ZLAB)",
    "STOCK_ATAT_Atour": "亚朵 (ATAT)",
    "STOCK_YSG_Yixian_Ecommerce": "小鹏 (YSG)",

    # A股 - 创业板/主板
    "STOCK_300750_CATL": "宁德时代 (300750)",
    "STOCK_300760_Mindray": "迈瑞医疗 (300760)",
    "STOCK_300124_Inovance": "汇川技术 (300124)",
    "STOCK_300274_Sungrow": "阳光电源 (300274)",
    "STOCK_300015_Aier": "爱尔眼科 (300015)",
    "STOCK_300122_Zhifei": "智飞生物 (300122)",
    "STOCK_300033_TONGHUA_RESEARCH": "同花顺 (300033)",
    "STOCK_300059_Eastmoney": "东方财富 (300059)",
    "STOCK_300014_EVE": "亿纬锂能 (300014)",
    "STOCK_300207_Sunwoda": "欣旺达 (300207)",
    "STOCK_300308_InnoLight": "中际旭创 (300308)",
    "STOCK_300316_Jingsheng": "晶盛机电 (300316)",
    "STOCK_300408_Torch": "三环集团 (300408)",
    "STOCK_300413_Mango": "芒果超媒 (300413)",
    "STOCK_300433_Lens": "蓝思科技 (300433)",
    "STOCK_300450_Lead": "先导智能 (300450)",
    "STOCK_300454_SANGFOR": "深信服 (300454)",
    "STOCK_300458_Allwinner": "全志科技 (300458)",
    "STOCK_300476_Victory": "胜宏科技 (300476)",
    "STOCK_300482_Wondfo": "万孚生物 (300482)",
    "STOCK_300496_THUNDERSOFT": "中科创达 (300496)",
    "STOCK_300502_Xinyisheng": "新易盛 (300502)",
    "STOCK_300529_Jafron": "健帆生物 (300529)",
    "STOCK_300595_Oulth": "欧普康视 (300595)",
    "STOCK_300601_BIOTECH": "康泰生物 (300601)",
    "STOCK_300604_Changchuan": "长川科技 (300604)",
    "STOCK_300661_SGMC": "圣邦股份 (300661)",
    "STOCK_300724_Jiejiawei": "捷佳伟创 (300724)",
    "STOCK_300735_Guanghong": "光弘科技 (300735)",
    "STOCK_300751_MINDRAY": "迈瑞医疗-SZ (300751)",
    "STOCK_300759_Pharmaron": "康龙化成 (300759)",
    "STOCK_300763_Ginlong": "锦浪科技 (300763)",
    "STOCK_300766_COMPANY": "每日互动 (300766)",
    "STOCK_300769_Defang": "德方纳米 (300769)",
    "STOCK_300777_FULLHAN": "中科海讯 (300777)",
    "STOCK_300782_Maxscend": "卓胜微 (300782)",
    "STOCK_300803_Compass": "指南针 (300803)",
    "STOCK_300821_SANUO": "三孚新科 (300821)",
    "STOCK_300866_Anker": "安克创新 (300866)",
    "STOCK_300888_CHINASOFT": "中科软 (300888)",
    "STOCK_300896_HITHINK": "爱美客 (300896)",
    "STOCK_300905_BAOCHENG": "宝丽迪 (300905)",
    "STOCK_300919_ZHONGKE": "中科电气 (300919)",
    "STOCK_300925_FABEN": "法本信息 (300925)",
    "STOCK_300932_BOCHUANG": "博创科技 (300932)",
    "STOCK_300938_JINYI": "金逸影视 (300938)",
    "STOCK_300945_GONGDA": "弘讯科技 (300945)",
    "STOCK_300947_HENGDA": "恒立液压 (300947)",
    "STOCK_300955_Wanhang": "宝通科技 (300955)",
    "STOCK_300957_BETAINY": "贝泰妮 (300957)",
    "STOCK_300963_DIOU": "中船应急 (300963)",
    "STOCK_300968_Hygon": "海光信息 (300968)",
    "STOCK_300985_ZHIYUAN": "致远互联 (300985)",
    "STOCK_300999_HUALI": "金龙鱼 (300999)",
    "STOCK_301003_ZHONGKE": "中科通达 (301003)",
    "STOCK_301011_SANMIN": "三美股份 (301011)",
    "STOCK_301028_HONGDU": "东亚机械 (301028)",
    "STOCK_301036_YULONG": "本川智能 (301036)",
    "STOCK_301111_KANGTAN": "康泰医学 (301111)",
    "STOCK_301168_JINGWEI": "通业科技 (301168)",
    "STOCK_301188_HANFEI": "力合科技 (301188)",
    "STOCK_301222_GREE": "格力博 (301222)",
    "STOCK_301236_isoftstone": "软通动力 (301236)",
    "STOCK_301301_Sichuan": "川宁生物 (301301)",
    "STOCK_301333_MINGYU": "明冠新材 (301333)",
    "STOCK_301558_YULONG": "三角轮胎 (301558)",
    "STOCK_302132_AVIC": "中航 (302132)",
    "STOCK_300001_TGOOD": "特锐德 (300001)",
    "STOCK_300002_SZHANYOU": "神州数码 (300002)",
    "STOCK_300003_Lepu": "乐普医疗 (300003)",
    "STOCK_300017_Wangsu": "网宿科技 (300017)",
    "STOCK_300024_SIASUN": "机器人 (300024)",
    "STOCK_300058_BlueFocus": "蓝色光标 (300058)",
    "STOCK_300073_Ronbay": "当升科技 (300073)",
    "STOCK_300075_CASOD": "数字政通 (300075)",
    "STOCK_300115_CHANGYING": "长盈精密 (300115)",
    "STOCK_300136_Sunway": "信维通信 (300136)",
    "STOCK_300142_WALVAX": "沃森生物 (300142)",
    "STOCK_300223_Ingenic": "北京君正 (300223)",
    "STOCK_300251_Enlight": "光线传媒 (300251)",
    "STOCK_300339_Runheng": "润和软件 (300339)",
    "STOCK_300346_Higah": "联创电子 (300346)",
    "STOCK_300347_Tigermed": "泰格医药 (300347)",
    "STOCK_300357_YaWo": "我武生物 (300357)",
    "STOCK_300373_JunSheng": "扬杰科技 (300373)",
    "STOCK_300383_Sinonet": "新城控股 (300383)",
    "STOCK_300394_Tfc": "天孚通信 (300394)",
    "STOCK_300418_Kunlun": "昆仑万维 (300418)",
    "STOCK_300442_Runze": "润泽科技 (300442)",
    "STOCK_300474_Jing": "景嘉微 (300474)",
    "STOCK_300502_Innolight": "旌屹科技 (300502)",
    "STOCK_300724_Jinjia": "金嘉 (300724)",
    "STOCK_300735_Light": "光韵达 (300735)",
    "STOCK_300750_SZ_CATL": "宁德时代-SZ (300750)",
    "STOCK_300896_Eime": "爱美客 (300896)",
    "STOCK_300955_Beta": "贝塔 (300955)",
    "STOCK_603613_Guolian": "国联股份 (603613)",
    "STOCK_002602_Shijiagiantong": "世纪华通 (002602)",

    # 科创板
    "STOCK_688008_SH_Lanjing": "澜起科技 (688008)",
    "STOCK_688009_SH_China_Railway_Signal": "中国通号 (688009)",
    "STOCK_688012_SH_AMEC": "中微公司 (688012)",
    "STOCK_688036_SH_Transsion": "传音控股 (688036)",
    "STOCK_688036_Transsion": "传音控股 (688036)",
    "STOCK_688041_SH_Hygon": "海光信息 (688041)",
    "STOCK_688047_SH_Loongson": "龙芯中科 (688047)",
    "STOCK_688065_SH_Caty": "凯赛生物 (688065)",
    "STOCK_688072_SH_Piotech": "拓荆科技 (688072)",
    "STOCK_688082_SH_ACMI": "奥普特 (688082)",
    "STOCK_688099_SH_Amlogic": "晶晨股份 (688099)",
    "STOCK_688111_SH_Kingsoft": "金山办公 (688111)",
    "STOCK_688114_SH_MGI": "华大智造 (688114)",
    "STOCK_688120_SH_Hwatsing": "华海清科 (688120)",
    "STOCK_688122_SH_Western_Superconducting": "西部超导 (688122)",
    "STOCK_688126_SH_Simgui": "聚杰微纤 (688126)",
    "STOCK_688169_SH_Roborock": "石头科技 (688169)",
    "STOCK_688169_Roborock": "石头科技 (688169)",
    "STOCK_688180_SH_Junshi_Bio": "君实生物 (688180)",
    "STOCK_688183_SH_Shyenn": "生益电子 (688183)",
    "STOCK_688187_SH_TimesElectric": "时代电气 (688187)",
    "STOCK_688188_SH_Baichu": "柏楚电子 (688188)",
    "STOCK_688213_SH_SmartSens": "思特威 (688213)",
    "STOCK_688220_SH_ALDA": "阿拉丁 (688220)",
    "STOCK_688223_SH_JinkoSolar": "晶科能源 (688223)",
    "STOCK_688234_SH_Tianyue": "天岳先进 (688234)",
    "STOCK_688249_SH_Huaian": "晶合集成 (688249)",
    "STOCK_688256_SH_Cambricon": "寒武纪 (688256)",
    "STOCK_688271_SH_United_Imaging": "联影医疗 (688271)",
    "STOCK_688278_SH_AmoyTop": "特宝生物 (688278)",
    "STOCK_688297_SH_Ewatt": "中电港 (688297)",
    "STOCK_688297_Ewatt": "中电港 (688297)",
    "STOCK_688303_SH_Daqan": "大全能源 (688303)",
    "STOCK_688303_Daqan": "大全能源 (688303)",
    "STOCK_688349_SH_Sany_Repower": "三一重能 (688349)",
    "STOCK_688349_Sany_Repower": "三一重能 (688349)",
    "STOCK_688375_SH_GuoBo": "国博电子 (688375)",
    "STOCK_688375_GuoBo": "国博电子 (688375)",
    "STOCK_688396_SH_CRMicro": "华润微 (688396)",
    "STOCK_688396_CRMicro": "华润微 (688396)",
    "STOCK_688469_SH_XinLian": "芯联集成 (688469)",
    "STOCK_688469_XinLian": "芯联集成 (688469)",
    "STOCK_688472_SH_Canadian": "阿特斯 (688472)",
    "STOCK_688472_Canadian": "阿特斯 (688472)",
    "STOCK_688475_SH_Ezviz": "萤石网络 (688475)",
    "STOCK_688475_Ezviz": "萤石网络 (688475)",
    "STOCK_688506_SH_Baili": "百利天恒 (688506)",
    "STOCK_688506_Baili": "百利天恒 (688506)",
    "STOCK_688521_SH_Verisilicon": "芯原股份 (688521)",
    "STOCK_688521_Verisilicon": "芯原股份 (688521)",
    "STOCK_688525_SH_Biwin_Storage": "佰维存储 (688525)",
    "STOCK_688538_SH_Everdisplay_OLED": "和辉光电 (688538)",
    "STOCK_688578_SH_Alis_Biopharma": "艾力斯 (688578)",
    "STOCK_688599_SH_Trisolar_PV": "天合光能 (688599)",
    "STOCK_688608_SH_Hengxuan_Tech": "恒玄科技 (688608)",
    "STOCK_688617_SH_Wit_Medical": "惠泰医疗 (688617)",
    "STOCK_688702_SH_Centec_Comm": "盛景微 (688702)",
    "STOCK_688728_SH_GalaxyCore": "格科微 (688728)",
    "STOCK_688777_SH_Supcon_Tech": "中控技术 (688777)",
    "STOCK_688819_SH_Tianan_Battery": "天能股份 (688819)",
    "STOCK_688981_SH_SMIC": "中芯国际-U (688981)",
    "STOCK_689009_SH_Ninebot": "九号公司 (689009)",
    "STOCK_689009_Ninebot": "九号公司 (689009)",

    # 行业分析
    "CHINA_CLOUD_COMPUTING_INDUSTRY_ANALYSIS": "中国云计算行业分析",
    "CHINA_ECOMMERCE_INDUSTRY_ANALYSIS_2025": "中国电商行业分析2025",
    "CHINA_EDUCATION_INDUSTRY_ANALYSIS_2025": "中国教育行业分析2025",
    "CHINA_LOGISTICS_INDUSTRY_ANALYSIS_2025": "中国物流行业分析2025",
    "EDUTECH_TRENDS_2025": "教育科技趋势2025",
    "LIVE_STREAMING_E-COMMERCE_ANALYSIS": "直播电商分析",
    "MOBILE_GAME_INDUSTRY_ANALYSIS_2024": "手游行业分析2024",
}

def get_market_type(folder_name):
    """根据文件夹名判断市场类型"""
    if folder_name.startswith("CHINA_") or folder_name in ["EDUTECH_TRENDS_2025", "LIVE_STREAMING_E-COMMERCE_ANALYSIS", "MOBILE_GAME_INDUSTRY_ANALYSIS_2024"]:
        return "industry"
    if "_HK_" in folder_name or folder_name.endswith("_HK"):
        return "hk"
    if folder_name.startswith("STOCK_688") or folder_name.startswith("STOCK_689"):
        return "cn"
    if folder_name.startswith("STOCK_300") or folder_name.startswith("STOCK_301") or folder_name.startswith("STOCK_002") or folder_name.startswith("STOCK_603"):
        return "cn"
    if folder_name.startswith("STOCK_") and "_" in folder_name:
        parts = folder_name.split("_")
        if len(parts) >= 3:
            stock_code = parts[1]
            if stock_code.isalpha():
                return "us"
    return "other"

def read_file_content(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"# 读取失败\n\n错误: {str(e)}"

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
        'bear_case.md': '悲观情形',
        'monitoring_checklist.md': '监控清单',
        'bibliography.md': '参考文献',
        'overview.md': '概览',
    }
    return display_names.get(filename, filename.replace('.md', ''))

def build_folder_structure(folder_path, folder_name):
    """构建文件夹结构"""
    files_data = []

    try:
        for item in folder_path.iterdir():
            if item.is_file() and item.suffix == '.md':
                relative_path = item.relative_to(BASE_DIR)
                file_key = str(relative_path).replace('\\', '/')

                files_data.append({
                    'name': item.name,
                    'displayName': get_display_name(item.name),
                    'path': file_key,
                    'size': item.stat().st_size
                })
            elif item.is_dir() and item.name not in EXCLUDE_DIRS:
                # 处理子文件夹
                sub_folder_data = build_folder_structure(item, folder_name + "/" + item.name)
                files_data.extend(sub_folder_data)
    except Exception as e:
        print(f"警告: 无法读取文件夹 {folder_path}: {e}")

    return files_data

def scan_all_folders():
    """扫描所有报告文件夹"""
    reports = []

    for item in BASE_DIR.iterdir():
        if not item.is_dir():
            continue

        folder_name = item.name

        # 跳过排除的文件夹
        if folder_name in EXCLUDE_DIRS:
            continue

        # 跳过排除的文件
        if folder_name in EXCLUDE_FILES:
            continue

        # 只处理 STOCK_ 开头或特定的行业分析文件夹
        if not (folder_name.startswith('STOCK_') or
                folder_name.startswith('CHINA_') or
                folder_name in ['EDUTECH_TRENDS_2025', 'LIVE_STREAMING_E-COMMERCE_ANALYSIS', 'MOBILE_GAME_INDUSTRY_ANALYSIS_2024']):
            continue

        # 获取报告名称
        report_name = REPORT_NAMES.get(folder_name, folder_name)
        market_type = get_market_type(folder_name)

        # 构建文件结构
        files = build_folder_structure(item, folder_name)

        if files:
            reports.append({
                'id': folder_name,
                'name': report_name,
                'folder': folder_name,
                'market': market_type,
                'files': files
            })

    return reports

def build_content_index(reports):
    """构建内容索引 - 包含所有文件内容"""
    content_index = {
        'version': '1.0',
        'generatedAt': '',
        'reports': reports,
        'files': {}
    }

    total_files = 0
    for report in reports:
        for file_info in report['files']:
            file_path = BASE_DIR / file_info['path']
            if file_path.exists():
                content = read_file_content(file_path)
                content_index['files'][file_info['path']] = content
                total_files += 1
                print(f"已读取: {file_info['path']}")

    print(f"\n总共读取 {total_files} 个文件")
    return content_index

def main():
    print("开始扫描报告文件夹...")
    print(f"基础目录: {BASE_DIR}")
    print(f"输出文件: {OUTPUT_FILE}\n")

    # 扫描所有文件夹
    reports = scan_all_folders()
    print(f"\n找到 {len(reports)} 个报告文件夹")

    # 构建内容索引
    content_index = build_content_index(reports)

    # 添加时间戳
    from datetime import datetime
    content_index['generatedAt'] = datetime.now().isoformat()

    # 保存JSON文件
    print(f"\n正在保存到 {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(content_index, f, ensure_ascii=False, indent=2)

    # 计算文件大小
    file_size = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"完成! JSON文件大小: {file_size:.2f} MB")

if __name__ == '__main__':
    main()
