import html
from mvm_parser.plugins.base import ComponentPlugin
from mvm_parser.data_object import DataObject


class AccordionPlugin(ComponentPlugin):
    name = "accordion"

    def render(self, section: "DataObject", children: list) -> str:
        heading = section.get("heading", "")
        heading_html = f'<h2 class="section-heading" data-searchable>{html.escape(heading)}</h2>\n' if heading else ""

        panels = ""
        for i, s in enumerate(children):
            h = s.get("heading", f"Section {i+1}")
            b = s.get("body", "")
            items_list = s.get("items", [])
            content = html.escape(b) if b else ""
            if items_list:
                content += '<ul class="items">' + "".join(
                    f"<li>{html.escape(it)}</li>" for it in items_list
                ) + "</ul>"
            panels += (
                f'<div class="accordion-item">\n'
                f'<button class="accordion-header" '
                f'onclick="toggleAccordion(this)">\n'
                f'<span>{html.escape(h)}</span>\n'
                f'<span class="accordion-arrow">&#9660;</span>\n'
                f'</button>\n'
                f'<div class="accordion-body"><div class="body">{content}</div></div>\n'
                f'</div>\n'
            )
        return (
            f'<div class="section accordion-group" data-section>\n{heading_html}{panels}</div>'
        )

    def get_css(self) -> str:
        return """
.accordion-item { border: 1px solid var(--border); border-radius: 8px; margin-bottom: 8px; overflow: hidden; }
.accordion-header {
  width: 100%; padding: 14px 18px; background: var(--bg-secondary); border: none;
  cursor: pointer; display: flex; justify-content: space-between; align-items: center;
  font-size: 1em; color: var(--text); text-align: left; transition: background 0.2s;
}
.accordion-header:hover { background: var(--bg-hover); }
.accordion-arrow { transition: transform 0.3s; font-size: 0.8em; }
.accordion-item.open .accordion-arrow { transform: rotate(180deg); }
.accordion-body { max-height: 0; overflow: hidden; transition: max-height 0.3s ease; }
.accordion-item.open .accordion-body { max-height: 2000px; }
.accordion-body .body { padding: 14px 18px; }
"""

    def get_js(self) -> str:
        return """
function toggleAccordion(btn) {
  const item = btn.parentElement;
  item.classList.toggle('open');
}
"""
