import random
def validate_answer(answer):
    return answer.upper() in ["A", "B", "C", "D"]

def validate_exam_request(num_easy, num_medium, num_hard):
    if num_easy < 0 or num_medium < 0 or num_hard < 0:
        return False
    if (num_easy + num_medium + num_hard) == 0:
        return False

    return True

def validate_question_bank(questions):
    required_keys = ["id", "subject", "level", "question", "options", "answer"]
    
    for q in questions:
        for key in required_keys:
            if key not in q:
                return False

        if "A" not in q["options"] or "B" not in q["options"] or "C" not in q["options"] or "D" not in q["options"]:
            return False

        if q["answer"] not in ["A", "B", "C", "D"]:
            return False

    return True

def filter_questions(questions, subject=None, level=None):
    result = questions

    if subject is not None:
        result = [q for q in result if q["subject"].lower() == subject.lower()]

    if level is not None:
        result = [q for q in result if q["level"].lower() == level.lower()]

    return result

def search_questions(questions, keyword):
    keyword = keyword.lower()
    result = [q for q in questions if keyword in q["question"].lower()]
    return result
        
def sort_questions(questions, sort_by="id", reverse=False):
    if sort_by not in ["id", "subject", "level"]:
        return questions

    return sorted(questions, key=lambda q: q[sort_by], reverse=reverse)

def check_enough_questions(questions, subject, num_easy, num_medium, num_hard):

    easy_questions = filter_questions(questions, subject=subject, level="De")
    medium_questions = filter_questions(questions, subject=subject, level="Vua")
    hard_questions = filter_questions(questions, subject=subject, level="Kho")

    if len(easy_questions) < num_easy:
        return False, "Khong du cau hoi muc De."
    if len(medium_questions) < num_medium:
        return False, "Khong du cau hoi muc Vua."
    if len(hard_questions) < num_hard:
        return False, "Khong du cau hoi muc Kho."

    return True, "Du so luong cau hoi."

def generate_exam(questions, subject, num_easy, num_medium, num_hard):
    if not validate_exam_request(num_easy, num_medium, num_hard):
        raise ValueError("So luong cau hoi yeu cau khong hop le.")

    enough, message = check_enough_questions(questions, subject, num_easy, num_medium, num_hard)
    if not enough:
        raise ValueError(message)

    easy_questions = filter_questions(questions, subject=subject, level="De")
    medium_questions = filter_questions(questions, subject=subject, level="Vua")
    hard_questions = filter_questions(questions, subject=subject, level="Kho")

    selected_easy = random.sample(easy_questions, num_easy)
    selected_medium = random.sample(medium_questions, num_medium)
    selected_hard = random.sample(hard_questions, num_hard)

    exam = selected_easy + selected_medium + selected_hard

    random.shuffle(exam)

    return exam

def take_exam(exam):
    user_answers = []

    print("\nBAT DAU BAI THI \n")

    for i, q in enumerate(exam, start=1):
        print(f"Cau {i}: {q['question']}")
        print(f"A. {q['options']['A']}")
        print(f"B. {q['options']['B']}")
        print(f"C. {q['options']['C']}")
        print(f"D. {q['options']['D']}")

        while True:
            answer = input("Nhap dap an (A/B/C/D): ").strip().upper()
            if validate_answer(answer):
                break
            else:
                print("Dap an khong hop le. Vui long nhap A, B, C hoac D.")

        user_answers.append({
            "question_id": q["id"],
            "user_answer": answer
        })

        print("-" * 40)

    print("KET THUC BAI THI\n")
    return user_answers

def grade_exam(exam, user_answers):
    answer_map = {}
    for item in user_answers:
        answer_map[item["question_id"]] = item["user_answer"]

    detailed_results = []

    for q in exam:
        qid = q["id"]
        correct_answer = q["answer"]
        user_answer = answer_map.get(qid, "")

        is_correct = (user_answer == correct_answer)

        detailed_results.append({
            "question_id": qid,
            "question": q["question"],
            "correct_answer": correct_answer,
            "user_answer": user_answer,
            "is_correct": is_correct
        })

    return detailed_results

def calculate_result(detailed_results):
    total = len(detailed_results)
    correct = sum(1 for item in detailed_results if item["is_correct"])
    wrong = total - correct

    if total == 0:
        score_10 = 0
        correct_percent = 0
        wrong_percent = 0
    else:
        score_10 = round((correct / total) * 10, 2)
        correct_percent = round((correct / total) * 100, 2)
        wrong_percent = round((wrong / total) * 100, 2)

    result = {
        "total_questions": total,
        "correct_answers": correct,
        "wrong_answers": wrong,
        "score_10": score_10,
        "correct_percent": correct_percent,
        "wrong_percent": wrong_percent
    }

    return result

def classify_score(score_10):
    if score_10 >= 8:
        return "Gioi"
    elif score_10 >= 6.5:
        return "Kha"
    elif score_10 >= 5:
        return "Trung binh"
    else:
        return "Yeu"

def process_exam(questions, subject, num_easy, num_medium, num_hard):
    exam = generate_exam(questions, subject, num_easy, num_medium, num_hard)
    user_answers = take_exam(exam)
    detailed_results = grade_exam(exam, user_answers)
    final_result = calculate_result(detailed_results)
    final_result["classification"] = classify_score(final_result["score_10"])

    return exam, user_answers, detailed_results, final_result

#TEST CODE
if __name__ == "__main__":
    questions = [
        {
            "id": 1,
            "subject": "Python",
            "level": "De",
            "question": "Python la ngon ngu gi?",
            "options": {
                "A": "Lap trinh",
                "B": "Co so du lieu",
                "C": "Mang",
                "D": "He dieu hanh"
            },
            "answer": "A"
        },
        {
            "id": 2,
            "subject": "Python",
            "level": "Vua",
            "question": "Lenh in ra man hinh trong Python la gi?",
            "options": {
                "A": "echo()",
                "B": "print()",
                "C": "show()",
                "D": "write()"
            },
            "answer": "B"
        },
        {
            "id": 3,
            "subject": "Python",
            "level": "Kho",
            "question": "Kieu du lieu nao dung de luu nhieu gia tri?",
            "options": {
                "A": "int",
                "B": "float",
                "C": "list",
                "D": "bool"
            },
            "answer": "C"
        }
    ]

    print("Kiem tra ngan hang cau hoi:", validate_question_bank(questions))

    exam = generate_exam(questions, "Python", 1, 1, 1)
    print("\nDe thi duoc tao:")
    for q in exam:
        print(q["id"], "-", q["question"])

    exam, user_answers, detailed_results, final_result = process_exam(questions, "Python", 1, 1, 1)

    print("\nKet qua cuoi cung:")
    print(final_result)

