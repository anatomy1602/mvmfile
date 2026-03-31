"""
WebRenderer - 网页渲染器
将 MVM 解析结果渲染为完整的 HTML 页面
"""

import html
from ..data_object import DataObject
from ..renderers import BaseRenderer


class WebRenderer(BaseRenderer):
    capabilities = ["media", "tree"]
    def file_extension(self) -> str:
        return "html"

    def render(self, result) -> str:
        data = result.data
        title = data.get("title", "MVM Document")
        subtitle = data.get("subtitle", "")
        author = data.get("author", "")
        date = data.get("date", "")
        tags = data.get("tags", [])
        sections = data.get("sections", [])

        sections_html = ""
        for section in sections:
            if isinstance(section, DataObject):
                sections_html += self._render_section(section)

        tags_html = " ".join(f'<span class="tag">{html.escape(t)}</span>' for t in tags)

        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.8;
  color: #1a1a2e;
  background: #fafafa;
}}
.container {{
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 24px;
}}
.header {{
  margin-bottom: 48px;
  padding-bottom: 32px;
  border-bottom: 2px solid #e8e8e8;
}}
.header h1 {{
  font-size: 2.2em;
  font-weight: 700;
  margin-bottom: 8px;
  color: #16213e;
}}
.header .subtitle {{
  font-size: 1.2em;
  color: #666;
  margin-bottom: 16px;
}}
.meta {{
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  color: #888;
  font-size: 0.9em;
  margin-bottom: 12px;
}}
.tags {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}}
.tag {{
  background: #e8f4f8;
  color: #2980b9;
  padding: 2px 12px;
  border-radius: 12px;
  font-size: 0.85em;
}}
.section {{
  margin-bottom: 36px;
}}
.section h2 {{
  font-size: 1.5em;
  font-weight: 600;
  margin-bottom: 12px;
  color: #16213e;
  padding-left: 12px;
  border-left: 4px solid #3498db;
}}
.section.format-quote {{
  background: #f0f7ff;
  border-left: 4px solid #3498db;
  padding: 20px 24px;
  border-radius: 0 8px 8px 0;
  margin: 24px 0;
}}
.section.format-quote h2 {{
  border-left: none;
  padding-left: 0;
  margin-bottom: 8px;
  font-size: 1.1em;
  color: #2980b9;
}}
.section.format-code {{
  background: #1e1e2e;
  color: #cdd6f4;
  padding: 20px 24px;
  border-radius: 8px;
  margin: 24px 0;
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 0.9em;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
}}
.section.format-code h2 {{
  color: #89b4fa;
  border-left-color: #89b4fa;
  background: none;
  padding: 0 0 12px 12px;
  margin-bottom: 16px;
  font-size: 1.1em;
}}
.section.format-code .body {{
  white-space: pre-wrap;
}}
.section.format-list h2 {{
  border-left-color: #27ae60;
}}
.section.format-tip {{
  background: #fef9e7;
  border-left: 4px solid #f39c12;
  padding: 20px 24px;
  border-radius: 0 8px 8px 0;
  margin: 24px 0;
}}
.section.format-tip h2 {{
  border-left: none;
  padding-left: 0;
  margin-bottom: 8px;
  font-size: 1.1em;
  color: #e67e22;
}}
.section.format-warning {{
  background: #fdedec;
  border-left: 4px solid #e74c3c;
  padding: 20px 24px;
  border-radius: 0 8px 8px 0;
  margin: 24px 0;
}}
.section.format-warning h2 {{
  border-left: none;
  padding-left: 0;
  margin-bottom: 8px;
  font-size: 1.1em;
  color: #c0392b;
}}
.body {{
  margin-top: 8px;
  white-space: pre-wrap;
}}
.items {{
  list-style: none;
  padding: 0;
  margin-top: 12px;
}}
.items li {{
  padding: 6px 0 6px 20px;
  position: relative;
}}
.items li::before {{
  content: "\\2022";
  position: absolute;
  left: 0;
  color: #3498db;
  font-weight: bold;
}}
.source {{
  margin-top: 8px;
  font-size: 0.85em;
}}
.source a {{
  color: #3498db;
  text-decoration: none;
}}
.source a:hover {{
  text-decoration: underline;
}}
.format-tab .tab-list {{
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  overflow: hidden;
}}
.format-tab .tab-item {{
  padding: 16px 20px;
  border-bottom: 1px solid #e8e8e8;
}}
.format-tab .tab-item:last-child {{
  border-bottom: none;
}}
.format-tab .tab-item h3 {{
  font-size: 1.1em;
  color: #3498db;
  margin-bottom: 8px;
}}
.format-accordion .accordion-list {{
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  overflow: hidden;
}}
.format-accordion .accordion-item {{
  border-bottom: 1px solid #e8e8e8;
}}
.format-accordion .accordion-item:last-child {{
  border-bottom: none;
}}
.format-accordion .accordion-item summary {{
  padding: 12px 20px;
  cursor: pointer;
  font-weight: 600;
  color: #16213e;
  background: #f8f9fa;
}}
.format-accordion .accordion-item summary:hover {{
  background: #eef1f5;
}}
.format-accordion .accordion-item .body {{
  padding: 12px 20px;
}}
.media-image {{
  margin: 12px 0;
}}
.media-image img {{
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}}
.media-video {{
  margin: 12px 0;
}}
.media-video video {{
  max-width: 100%;
  border-radius: 8px;
}}
.media-audio {{
  margin: 12px 0;
}}
.media-audio audio {{
  width: 100%;
}}
.footer {{
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid #e8e8e8;
  color: #aaa;
  font-size: 0.85em;
  text-align: center;
}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>{html.escape(title)}</h1>
    {f'<div class="subtitle">{html.escape(subtitle)}</div>' if subtitle else ''}
    <div class="meta">
      {f'<span>{html.escape(author)}</span>' if author else ''}
      {f'<span>{html.escape(date)}</span>' if date else ''}
    </div>
    {f'<div class="tags">{tags_html}</div>' if tags else ''}
  </div>
  {sections_html}
  <div class="footer">
    Generated by MVM Parser &middot; {html.escape(title)}
  </div>
</div>
</body>
</html>"""

    def _render_section(self, section: DataObject) -> str:
        heading = section.get("heading", "")
        body = section.get("body", "")
        fmt = section.get("format", "paragraph")
        items = section.get("items", [])
        source = section.get("source", "")
        children = section.get("children", [])
        image = section.get("image", "")
        audio = section.get("audio", "")
        video = section.get("video", "")
        background = section.get("background", "")

        if children and fmt in ("tab", "accordion"):
            return self._render_container_section(section, children)

        css_class = f"format-{fmt}" if fmt != "paragraph" else ""
        heading_html = f"<h2>{html.escape(heading)}</h2>"

        body_html = ""
        if body:
            escaped_body = html.escape(body)
            body_html = f'<div class="body">{escaped_body}</div>'

        items_html = ""
        if items:
            li_items = "".join(f"<li>{html.escape(item)}</li>" for item in items)
            items_html = f'<ul class="items">{li_items}</ul>'

        source_html = ""
        if source:
            source_html = f'<div class="source"><a href="{html.escape(source)}">{html.escape(source)}</a></div>'

        media_html = self._render_media(image, audio, video)

        bg_style = f' style="background-image:url({html.escape(background)});background-size:cover;background-position:center;"' if background else ""

        return f'<div class="section {css_class}"{bg_style}>\n{heading_html}\n{media_html}\n{body_html}\n{items_html}\n{source_html}\n</div>'

    def _render_container_section(self, section: DataObject, children: list) -> str:
        fmt = section.get("format", "paragraph")
        heading = section.get("heading", "")
        heading_html = f"<h2>{html.escape(heading)}</h2>"

        if fmt == "tab":
            return self._render_static_tab(heading_html, children)
        elif fmt == "accordion":
            return self._render_static_accordion(heading_html, children)
        return self._render_section(section)

    def _render_static_tab(self, heading_html: str, children: list) -> str:
        tabs_html = ""
        for i, child in enumerate(children):
            if not isinstance(child, DataObject):
                continue
            h = child.get("heading", f"Tab {i+1}")
            b = child.get("body", "")
            body_part = f'<div class="body">{html.escape(b)}</div>\n' if b else ""
            tabs_html += (
                f'<div class="tab-item">\n'
                f'<h3>{html.escape(h)}</h3>\n'
                f'{body_part}'
                f'</div>\n'
            )
        return (
            f'<div class="section format-tab">\n{heading_html}\n'
            f'<div class="tab-list">{tabs_html}</div>\n</div>'
        )

    def _render_static_accordion(self, heading_html: str, children: list) -> str:
        items_html = ""
        for child in children:
            if not isinstance(child, DataObject):
                continue
            h = child.get("heading", "")
            b = child.get("body", "")
            body_part = f'<div class="body">{html.escape(b)}</div>\n' if b else ""
            items_html += (
                f'<details class="accordion-item">\n'
                f'<summary>{html.escape(h)}</summary>\n'
                f'{body_part}'
                f'</details>\n'
            )
        return (
            f'<div class="section format-accordion">\n{heading_html}\n'
            f'<div class="accordion-list">{items_html}</div>\n</div>'
        )

    def _render_media(self, image: str, audio: str, video: str) -> str:
        parts = []
        if image:
            parts.append(f'<div class="media-image"><img src="{html.escape(image)}" alt="" loading="lazy"></div>')
        if video:
            parts.append(f'<div class="media-video"><video controls><source src="{html.escape(video)}">Your browser does not support video.</video></div>')
        if audio:
            parts.append(f'<div class="media-audio"><audio controls><source src="{html.escape(audio)}">Your browser does not support audio.</audio></div>')
        return "\n".join(parts)
