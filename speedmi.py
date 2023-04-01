import os
import sys
import datetime
import psycopg2
import requests
from tqdm import tqdm
import xml.etree.ElementTree as ET

timestamp = datetime.datetime.now()


def main(sitemap_url):

    response = requests.get(sitemap_url)
    root = ET.fromstring(response.content)

    urls = []
    for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        urls.append(loc.text)

    conn = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT']
    )
    cursor = conn.cursor()

    items = []
    for url in tqdm(urls, desc="Processing URLs", unit="URL", ncols=80):
        item = process_url(url)
        save_to_postgresql(item, cursor, conn)
        items.append(item)

    cursor.close()
    conn.close()


def process_url(url):
    google_api_key = os.environ['GOOGLE_SPEED_API_KEY']
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={google_api_key}&category=accessibility&category=best-practices&category=seo&category=performance&strategy=mobile"

    response = requests.get(api_url)
    data = response.json()
    lighthouse_result = data['lighthouseResult']
    audits = lighthouse_result['audits']

    item = {}
    item['url'] = url
    item['timestamp'] = timestamp

    categories = lighthouse_result['categories']
    item['performance_score'] = categories['performance']['score']
    item['accessibility_score'] = categories['accessibility']['score']
    item['best_practices_score'] = categories['best-practices']['score']
    item['seo_score'] = categories['seo']['score']

    item['first_contentful_paint_score'] = audits['first-contentful-paint']['score']
    item['first_meaningful_paint_score'] = audits['first-meaningful-paint']['score']
    item['largest_contentful_paint_score'] = audits['largest-contentful-paint']['score']
    item['speed_index_score'] = audits['speed-index']['score']
    item['cumulative_layout_shift_score'] = audits['cumulative-layout-shift']['score']

    item['server_response_time_score'] = audits['server-response-time']['score']
    item['is_crawlable_score'] = audits['is-crawlable']['score']
    item['console_errors_score'] = audits['errors-in-console']['score']
    item['total_byte_weight_score'] = audits['total-byte-weight']['score']
    item['dom_size_score'] = audits['dom-size']['score']

    item['raw_json_data'] = data

    return item


def save_to_postgresql(item, cursor, conn):
    columns = ', '.join(item.keys())
    placeholders = ', '.join(['%s'] * len(item))
    query = f"""
        INSERT INTO site_speed_scores ({columns})
        VALUES ({placeholders});
    """
    data = tuple(item.values())
    cursor.execute(query, data)
    conn.commit()


if __name__ == '__main__':
    sitemap_url = sys.argv[1]
    main(sitemap_url)
