import random
import difflib

# VALIDATION 
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

    ids = []
    for q in questions:
        for key in required_keys:
            if key not in q:
                return False

        if not all(opt in q["options"] for opt in ["A", "B", "C", "D"]):
            return False

        if q["answer"] not in ["A", "B", "C", "D"]:
            return False

        ids.append(q["id"])

    # kiểm tra trùng ID
    if len(ids) != len(set(ids)):
        return False

    return True

#  SEARCH & SORT 
def search_questions(questions, keyword):
    keyword = keyword.lower()
    return [q for q in questions if keyword in q["question"].lower()]

# tìm gần đúng (fuzzy search)
def search_questions_fuzzy(questions, keyword):
    result = []
    for q in questions:
        matches = difflib.get_close_matches(keyword.lower(), [q["question"].lower()], n=1, cutoff=0.4)
        if matches:
            result.append(q)
    return result

def sort_questions(questions, sort_by="id", reverse=False):
    if sort_by not in ["id", "subject", "level"]:
        return questions
    return sorted(questions, key=lambda q: q[sort_by], reverse=reverse)

#  FILTER 
def filter_questions(questions, subject=None, level=None):
    result = questions
    if subject:
        result = [q for q in result if q["subject"].lower() == subject.lower()]
    if level:
        result = [q for q in result if q["level"].lower() == level.lower()]
    return result

#  GENERATE EXAM 
def check_enough_questions(questions, subject, num_easy, num_medium, num_hard):
    if len(filter_questions(questions, subject, "De")) < num_easy:
        return False, "Không đủ câu hỏi dễ"
    if len(filter_questions(questions, subject, "Vua")) < num_medium:
        return False, "Không đủ câu hỏi vừa"
    if len(filter_questions(questions, subject, "Kho")) < num_hard:
        return False, "Không đủ câu hỏi khó"
    return True, "OK"

def generate_exam(questions, subject, num_easy, num_medium, num_hard):
    if not validate_exam_request(num_easy, num_medium, num_hard):
        raise ValueError("Yêu cầu đề không hợp lệ")

    enough, msg = check_enough_questions(questions, subject, num_easy, num_medium, num_hard)
    if not enough:
        raise ValueError(msg)

    exam = (
        random.sample(filter_questions(questions, subject, "De"), num_easy) +
        random.sample(filter_questions(questions, subject, "Vua"), num_medium) +
        random.sample(filter_questions(questions, subject, "Kho"), num_hard)
    )

    random.shuffle(exam)
    return exam

#  TAKE EXAM 
def take_exam(exam):
    answers = []
    print("\n=== BẮT ĐẦU THI ===\n")

    for i, q in enumerate(exam, 1):
        print(f"Câu {i}: {q['question']}")
        for k, v in q["options"].items():
            print(f"{k}. {v}")

        while True:
            try:
                ans = input("Đáp án: ").strip().upper()
                if validate_answer(ans):
                    break
                else:
                    print("Sai định dạng! Nhập A/B/C/D")
            except Exception:
                print("Lỗi nhập!")

        answers.append({"id": q["id"], "answer": ans})
        print("-" * 30)

    return answers

#  GRADING 
def grade_exam(exam, user_answers):
    answer_map = {a["id"]: a["answer"] for a in user_answers}
    results = []

    for q in exam:
        correct = q["answer"]
        user = answer_map.get(q["id"], "")
        results.append({
            "question": q["question"],
            "correct": correct,
            "user": user,
            "is_correct": correct == user
        })

    return results

def calculate_result(results):
    total = len(results)
    correct = sum(r["is_correct"] for r in results)

    score = round((correct / total) * 10, 2) if total else 0
    percent = round((correct / total) * 100, 2) if total else 0

    return {
        "total": total,
        "correct": correct,
        "score": score,
        "percent": percent
    }

def classify(score):
    if score >= 8: return "Giỏi"
    if score >= 6.5: return "Khá"
    if score >= 5: return "Trung bình"
    return "Yếu"

#  AUTO ID 
def generate_id(questions):
    return max(q["id"] for q in questions) + 1 if questions else 1

# MAIN 
if __name__ == "__main__":
    questions = [
        {"id": 1, "subject": "Python", "level": "De",
         "question": "Python là gì?",
         "options": {"A": "Ngôn ngữ lập trình", "B": "CSDL", "C": "Mạng", "D": "OS"},
         "answer": "A"},

        {"id": 2, "subject": "Python", "level": "Vua",
         "question": "Lệnh in?",
         "options": {"A": "echo()", "B": "print()", "C": "show()", "D": "write()"},
         "answer": "B"},

        {"id": 3, "subject": "Python", "level": "Kho",
         "question": "Kiểu lưu nhiều giá trị?",
         "options": {"A": "int", "B": "float", "C": "list", "D": "bool"},
         "answer": "C"},
    ]

    # validate
    if not validate_question_bank(questions):
        print("Ngân hàng câu hỏi lỗi!")
        exit()

    # test search gần đúng
    print("\nTìm gần đúng 'pythn':")
    print(search_questions_fuzzy(questions, "pythn"))

    try:
        exam = generate_exam(questions, "Python", 1, 1, 1)
        answers = take_exam(exam)
        results = grade_exam(exam, answers)
        final = calculate_result(results)
        final["classification"] = classify(final["score"])

        print("\nKẾT QUẢ")
        print(final)

    except Exception as e:
        print("Lỗi:", e)
