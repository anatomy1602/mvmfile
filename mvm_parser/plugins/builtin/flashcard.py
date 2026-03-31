import html
from mvm_parser.plugins.base import ComponentPlugin
from mvm_parser.data_object import DataObject


class FlashcardPlugin(ComponentPlugin):
    name = "flashcard"

    def render(self, section: "DataObject", children: list) -> str:
        heading = section.get("heading", "")
        heading_html = f'<h2 class="section-heading" data-searchable>{html.escape(heading)}</h2>\n' if heading else ""

        cards = ""
        for s in children:
            front = s.get("heading", "")
            back = s.get("body", "")
            cards += (
                f'<div class="flashcard" onclick="flipCard(this)">\n'
                f'<div class="flashcard-inner">\n'
                f'<div class="flashcard-front">\n'
                f'<div class="body">{html.escape(front)}</div>\n'
                f'</div>\n'
                f'<div class="flashcard-back">\n'
                f'<div class="body">{html.escape(back)}</div>\n'
                f'</div>\n'
                f'</div>\n</div>\n'
            )
        return (
            f'<div class="section flashcard-group" data-section>\n'
            f'{heading_html}<div class="flashcard-grid">{cards}</div>\n'
            f'<p class="flashcard-hint">Click card to flip</p>\n'
            f"</div>"
        )

    def get_css(self) -> str:
        return """
.flashcard-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; margin: 16px 0; }
.flashcard { perspective: 1000px; cursor: pointer; height: 200px; }
.flashcard-inner {
  position: relative; width: 100%; height: 100%;
  transition: transform 0.6s; transform-style: preserve-3d;
}
.flashcard.flipped .flashcard-inner { transform: rotateY(180deg); }
.flashcard-front, .flashcard-back {
  position: absolute; width: 100%; height: 100%; backface-visibility: hidden;
  border-radius: 12px; display: flex; align-items: center; justify-content: center;
  padding: 20px; box-sizing: border-box;
}
.flashcard-front { background: var(--bg-secondary); border: 2px solid var(--border); }
.flashcard-back { background: var(--accent); color: #fff; transform: rotateY(180deg); }
.flashcard-hint { text-align: center; color: var(--text-light); font-size: 0.85em; }
"""

    def get_js(self) -> str:
        return """
function flipCard(card) { card.classList.toggle('flipped'); }
"""
