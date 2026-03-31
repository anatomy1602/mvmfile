import html
from mvm_parser.plugins.base import ComponentPlugin
from mvm_parser.data_object import DataObject


class RevealPlugin(ComponentPlugin):
    name = "reveal"

    def render(self, section: "DataObject", children: list) -> str:
        heading = section.get("heading", "")
        safe_id = html.escape(heading or "default")
        heading_html = f'<h2 class="section-heading" data-searchable>{html.escape(heading)}</h2>\n' if heading else ""

        steps = ""
        for i, s in enumerate(children):
            h = s.get("heading", "")
            b = s.get("body", "")
            steps += (
                f'<div class="reveal-step" '
                f'data-reveal-group="{safe_id}" data-reveal-step="{i}">\n'
                f'<h3>{html.escape(h)}</h3>\n'
                f'<div class="body">{html.escape(b)}</div>\n'
                f'</div>\n'
            )
        return (
            f'<div class="section reveal-group" data-section>\n'
            f'{heading_html}<div class="reveal-steps">{steps}</div>\n'
            f'<div class="reveal-controls">\n'
            f'<button class="reveal-btn" onclick="revealNext(\'{safe_id}\', 1)">'
            f'Next &#8594;</button>\n'
            f'<button class="reveal-btn" onclick="revealNext(\'{safe_id}\', -1)">'
            f'&#8592; Prev</button>\n'
            f'<button class="reveal-btn" onclick="revealAll(\'{safe_id}\')">'
            f'Show All</button>\n'
            f'</div>\n</div>'
        )

    def get_css(self) -> str:
        return """
.reveal-step { opacity: 0; transform: translateY(20px); transition: all 0.5s ease; margin: 16px 0; padding: 16px; background: var(--bg-secondary); border-radius: 8px; border-left: 3px solid var(--accent); }
.reveal-step.visible { opacity: 1; transform: translateY(0); }
.reveal-controls { display: flex; gap: 10px; margin-top: 16px; }
.reveal-btn {
  padding: 8px 18px; background: var(--accent); color: #fff; border: none;
  border-radius: 6px; cursor: pointer; font-size: 0.9em; transition: opacity 0.2s;
}
.reveal-btn:hover { opacity: 0.85; }
"""

    def get_js(self) -> str:
        return """
function revealNext(groupId, dir) {
  const steps = document.querySelectorAll('[data-reveal-group="' + groupId + '"]');
  const visible = [...steps].filter(s => s.classList.contains('visible')).length;
  const target = Math.max(0, Math.min(steps.length, visible + dir));
  steps.forEach((s, i) => { if (i < target) s.classList.add('visible'); else s.classList.remove('visible'); });
}
function revealAll(groupId) {
  document.querySelectorAll('[data-reveal-group="' + groupId + '"]').forEach(s => s.classList.add('visible'));
}
"""
