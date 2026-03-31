import html
from mvm_parser.plugins.base import ComponentPlugin
from mvm_parser.data_object import DataObject


class TimelinePlugin(ComponentPlugin):
    name = "timeline"

    def render(self, section: "DataObject", children: list) -> str:
        heading = section.get("heading", "")
        heading_html = f'<h2 class="section-heading" data-searchable>{html.escape(heading)}</h2>\n' if heading else ""

        entries = ""
        for i, s in enumerate(children):
            h = s.get("heading", "")
            b = s.get("body", "")
            side = "left" if i % 2 == 0 else "right"
            entries += (
                f'<div class="timeline-item timeline-{side}">\n'
                f'<div class="timeline-dot"></div>\n'
                f'<div class="timeline-card">\n'
                f'<h3>{html.escape(h)}</h3>\n'
                f'<div class="body">{html.escape(b)}</div>\n'
                f'</div>\n</div>\n'
            )
        return (
            f'<div class="section timeline-group" data-section>\n'
            f'{heading_html}<div class="timeline">{entries}</div>\n</div>'
        )

    def get_css(self) -> str:
        return """
.timeline { position: relative; padding: 20px 0; }
.timeline::before {
  content: ''; position: absolute; left: 50%; top: 0; bottom: 0;
  width: 2px; background: var(--border); transform: translateX(-50%);
}
.timeline-item { position: relative; width: 50%; padding: 10px 30px; box-sizing: border-box; }
.timeline-left { left: 0; text-align: right; }
.timeline-right { left: 50%; text-align: left; }
.timeline-dot {
  position: absolute; top: 20px; width: 12px; height: 12px;
  background: var(--accent); border-radius: 50%; z-index: 1;
}
.timeline-left .timeline-dot { right: -6px; }
.timeline-right .timeline-dot { left: -6px; }
.timeline-card {
  background: var(--bg-secondary); border-radius: 8px; padding: 16px;
  border: 1px solid var(--border); display: inline-block; text-align: left;
  max-width: 100%;
}
@media (max-width: 768px) {
  .timeline::before { left: 20px; }
  .timeline-item { width: 100%; left: 0 !important; text-align: left !important; padding-left: 50px; }
  .timeline-dot { left: 14px !important; right: auto !important; }
}
"""

    def get_js(self) -> str:
        return ""
