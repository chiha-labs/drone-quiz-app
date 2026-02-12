let questions = [];
let currentIndex = 0;
let wrongQuestions = [];

const cleanText = (text) =>
  text
    .replace(/\r?\n/g, " ")
    .replace(/\s+/g, " ")
    .replace(/　/g, " ")
    .trim();


fetch("questions.json")
  .then(res => res.json())
  .then(data => {
    questions = data;
    showQuestion();
  });

function showQuestion() {
  const quizDiv = document.getElementById("quiz");
  const nextBtn = document.getElementById("nextBtn");
  nextBtn.style.display = "none";

  const q = questions[currentIndex];

 quizDiv.innerHTML = `
  <h3>${cleanText(q.question)}</h3>
  ${q.choices.map((c, i) =>
    `<button onclick="checkAnswer(${i})">${cleanText(c)}</button>`
  ).join("")}
  <div id="result"></div>
`;

}

function checkAnswer(selected) {
  const q = questions[currentIndex];
  const resultDiv = document.getElementById("result");
  const buttons = document.querySelectorAll("button");

  buttons.forEach(b => b.disabled = true);

if (selected === q.answer) {
  resultDiv.innerHTML =
    `<p class="correct">正解！</p>
     <p>${cleanText(q.explanation)}</p>`;
} else {
  wrongQuestions.push(q);
  resultDiv.innerHTML =
    `<p class="wrong">不正解</p>
     <p>${cleanText(q.explanation)}</p>`;
}


  document.getElementById("nextBtn").style.display = "block";
}

document.getElementById("nextBtn").addEventListener("click", () => {
  currentIndex++;
  if (currentIndex < questions.length) {
    showQuestion();
  } else {
    alert("終了！");
  }
});
