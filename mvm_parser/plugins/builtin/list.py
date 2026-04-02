from mvm_parser.plugins.base import ComponentPlugin
from mvm_parser.data_object import DataObject


class ListPlugin(ComponentPlugin):
    name = "list"

    def render(self, section: "DataObject", children: list) -> str:
        ordered = section.get("ordered", False)
        items = section.get("items", [])

        tag = "ol" if ordered else "ul"
        list_class = "mvm-list-ordered" if ordered else "mvm-list-unordered"
        
        html = f'<{tag} class="mvm-list {list_class}">'
        
        for item in items:
            if isinstance(item, str):
                content = item
                subitems = []
            else:
                content = item.get("content", "")
                subitems = item.get("subitems", [])
            html += f'<li>{content}'
            if subitems:
                html += self._render_subitems(subitems, ordered)
            html += '</li>'
        
        html += f'</{tag}>'
        return html

    def _render_subitems(self, subitems: list, ordered: bool) -> str:
        tag = "ol" if ordered else "ul"
        list_class = "mvm-sublist-ordered" if ordered else "mvm-sublist-unordered"
        
        html = f'<{tag} class="mvm-sublist {list_class}">'
        for item in subitems:
            if isinstance(item, str):
                content = item
                sub_subitems = []
            else:
                content = item.get("content", "")
                sub_subitems = item.get("subitems", [])
            html += f'<li>{content}'
            if sub_subitems:
                html += self._render_subitems(sub_subitems, ordered)
            html += '</li>'
        html += f'</{tag}>'
        return html

    def get_css(self) -> str:
        return """
.mvm-list {
    margin: 0.5em 0;
    padding-left: 2em;
    color: var(--text-primary);
}
.mvm-list-ordered {
    list-style-type: decimal;
}
.mvm-list-unordered {
    list-style-type: disc;
}
.mvm-sublist {
    margin: 0.25em 0;
    padding-left: 1.5em;
}
.mvm-sublist-ordered {
    list-style-type: lower-alpha;
}
.mvm-sublist-unordered {
    list-style-type: circle;
}
.mvm-list li, .mvm-sublist li {
    margin: 0.25em 0;
    line-height: 1.6;
}
"""
