from mvm_parser.plugins.base import ComponentPlugin
from mvm_parser.data_object import DataObject


class QuotePlugin(ComponentPlugin):
    name = "quote"

    def render(self, section: "DataObject", children: list) -> str:
        content = section.get("content", "")
        author = section.get("author", "")
        source = section.get("source", "")

        html = '<blockquote class="mvm-quote">'
        html += f'<div class="mvm-quote-content">{content}</div>'
        
        if author or source:
            html += '<div class="mvm-quote-footer">'
            if author:
                html += f'<span class="mvm-quote-author">— {author}</span>'
            if source:
                html += f'<span class="mvm-quote-source">《{source}》</span>'
            html += '</div>'
        
        html += '</blockquote>'
        return html

    def get_css(self) -> str:
        return """
.mvm-quote {
    margin: 1.5em 0;
    padding: 1em 1.5em;
    border-left: 4px solid var(--accent);
    background: var(--bg-secondary);
    color: var(--text-primary);
}
.mvm-quote-content {
    font-style: italic;
    line-height: 1.6;
}
.mvm-quote-footer {
    margin-top: 0.5em;
    font-size: 0.9em;
    color: var(--text-light);
}
.mvm-quote-author {
    margin-right: 0.5em;
}
.mvm-quote-source {
    font-style: italic;
}
"""
