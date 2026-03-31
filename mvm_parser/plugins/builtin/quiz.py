import html
from mvm_parser.plugins.base import ComponentPlugin
from mvm_parser.data_object import DataObject


class QuizPlugin(ComponentPlugin):
    name = "quiz"

    def render(self, section: "DataObject", children: list) -> str:
        heading = section.get("heading", "")
        heading_html = f'<h2 class="section-heading" data-searchable>{html.escape(heading)}</h2>\n' if heading else ""

        quizzes = ""
        for qi, s in enumerate(children):
            question = s.get("heading", "")
            options = s.get("items", [])
            correct = s.get("correct_answer", 0)
            explanation = s.get("body", "")
            opts_html = ""
            for oi, opt in enumerate(options):
                opts_html += (
                    f'<button class="quiz-option" '
                    f'data-quiz="{qi}" data-index="{oi}" '
                    f'data-correct="{correct}" '
                    f'onclick="checkAnswer(this)">'
                    f'<span class="quiz-label">'
                    f'{"ABCD"[oi]}</span> {html.escape(opt)}</button>\n'
                )
            quizzes += (
                f'<div class="quiz-item" data-quiz-id="{qi}">\n'
                f'<div class="quiz-question">\n'
                f'<span class="quiz-num">Q{qi+1}</span>\n'
                f'<span>{html.escape(question)}</span>\n'
                f'</div>\n'
                f'<div class="quiz-options">{opts_html}</div>\n'
                f'<div class="quiz-feedback" id="feedback-{qi}"></div>\n'
                f'<div class="quiz-explanation" id="explain-{qi}" style="display:none">'
                f'<div class="body">{html.escape(explanation)}</div></div>\n'
                f'</div>\n'
            )
        return (
            f'<div class="section quiz-group" data-section>\n{heading_html}{quizzes}</div>'
        )

    def get_css(self) -> str:
        return """
.quiz-item { margin: 20px 0; padding: 20px; background: var(--bg-secondary); border-radius: 12px; border: 1px solid var(--border); }
.quiz-question { font-size: 1.05em; margin-bottom: 14px; display: flex; gap: 10px; }
.quiz-num { color: var(--accent); font-weight: 700; }
.quiz-options { display: flex; flex-direction: column; gap: 8px; }
.quiz-option {
  padding: 10px 16px; background: var(--bg-primary); border: 2px solid var(--border);
  border-radius: 8px; cursor: pointer; text-align: left; font-size: 0.95em;
  transition: all 0.2s; display: flex; align-items: center; gap: 10px;
}
.quiz-option:hover:not(.selected) { border-color: var(--accent); background: var(--bg-hover); }
.quiz-option.correct { border-color: #27ae60; background: rgba(39,174,96,0.1); }
.quiz-option.wrong { border-color: #e74c3c; background: rgba(231,76,60,0.1); }
.quiz-label {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; border-radius: 50%; background: var(--border);
  font-size: 0.85em; font-weight: 700; flex-shrink: 0;
}
.quiz-feedback { margin-top: 10px; font-weight: 600; }
.quiz-explanation { margin-top: 10px; padding: 12px; background: rgba(52,152,219,0.1); border-radius: 8px; font-size: 0.9em; }
"""

    def get_js(self) -> str:
        return """
function checkAnswer(btn) {
  const quizId = btn.getAttribute('data-quiz');
  const correctIdx = btn.getAttribute('data-correct');
  const options = document.querySelectorAll('.quiz-option[data-quiz="' + quizId + '"]');
  const feedback = document.getElementById('feedback-' + quizId);
  const explain = document.getElementById('explain-' + quizId);
  options.forEach(o => { o.classList.add('selected'); o.disabled = true; });
  const idx = btn.getAttribute('data-index');
  if (idx === correctIdx) {
    btn.classList.add('correct');
    feedback.textContent = 'Correct!';
    feedback.style.color = '#27ae60';
  } else {
    btn.classList.add('wrong');
    options.forEach(o => { if (o.getAttribute('data-index') === correctIdx) o.classList.add('correct'); });
    feedback.textContent = 'Incorrect';
    feedback.style.color = '#e74c3c';
  }
  if (explain) explain.style.display = 'block';
}
"""
