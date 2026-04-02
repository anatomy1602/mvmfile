from mvm_parser.plugins.base import ComponentPlugin
from mvm_parser.data_object import DataObject


class CodePlugin(ComponentPlugin):
    name = "code"

    def render(self, section: "DataObject", children: list) -> str:
        language = section.get("language", "")
        content = section.get("content", "")

        html = '<div class="mvm-code-container">'
        if language:
            html += f'<div class="mvm-code-header"><span class="mvm-code-language">{language}</span></div>'
        
        html += f'<pre class="mvm-code"><code class="language-{language}">{content}</code></pre>'
        html += '</div>'
        return html

    def get_css(self) -> str:
        return """
.mvm-code-container {
    margin: 1em 0;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border);
}
.mvm-code-header {
    background: var(--bg-secondary);
    padding: 0.5em 1em;
    border-bottom: 1px solid var(--border);
}
.mvm-code-language {
    font-size: 0.85em;
    color: var(--text-light);
    text-transform: uppercase;
    font-weight: bold;
}
.mvm-code {
    margin: 0;
    padding: 1em;
    background: var(--bg-code);
    color: var(--text-code);
    overflow-x: auto;
    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
    font-size: 0.9em;
    line-height: 1.6;
}
.mvm-code code {
    display: block;
}
"""
