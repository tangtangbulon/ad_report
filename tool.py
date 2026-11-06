import requests
import sqlite3
import os
from pathlib import Path
import logging
import csv


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)


filepath = 'ad_report.csv'


def read_filter_csv(filepath,threshold=30):
    data = []
    try:
        with open(filepath,'r',encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                acos = float(row['acos'].rstrip('%'))  # 14.46 表示 14.46%
                if acos >= threshold:
                    row['cost_cny'] = round(float(row['cost']) * rate,2) # 转换为人民币
                    row['sales_cny'] = round(float(row['sales']) * rate,2) # 转换为人民币
                    data.append(row)
            print(f'Found {len(data)} rows with ACOS >= {threshold}')
        return data
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return []


def get_exchange_rate(currency='USD',):
    url="https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status() # 检查 HTTP 状态码
        data = response.json()

        return data['rates']['CNY']
    except requests.exceptions.Timeout as e:
        print("⚠️ 网络超时，使用备用默认汇率 7.2")
        return 7.2
    except requests.exceptions.ConnectionError as e:
        print("⚠️ 网络连接错误，使用备用默认汇率 7.2")
        return 7.2

rate = get_exchange_rate()


def save_to_new_file(data,rate):
    if data:
        fieldnames = list(data[0].keys())
        with open('ad_report_cny.csv','w',encoding='utf-8',newline='') as file:
            writer = csv.DictWriter(file,fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"✅ 处理完成！符合条件的数据已保存到 ad_report_cny.csv")
    else:
        print("❌ 没有符合条件的数据")

shop_db_path = (
    Path(__file__).resolve().parents[1]
    / "frist_1_ecom_analytics"
    / "ecom-analytics"
    / "my_web_project"
    / "database"
    / "shop.db"
)

def get_cost(sku):
    logger.info(f"查询成本: {sku}")
    try:
        if sku == "ERROR":
            raise RuntimeError("成本服务超时")

        with sqlite3.connect(shop_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT cost FROM products WHERE sku=?", (sku,))
            row = cursor.fetchone()
            if row is not None:
                result = {"cost": row[0]}
            else:
                result = {"cost": {"error": "成本不存在"}}
    except RuntimeError as e:
        result = {"cost": {"error": str(e)}}
    logger.info(f"查询成本结果: {result}")
    return result


def get_commission_rate(store_id):
    logger.info(f"查询佣金率: {store_id}")
    try:
        if store_id == "ERROR":
            raise RuntimeError("佣金率服务超时")

        with sqlite3.connect(shop_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT commission_rate FROM stores WHERE store_id=?", (store_id,))
            row = cursor.fetchone()
            if row is not None:
                result={"commission_rate": row[0]}
            else:
                result={"commission_rate": {"error": "佣金率不存在"}}
    except RuntimeError as e:
        result={"commission_rate": {"error": str(e)}}
    logger.info(f"查询佣金率结果: {result}")
    return result
