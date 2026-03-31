import html
from mvm_parser.plugins.base import ComponentPlugin
from mvm_parser.data_object import DataObject


class TabPlugin(ComponentPlugin):
    name = "tab"

    def render(self, section: "DataObject", children: list) -> str:
        heading = section.get("heading", "")
        safe_id = html.escape(heading or "default")
        heading_html = f'<h2 class="section-heading" data-searchable>{html.escape(heading)}</h2>\n' if heading else ""

        tab_btns = ""
        tab_panels = ""
        for i, s in enumerate(children):
            h = s.get("heading", f"Tab {i+1}")
            b = s.get("body", "")
            items_list = s.get("items", [])
            active = ' active' if i == 0 else ""
            tab_btns += (
                f'<button class="tab-btn{active}" '
                f'onclick="switchTab(this, \'{safe_id}\', {i})">'
                f"{html.escape(h)}</button>\n"
            )
            content = html.escape(b) if b else ""
            if items_list:
                content += '<ul class="items">' + "".join(
                    f"<li>{html.escape(it)}</li>" for it in items_list
                ) + "</ul>"
            tab_panels += (
                f'<div class="tab-panel{active}" '
                f'data-tab-group="{safe_id}" data-tab-index="{i}">'
                f'<div class="body">{content}</div></div>\n'
            )
        return (
            f'<div class="section tab-group" data-section>\n'
            f'{heading_html}'
            f'<div class="tab-bar">{tab_btns}</div>\n'
            f'<div class="tab-content">{tab_panels}</div>\n'
            f"</div>"
        )

    def get_css(self) -> str:
        return """
.tab-bar { display: flex; gap: 0; border-bottom: 2px solid var(--border); margin-bottom: 16px; }
.tab-btn {
  padding: 10px 20px; background: none; border: none; cursor: pointer;
  font-size: 0.95em; color: var(--text-light); border-bottom: 2px solid transparent;
  margin-bottom: -2px; transition: all 0.2s;
}
.tab-btn:hover { color: var(--text); }
.tab-btn.active { color: var(--accent); border-bottom-color: var(--accent); font-weight: 600; }
.tab-panel { display: none; padding: 16px 0; }
.tab-panel.active { display: block; }
"""

    def get_js(self) -> str:
        return """
function switchTab(btn, groupId, index) {
  const bar = btn.parentElement;
  bar.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('[data-tab-group="' + groupId + '"]').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('[data-tab-group="' + groupId + '"][data-tab-index="' + index + '"]').forEach(p => p.classList.add('active'));
}
"""
