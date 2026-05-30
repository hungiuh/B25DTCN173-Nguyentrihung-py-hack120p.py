#B25DTCN173 Nguyễn Trí Hùng
import json
import os

DATA_FILE = 'data.json'
students = []

def calculate_gpa(toan, ly, hoa):
    return round((toan + ly + hoa) / 3, 2)

def classify_grade(gpa):
    if gpa < 5.0:
        return "yếu"
    elif gpa < 7.0:
        return "tb"
    elif gpa < 8.0:
        return "khá"
    else:
        return "giỏi"

def input_score(prompt):
    while True:
        try:
            score = float(input(prompt))
            if 0.0 <= score <= 10.0:
                return score
            print("điểm phải nằm trong khoảng từ 0 đến 10")
        except ValueError:
            print("vui lòng nhập một số hợp lệ")

def display_table(student_list):
    if not student_list:
        print("\ndanh sách trống")
        return
    
    print(f"{'Mã SV'} | {'Tên Sinh Viên'} | {'Toán'} | {'Lý'} | {'Hóa'} | {'Điểm TB'} | {'Xếp Loại'}")
    for sv in student_list:
        print(f"{sv['id']} | {sv['ten']} | {sv['diem_toan']} | {sv['diem_ly']} | {sv['diem_hoa']} | {sv['diem_tb']} | {sv['xep_loai']}")

def load_data():
    global students
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                students = json.load(file)
        except Exception as e:
            print(f"không thể đọc file {e}")
            students = []
    else:
        print(f"file {DATA_FILE} ?")
        students = []

def save_data():
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(students, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"không thể lưu file {e}")

def menu_1_display():
    load_data()
    display_table(students)

def menu_2_add():
    print("\n--- thêm mới sinh viên ---")
    sv_id = input("nhập mã sv: ").strip()
    
    if any(sv['id'] == sv_id for sv in students):
        print("mã sv đã tồn tại")
        return

    ten = input("nhập tên sv: ").strip()
    toan = input_score("nhập điểm toán: ")
    ly = input_score("nhập điểm lý: ")
    hoa = input_score("nhập điểm hóa: ")
    
    gpa = calculate_gpa(toan, ly, hoa)
    grade = classify_grade(gpa)
    
    new_sv = {
        "id": sv_id,
        "ten": ten,
        "diem_toan": toan,
        "diem_ly": ly,
        "diem_hoa": hoa,
        "diem_tb": gpa,
        "xep_loai": grade
    }
    
    students.append(new_sv)
    print("đã thêm sinh viên thành công")

def menu_3_update():
    print("\ncập nhật thông tin sinh viên")
    sv_id = input("nhập mã sv cần cập nhật: ").strip()
    
    for sv in students:
        if sv['id'] == sv_id:
            print(f"đang cập nhật cho sinh viên: {sv['ten']}")
            sv['diem_toan'] = input_score("nhập điểm toán mới: ")
            sv['diem_ly'] = input_score("nhập điểm lý mới: ")
            sv['diem_hoa'] = input_score("nhập điểm hóa mới: ")
            
            sv['diem_tb'] = calculate_gpa(sv['diem_toan'], sv['diem_ly'], sv['diem_hoa'])
            sv['xep_loai'] = classify_grade(sv['diem_tb'])
            
            print("cập nhật thành công")
            return
            
    print("không tìm thấy mã sv này")

def menu_4_delete():
    print("\nxoá sinh viên")
    sv_id = input("nhập mã sv cần xoá: ").strip()
    
    for i, sv in enumerate(students):
        if sv['id'] == sv_id:
            confirm = input(f"bạn có chắc muốn xóa sinh viên '{sv['ten']}'? (y/n): ").strip().lower()
            if confirm == 'y':
                del students[i]
                print("đã xoá sinh viên")
            else:
                print("đã hủy thao tác xoá")
            return
            
    print("không tìm thấy mã sv này")

def menu_5_search():
    print("\ntìm kiếm sinh viên")
    keyword = input("nhập mã sv hoặc tên cần tìm: ").strip().lower()
    
    results = [sv for sv in students if keyword in sv['id'].lower() or keyword in sv['ten'].lower()]
    
    if results:
        print(f"\ntìm thấy {len(results)} kết quả:")
        display_table(results)
    else:
        print("không tìm thấy sinh viên nào phù hợp")

def menu_6_sort():
    print("\nsắp xếp danh sách")
    print("1 theo điểm tb giảm dần")
    print("2 theo tên tăng dần (a-z)")
    choice = input("chọn cách sắp xếp (1/2): ").strip()
    
    if choice == '1':
        students.sort(key=lambda x: x['diem_tb'], reverse=True)
        print("đã sắp xếp theo điểm tb giảm dần")
    elif choice == '2':
        students.sort(key=lambda x: x['ten'].split()[-1].lower())
        print("đã sắp xếp theo tên (a-z)")
    else:
        print("lựa chọn không hợp lệ")
    
    display_table(students)

def menu_7_stats():
    print("\nthống kê học lực")
    stats = {"giỏi": 0, "khá": 0, "tb": 0, "yếu": 0}
    
    for sv in students:
        stats[sv['xep_loai']] += 1
        
    for loai, count in stats.items():
        print(f"- loại {loai}: {count} sinh viên")

def menu_8_min_max():
    if not students:
        print("danh sách trống")
        return
        
    max_gpa = max(sv['diem_tb'] for sv in students)
    min_gpa = min(sv['diem_tb'] for sv in students)
    
    print("\nsinh viên có điểm tb cao nhất")
    highest_students = [sv for sv in students if sv['diem_tb'] == max_gpa]
    display_table(highest_students)
    
    print("\nsinh viên có điểm tb thấp nhất")
    lowest_students = [sv for sv in students if sv['diem_tb'] == min_gpa]
    display_table(lowest_students)

def menu_9_classify():
    print("\n--- tiêu chí phân loại học lực ---")
    print("< 5.0        : yếu")
    print("[5.0 - 7.0)  : tb")
    print("[7.0 - 8.0)  : khá")
    print("[8.0 - 10.0] : giỏi")
    
    for sv in students:
        sv['xep_loai'] = classify_grade(sv['diem_tb'])
    print("pass")
    display_table(students)

def main():
    load_data()
    
    while True:
        choice = input("""Quản lí sinh viên
1. Hiển thị danh sách sinh viên
2. Thêm mới sinh viên
3. Cập nhật thông tin sinh viên
4. Xoá sinh viên
5. Tìm kiếm sinh viên
6. Sắp xếp danh sách sinh viên
7 .Thống kê điểm TB
8. Liệt kê sinh viên có điểm TB cao nhất / thấp nhất
9. Phân loại học lực sinh viên		
nhập: """).strip()
        match choice:
            case '1': 
                menu_1_display()
            case '2': 
                menu_2_add()
            case '3': 
                menu_3_update()
            case '4': 
                menu_4_delete()
            case '5': 
                menu_5_search()
            case '6': 
                menu_6_sort()
            case '7': 
                menu_7_stats()
            case '8': 
                menu_8_min_max()
            case '9': 
                menu_9_classify()
            case '10':
                save_data()
                print("dữ liệu đã được lưu pp")
                break
            case _:
                print("lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()