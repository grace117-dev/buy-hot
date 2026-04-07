import requests
import json
from datetime import datetime
from collections import Counter

def get_data():
    # 1. 抓取即時匯率 (JPY to TWD)
    try:
        ex_res = requests.get("https://open.er-api.com/v6/latest/JPY", timeout=10)
        rate = ex_res.json()["rates"]["TWD"]
    except:
        rate = 0.2128  # 備用匯率

    # 2. 專業代購清單 (含模擬台灣搜尋熱度 1-100)
    # 真實開發可介接 Amazon/Google Trends API
    raw_items = [
        {"name": "&be 河北裕介遮瑕膏", "cat": "美妝保養", "jpy": 3850, "tw_hot": 95},
        {"name": "Snow Peak 鈦金屬單層杯", "cat": "戶外露營", "jpy": 3190, "tw_hot": 82},
        {"name": "大正感冒藥 Gold A", "cat": "醫藥保健", "jpy": 1680, "tw_hot": 98},
        {"name": "Uniqlo U 系列抽繩包", "cat": "服飾配件", "jpy": 2990, "tw_hot": 88},
        {"name": "富士山 KAKUDAI 醬油碟", "cat": "生活雜貨", "jpy": 1200, "tw_hot": 75},
        {"name": "IPSA 流金水", "cat": "美妝保養", "jpy": 4400, "tw_hot": 90},
        {"name": "SOTO 蜘蛛爐 ST-310", "cat": "戶外露營", "jpy": 6800, "tw_hot": 85},
        {"name": "EVE止痛藥 Quick DX", "cat": "醫藥保健", "jpy": 1980, "tw_hot": 96}
    ]

    # 3. 分析數據
    # A. 根據台灣熱度排序 (排行榜)
    ranked_items = sorted(raw_items, key=lambda x: x["tw_hot"], reverse=True)

    # B. 統計分類占比 (圓餅圖數據)
    cat_counts = Counter([item["cat"] for item in raw_items])
    total_items = len(raw_items)
    cat_ratio = {k: round((v / total_items) * 100) for k, v in cat_counts.items()}

    # 4. 整合存檔
    final_data = {
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rate": round(rate, 4),
        "ranking": ranked_items[:5], # 取前五名
        "ratio": cat_ratio
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_data()
