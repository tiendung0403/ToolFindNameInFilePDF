import pdfplumber
import os

# Thư mục chứa các file PDF
folder_path = "E:\\CTXHH"


if not os.path.exists(folder_path):
    print(f"❌ Thư mục '{folder_path}' không tồn tại.")
    exit()

# Hàm trích xuất thông tin từ một file PDF
def extract_data_from_pdf(pdf_path):
    data = []  # Danh sách lưu
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                if not tables:
                    continue

                for table in tables:
                    if not table or len(table) < 2:
                        continue

                    header = table[0] 
                    
                    mssv_index, name_index, days_index = None, None, None

                    for i, col in enumerate(header):
                        if col:
                            col_lower = col.lower()
                            if "mssv" in col_lower or "mã số sinh viên" in col_lower:
                                mssv_index = i
                            if "họ và tên" in col_lower:
                                name_index = i
                            if "số ngày" in col_lower or "số ngày ctxh được tính" in col_lower:
                                days_index = i

                    
                    if name_index is None and days_index is None and mssv_index is None:
                        continue  

                    
                    for row in table[1:]:
                        mssv = "Không rõ"  
                        name = "Không rõ"
                        days = "0" 

                        if mssv_index is not None and len(row) > mssv_index and row[mssv_index]:
                            mssv = row[mssv_index].strip()
                        
                        if name_index is not None and len(row) > name_index and row[name_index]:
                            name = row[name_index].strip()
                        
                        if days_index is not None and len(row) > days_index and row[days_index]:
                            days = row[days_index].strip()

                        data.append((mssv, name, days))  # Lưu dữ liệu

    except Exception as e:
        print(f"❌ Lỗi khi xử lý file {pdf_path}: {e}")

    return data


pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]

if not pdf_files:
    print("❌ Không tìm thấy file PDF nào trong thư mục.")
    exit()


search_query = input("🔍 Nhập MSSV hoặc tên cần tìm (bỏ trống để xem tất cả): ").strip().lower()


files_with_query = {}


for pdf_file in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file)
    extracted_data = extract_data_from_pdf(pdf_path)

    if search_query:

        matching_data = [(mssv, name, days) for mssv, name, days in extracted_data if search_query in mssv.lower() or search_query in name.lower()]
        
        if matching_data:
            files_with_query[pdf_file] = matching_data

    print(f"\n📄 **Danh sách từ file: {pdf_file}**")
    if extracted_data:
        for mssv, name, days in extracted_data:
            if search_query and (search_query in mssv.lower() or search_query in name.lower()):
                print(f"- ✅ MSSV: {mssv}, Họ Tên: {name}, Số ngày CTXH: {days}")
            else:
                print(f"- MSSV: {mssv}, Họ Tên: {name}, Số ngày CTXH: {days}")
    else:
        print("❌ Không tìm thấy dữ liệu trong file này.")

# Hiển thị kết quả tìm kiếm
if search_query:
    print("\n🎯 **Kết quả tìm kiếm:**")
    if files_with_query:
        for file, matched_data in files_with_query.items():
            print(f"📌 **{file}**:")
            for mssv, name, days in matched_data:
                print(f"- ✅ MSSV: {mssv}, Họ Tên: {name}, Số ngày CTXH: {days}")
    else:
        print("❌ Không tìm thấy thông tin trong bất kỳ file nào.")
