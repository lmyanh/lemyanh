from logic_exam import *

# DU LIEU MAU (GIA LAP TU SV1)
questions = [
    {
        "id": 1,
        "subject": "Python",
        "level": "De",
        "question": "Python la ngon ngu gi?",
        "options": {
            "A": "Lap trinh",
            "B": "Mang",
            "C": "Co so du lieu",
            "D": "He dieu hanh"
        },
        "answer": "A"
    },
    {
        "id": 2,
        "subject": "Python",
        "level": "De",
        "question": "Ham in ra man hinh la gi?",
        "options": {
            "A": "echo",
            "B": "print",
            "C": "show",
            "D": "write"
        },
        "answer": "B"
    },
    {
        "id": 3,
        "subject": "Python",
        "level": "Vua",
        "question": "Kieu du lieu luu danh sach la gi?",
        "options": {
            "A": "int",
            "B": "float",
            "C": "list",
            "D": "bool"
        },
        "answer": "C"
    },
    {
        "id": 4,
        "subject": "Python",
        "level": "Vua",
        "question": "Ham lay do dai danh sach la gi?",
        "options": {
            "A": "len()",
            "B": "count()",
            "C": "sum()",
            "D": "size()"
        },
        "answer": "A"
    },
    {
        "id": 5,
        "subject": "Python",
        "level": "Kho",
        "question": "Tu khoa tao lop trong Python la gi?",
        "options": {
            "A": "def",
            "B": "class",
            "C": "new",
            "D": "object"
        },
        "answer": "B"
    }
]

# TEST CAC HAM

print("1. Kiem tra ngan hang cau hoi:")
print(validate_question_bank(questions))

print("\n2. Loc cau hoi Python muc De:")
easy_questions = filter_questions(questions, subject="Python", level="De")
print("So cau:", len(easy_questions))

print("\n3. Tim cau hoi chua tu 'class':")
search_result = search_questions(questions, "class")
print("So cau tim thay:", len(search_result))

print("\n4. Sap xep giam dan theo ID:")
sorted_list = sort_questions(questions, sort_by="id", reverse=True)
for q in sorted_list:
    print("ID:", q["id"], "-", q["question"])

print("\n5. Tao de thi 1 De, 1 Vua, 1 Kho:")
exam = generate_exam(questions, "Python", 1, 1, 1)
print("So cau trong de:", len(exam))

print("\n6. Bat dau thi thu:")
exam, user_answers, detailed_results, final_result = process_exam(questions, "Python", 1, 1, 1)

print("\n===== KET QUA CUOI CUNG =====")
print("Tong so cau:", final_result["total_questions"])
print("So cau dung:", final_result["correct_answers"])
print("So cau sai:", final_result["wrong_answers"])
print("Diem thang 10:", final_result["score_10"])
print("Ty le dung:", final_result["correct_percent"], "%")
print("Ty le sai:", final_result["wrong_percent"], "%")
print("Xep loai:", final_result["classification"])
