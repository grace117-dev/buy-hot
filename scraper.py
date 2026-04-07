import requests
import json
from datetime import datetime, timedelta
import random

def get_data():
    # 1. 抓取即時匯率 (JPY to TWD)
    try:
        # 使用更穩定的 API 備援
        ex_res = requests.get("https://open.er-api.com/v6/latest/JPY", timeout=10)
        rate = ex_res.json()["rates"]["TWD"]
    except:
        rate = 0.2118  # 備用匯率

    # 2. 生成過去 7 天的日期標籤 (日式格式)
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%m/%d") for i in range(6, -1, -1)]

    # 3. 專業代購清單 (含 7 天歷史熱度趨勢 1-100)
    # 真實開發可介接 Amazon Business API 或爬取 Google Trends
    raw_items = [
        {
            "name": "&be 河北裕介遮瑕膏", 
            "cat": "美妝保養", 
            "jpy": 3850, 
            "tw_hot": 95,
            "trend": [80, 82, 85, 88, 90, 93, 95] # 過去 7 天熱度
        },
        {
            "name": "Snow Peak 鈦金屬單層杯", 
            "cat": "戶外露營", 
            "jpy": 3190, 
            "tw_hot": 82,
            "trend": [88, 87, 86, 85, 84, 83, 82] # 熱度略微下滑
        },
        {
            "name": "大正感冒藥 Gold A", 
            "cat": "醫藥保健", 
            "jpy": 1680, 
            "tw_hot": 98,
            "trend": [90, 92, 94, 96, 97, 98, 98] # 持續高溫
        },
        {
            "name": "Uniqlo U 系列抽繩包", 
            "cat": "服飾配件", 
            "jpy": 2990, 
            "tw_hot": 88,
            "trend": [70, 75, 80, 82, 85, 87, 88] # 快速上升
        },
        {
            "name": "富士山 KAKUDAI 醬油碟", 
            "cat": "生活雜貨", 
            "jpy": 1200, 
            "tw_hot": 75,
            "trend": [70, 72, 74, 75, 75, 75, 75] # 趨於穩定
        }
    ]

    # 4. 分析數據
    # A. 根據最新熱度排序 (排行榜)
    ranked_items = sorted(raw_items, key=lambda x: x["tw_hot"], reverse=True)

    # B. 統計分類占比 (用於雷達圖基底)
    categories = list(set([item["cat"] for item in raw_items]))
    cat_data = []
    for cat in categories:
        # 計算該分類下商品的平均熱度作為雷達圖指標
        avg_hot = sum([item["tw_hot"] for item in raw_items if item["cat"] == cat]) / len([item for item in raw_items if item["cat"] == cat])
        cat_data.append({"category": cat, "value": round(avg_hot)})

    # 5. 整合存檔
    final_data = {
        "update_time": datetime.now().strftime("%Y/%m/%d %H:%M"),
        "dates": dates, # 趨勢圖的 X 軸
        "rate": round(rate, 4),
        "ranking": ranked_items[:5], # 取前五名
        "ratio_radar": cat_data # 雷達圖數據
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_data()
