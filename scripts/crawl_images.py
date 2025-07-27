# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# import time
# import os
# import requests
# import re

# def sanitize_filename(name):
#     return re.sub(r'[\\/*?:"<>|]', "_", name.strip())

# def download_image(url, path):
#     try:
#         r = requests.get(url, timeout=10)
#         with open(path, 'wb') as f:
#             f.write(r.content)
#         return True
#     except:
#         return False

# def crawl_images_by_tab(url, categories, save_dir='images', max_images=20):
#     options = Options()
#     options.add_argument("--headless")  # không hiển thị trình duyệt
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")

#     driver = webdriver.Chrome(options=options)
#     driver.get(url)
#     time.sleep(3)  # chờ trang load

#     for category in categories:
#         print(f"\n📥 Đang xử lý danh mục: {category}")
#         try:
#             # Tìm tab theo nội dung văn bản
#             tab = driver.find_element(By.XPATH, f"//span[contains(text(), '{category}')]")
#             driver.execute_script("arguments[0].click();", tab)
#             time.sleep(3)  # chờ nội dung tab load lại

#             # Lấy tất cả ảnh trong tab
#             imgs = driver.find_elements(By.CSS_SELECTOR, "img.thumb.lazyloaded")

#             folder = os.path.join(save_dir, category.lower().replace(" ", "_"))
#             os.makedirs(folder, exist_ok=True)

#             count = 0
#             for idx, img in enumerate(imgs):
#                 if count >= max_images:
#                     break
#                 src = img.get_attribute("src") or img.get_attribute("data-src")
#                 alt = img.get_attribute("alt") or f"{category}_{idx}"
#                 filename = sanitize_filename(alt) + ".jpg"
#                 saved_path = os.path.join(folder, filename)
#                 if src and src.startswith("https") and download_image(src, saved_path):
#                     print(f"✅ Đã lưu: {filename}")
#                     count += 1

#         except Exception as e:
#             print(f"❌ Không thể xử lý danh mục '{category}': {e}")

#     driver.quit()

# # Chạy script
# if __name__ == "__main__":
#     crawl_images_by_tab(
#         url="https://www.thegioididong.com/dtdd",  # vẫn dùng URL này vì trang không đổi
#         categories=["""
#                                     Điện Thoại
#                                 """, """
#                                     Apple
#                                 """, """
#                                     Laptop
#                                 """, """
#                                     Phụ Kiện
#                                 """],
#         save_dir="images/khuyenmai",
#         max_images=10
#     )

import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def download_image(url, save_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(res.content)
            print(f"✅ Đã lưu: {save_path}")
        else:
            print(f"❌ Không tải được: {url}")
    except Exception as e:
        print(f"❌ Lỗi khi tải ảnh {url}: {e}")

def crawl_category(driver, url, save_dir, max_products=20):
    os.makedirs(save_dir, exist_ok=True)
    driver.get(url)
    time.sleep(3)
    products = driver.find_elements(By.CSS_SELECTOR, ".listproduct li")[:max_products]
    for idx, item in enumerate(products):
        try:
            name_tag = item.find_element(By.CSS_SELECTOR, "h3")
            name = sanitize_filename(name_tag.text.strip())

            img_tag = item.find_element(By.CSS_SELECTOR, "img")
            img_url = img_tag.get_attribute("data-src") or img_tag.get_attribute("src")
            if img_url and not img_url.startswith("http"):
                img_url = "https:" + img_url
            save_path = os.path.join(save_dir, f"{name}_{idx}.jpg")
            download_image(img_url, save_path)
        except Exception as e:
            print(f"⚠️ Bỏ qua 1 sản phẩm: {e}")

def main():
    base_url = "https://www.thegioididong.com/"
    categories = {
        "dien-thoai": "images/dienthoai",
        "laptop": "images/laptop",
        "apple": "images/apple",
        "phu-kien": "images/phukien"
    }

    options = Options()
    options.add_argument('--headless')  # Ẩn trình duyệt
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200, 800)

    for slug, folder in categories.items():
        url = base_url + slug
        print(f"\n📥 Đang crawl: {slug} → {url}")
        crawl_category(driver, url, folder)

    driver.quit()

if __name__ == "__main__":
    main()
