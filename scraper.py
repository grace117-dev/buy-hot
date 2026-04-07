import requests
import json
from datetime import datetime

def get_data():
    # 1. 抓取即時匯率 (JPY to TWD)
    try:
        ex_res = requests.get("https://open.er-api.com/v6/latest/JPY")
        rate = ex_res.json()["rates"]["TWD"]
    except:
        rate = 0.212  # 備用匯率

    # 2. 模擬/抓取日本代購熱門趨勢 (這裡可以根據需求擴充 BeautifulSoup 爬蟲)
    # 這裡預設抓取日本 Amazon 與 Mercari 的高需求分類
    trends = [
        {"name": "日本限定 Bioré 防曬噴霧", "category": "藥妝", "jpy": 880, "tag": "熱銷"},
        {"name": "Pokémon Center 季節限定公仔", "category": "動漫", "jpy": 2200, "tag": "高利潤"},
        {"name": "Snow Peak 鈦金屬單層杯", "category": "戶外", "jpy": 3190, "tag": "穩定需求"},
        {"name": "WPC 輕量遮光傘", "category": "生活", "jpy": 2860, "tag": "季節性"},
        {"name": "Uniqlo C 系列聯名款", "category": "服飾", "jpy": 4990, "tag": "新上市"}
    ]

    # 3. 整合存檔
    final_data = {
        "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rate": round(rate, 4),
        "items": trends
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_data()
