import re
import json
import pdfplumber

PDF_PATH = "二等_無人航空機操縦者技能証明_問題集_OCR.pdf"

questions = {}
answers = {}

with pdfplumber.open(PDF_PATH) as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

# 設問抽出
question_pattern = re.compile(
    r"設問(\d+-\d+).*?\n(.*?)\na\.(.*?)\nb\.(.*?)\nc\.(.*?)(?=\n設問|\Z)",
    re.S
)

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
        "choices": choices
    }

# 正答と解説抽出
answer_pattern = re.compile(
    r"設問(\d+-\d+)正答と解説.*?正答[:：]\s*([abc]).*?説明[:：]\s*(.*?)(?=\n設問|\Z)",
    re.S
)

for match in answer_pattern.finditer(full_text):
    qid = match.group(1)
    answer_letter = match.group(2)
    explanation = match.group(3).strip()

    index = {"a":0, "b":1, "c":2}.get(answer_letter, 0)

    answers[qid] = {
        "answer": index,
        "explanation": explanation
    }

# マージ
final_data = []

for qid, qdata in questions.items():
    if qid in answers:
        qdata.update(answers[qid])
    else:
        qdata["answer"] = None
        qdata["explanation"] = ""

    final_data.append(qdata)

# JSON出力
with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print("questions.json を生成しました。")
