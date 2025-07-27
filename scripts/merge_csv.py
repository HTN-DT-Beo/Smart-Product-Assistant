import pandas as pd
import glob
import os

# Đường dẫn tới thư mục chứa các file CSV
folder_path = "data\info"  # Thay bằng đường dẫn thư mục thật
output_path = "data\info\product_catalog_combined.csv"  # File CSV đầu ra

# Lấy danh sách tất cả các file CSV trong thư mục
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

# Đọc và nối tất cả các file lại
df_list = [pd.read_csv(file) for file in csv_files]
combined_df = pd.concat(df_list, ignore_index=True)

# Ghi ra file CSV mới
combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"[✅] Đã gộp {len(csv_files)} file CSV thành: {output_path}")
