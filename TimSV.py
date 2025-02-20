import pdfplumber # thư viện làm việc với PDF
import os # thư viện làm việc tự động với hệ thống như liệt kê danh sách trong thư mục , xóa thư mục

# đường dẫn tới thư mục cần làm việc

current_directory = os.getcwd()  # lấy đường dẫn thư mục hiện tại

folder_path = os.path.join(current_directory,"CTXH")

# kiểm tra thư mục tồn tại hay không
if not os.path.exists(folder_path):
    print(f"❌ Thư mục '{folder_path}' không tồn tại.")
    input()
    exit()

# hàm trích xuất thông tin từ một file pdf
def extract_data_from_pdf(pdf_path):
    data = []  # danh sách lưu Dữ liệu
    try: # dùng with .. as để mở và đóng file tự động
        with pdfplumber.open(pdf_path) as pdf:
            # tạo đối tượng trang (page) trong file pdf
            for page in pdf.pages: 
                # tạo danh dách chứa các bảng 2D trong một trang nếu
                tables = page.extract_tables()  # lấy tất cả bảng trên trang
                if not tables:
                    continue  # nếu không có bảng nào thì bỏ qua trang này

                for table in tables: # tạo biến bảng chứa bảng 2D trong danh sách các bảng 2D
                    if not table or len(table) < 2: 
                        continue  # Nếu bảng 2D chỉ có một hàng tức tiêu đề(<2) => không có dữ liệu, bỏ qua

                    header = table[0]  # lấy dòng tiêu đề
                    # tìm vị trí của các cột "MSSV", "Họ và Tên" và "Số ngày CTXH"
                    mssv_index, name_index, days_index = None, None, None

                    for i, col in enumerate(header):
                        if col:
                            col_lower = col.lower()
                            if "mssv" in col_lower or "mã số sv" in col_lower:
                                mssv_index = i # nếu chuỗi mssv có trong cột thì gán vị trí
                            if "họ và tên" in col_lower:
                                name_index = i
                            if "số ngày" in col_lower: # or "số ngày ctxh được tính" in col_lower or "số ngày công tác xã hội" in col_lower:
                                days_index = i

                    # nếu không tìm thấy các cột cần thiết, bỏ qua bảng này
                    if name_index is None and days_index is None and mssv_index is None:
                        continue  

                    # Trích xuất dữ liệu từ các hàng bắt đầu từ hàng số 1 trở đi
                    for row in table[1:]:
                        mssv = "Không rõ"  # giá trị mặc định
                        name = "Không rõ"
                        days = "0"  # Nếu không có số ngày, mặc định là 0

                        if mssv_index is not None and row[mssv_index]: #and len(row) > mssv_index 
                            mssv = row[mssv_index].strip() # loại bỏ các khoảng trắng không cần thiết
                        
                        if name_index is not None and row[name_index]: #and len(row) > name_index 
                            name = row[name_index].strip()
                        
                        if days_index is not None and row[days_index]: # and len(row) > days_index 
                            days = row[days_index].strip()

                        data.append((mssv, name, days))  # lưu dữ liệu

    except Exception as e:
        print(f"❌ Lỗi khi xử lý file {pdf_path}: {e}")
        input("Nhập enter để tiếp tục")

    return data

# lấy danh sách các file PDF
pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
"""
    có thể thay đoạn code ở trên bằng
    pdf_files = []
    for f in os.listdir(folder_path):
        if f.lower().endswith(".pdf"):
            pdf_file.append(f)
"""
if not pdf_files:
    print("❌ Không tìm thấy file PDF nào trong thư mục.")
    input()
    exit()

# nhập thông tin cần tìm
search_query = input("🔍 Nhập MSSV hoặc tên cần tìm (bỏ trống để xem tất cả): ").strip().lower()

# danh sách chứa thông tin cần tìm kieeu dictionary
files_with_query = {}

# duyệt qua từng file và trích xuất dữ liệu
for pdf_file in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file) # lệnh nối đường dẫn
    extracted_data = extract_data_from_pdf(pdf_path)

    if search_query:
        # lọc danh sách chứa mssv or tên
        matching_data = [(mssv, name, days) for mssv, name, days in extracted_data if search_query in mssv.lower() or search_query in name.lower()]
        
        if matching_data:
            files_with_query[pdf_file] = matching_data

    print(f"\n📄 **Danh sách từ file: {pdf_file}**")
    if extracted_data:
        for mssv, name, days in extracted_data:
            if search_query and (search_query in mssv.lower() or search_query in name.lower()):
                print(f"- ✅ MSSV: {mssv}, Họ Tên: {name}, Số ngày CTXH: {days}")  # highlight kết quả tìm kiếm
            else:
                print(f"- MSSV: {mssv}, Họ Tên: {name}, Số ngày CTXH: {days}")
    else:
        print("❌ Không tìm thấy dữ liệu trong file này.")

# hiển thị kết quả tìm kiếm
if search_query:
    print("\n🌚**Kết quả tìm kiếm:**")
    if files_with_query:
        for file, matched_data in files_with_query.items():
            print(f"📌 **{file}**:")
            for mssv, name, days in matched_data:
                print(f"- ✅ MSSV: {mssv}, Họ Tên: {name}, Số ngày CTXH: {days}")
    else:
        print("❌ Không tìm thấy thông tin trong bất kỳ file nào.")
print("\033[91mthấy hay thì cho dũng xin 3k gửi xe🤡\033[0m")
input()
