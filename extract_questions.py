import re
import json
import pdfplumber

PDF_PATH = "二等_無人航空機操縦者技能証明_問題集_OCR.pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

# 問題抽出（問題ページだけ）
question_pattern = re.compile(
    r"設問(\d+-\d+)\s*(.*?)\s*a\.\s*(.*?)\s*b\.\s*(.*?)\s*c\.\s*(.*?)(?=設問\d+-\d+|\Z)",
    re.S
)

questions = {}

for match in question_pattern.finditer(full_text):
    qid = match.group(1)
    question = match.group(2).strip()
    choices = [
        match.group(3).strip(),
        match.group(4).strip(),
        match.group(5).strip()
    ]

    questions[qid] = {
        "id": qid,
        "question": question,
        "choices": choices,
        "answer": None,
        "explanation": ""
    }

# 正答と解説抽出（解説ページのみ）
answer_pattern = re.compile(
    r"設問(\d+-\d+)\s*正答[:：]\s*([abc]).*?説明[:：]\s*(.*?)(?=設問\d+-\d+|\Z)",
    re.S
)

for match in answer_pattern.finditer(full_text):
    qid = match.group(1)
    answer_letter = match.group(2)
    explanation = match.group(3).strip()

    if qid in questions:
        questions[qid]["answer"] = {"a":0, "b":1, "c":2}[answer_letter]
        questions[qid]["explanation"] = explanation

final_data = list(questions.values())

with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("再生成完了")
