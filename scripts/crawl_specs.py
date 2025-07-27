import requests
from bs4 import BeautifulSoup
import csv
import os

def crawl_product_details(url, save_file='data/product_details.csv', max_products=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    os.makedirs(os.path.dirname(save_file), exist_ok=True)

    with open(save_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Tên sản phẩm', 'RAM', 'SSD', 'Giá hiện tại', 'Giá cũ',
            'Giảm giá', 'Quà tặng', 'Đã bán', 'Rating', 'Link ảnh'
        ])

        products = soup.select('.listproduct li')
        count = 0

        for p in products:
            if max_products and count >= max_products:
                break
            try:
                name = p.find('h3').text.strip()

                specs = p.select('.item-compare span')
                ram = specs[0].text.strip() if len(specs) > 0 else "NaN"
                ssd = specs[1].text.strip() if len(specs) > 1 else "NaN"

                price_now = p.select_one('.price')
                price_old = p.select_one('.price-old')
                discount = p.select_one('.percent')
                gift = p.select_one('.item-gift b')
                sold = p.select_one('.vote-txt span')
                rating = p.select_one('.ratingnumber')

                price_now = price_now.text.strip() if price_now else "NaN"
                price_old = price_old.text.strip() if price_old else "NaN"
                discount = discount.text.strip() if discount else "NaN"
                gift_value = gift.text.strip() if gift else "NaN"
                sold_text = sold.text.strip() if sold else "NaN"
                rating_text = rating.text.strip() if rating else "NaN"

                # Lấy ảnh sản phẩm
                img_tag = p.find('img')
                img_link = img_tag.get('data-src') or img_tag.get('src') or "NaN"

                writer.writerow([
                    name, ram, ssd, price_now, price_old, discount,
                    gift_value, sold_text, rating_text, img_link
                ])
                print(f"✅ Đã crawl: {name}")
                count += 1
            except Exception as e:
                print(f"❌ Lỗi với 1 sản phẩm: {e}")
                continue


def main():
    base_url = "https://www.thegioididong.com/"
    categories = {
        "dien-thoai": "data/products_dienthoai.csv",
        "laptop": "data/products_laptop.csv",
        "apple": "data/products_apple.csv",
        "tai-nghe": "data/products_tainghe.csv",
        "sac-dtdd": "data/products_sac.csv"
    }

    for slug, filepath in categories.items():
        url = base_url + slug
        print(f"\n🔍 Đang crawl dữ liệu sản phẩm từ: {url}")
        crawl_product_details(url, save_file=filepath, max_products=30)

if __name__ == "__main__":
    main()
