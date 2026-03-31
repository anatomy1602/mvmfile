"""
SlideRenderer - 幻灯片渲染器
将 MVM 解析结果渲染为 Reveal.js 幻灯片
"""

import html
from ..data_object import DataObject
from ..renderers import BaseRenderer


class SlideRenderer(BaseRenderer):
    def file_extension(self) -> str:
        return "html"

    def render(self, result) -> str:
        data = result.data
        title = data.get("title", "MVM Presentation")
        subtitle = data.get("subtitle", "")
        author = data.get("author", "")
        sections = data.get("sections", [])

        slides_html = self._render_title_slide(title, subtitle, author)

        content_sections = [s for s in sections if isinstance(s, DataObject)]
        for section in content_sections:
            children = section.get("children", [])
            fmt = section.get("format", "paragraph")
            if children and fmt in ("tab", "accordion", "quiz"):
                slides_html += self._render_container_slides(section, children)
            else:
                slides_html += self._render_single_section(section)

        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css">
<style>
.reveal {{
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}}
.reveal h1 {{
  font-size: 2.4em;
  color: #16213e;
  text-transform: none;
}}
.reveal h2 {{
  font-size: 1.6em;
  color: #16213e;
  text-transform: none;
  border-left: 4px solid #3498db;
  padding-left: 16px;
}}
.reveal .subtitle {{
  font-size: 1.2em;
  color: #666;
  margin-top: 16px;
}}
.reveal .author {{
  font-size: 0.9em;
  color: #888;
  margin-top: 32px;
}}
.slide-quote {{
  background: #f0f7ff;
  border-left: 4px solid #3498db;
  padding: 24px 32px;
  border-radius: 0 8px 8px 0;
  text-align: left;
  font-size: 0.9em;
}}
.slide-quote h2 {{
  border-left: none;
  padding-left: 0;
  color: #2980b9;
  font-size: 1.3em;
  margin-bottom: 12px;
}}
.slide-code {{
  background: #1e1e2e;
  color: #cdd6f4;
  padding: 24px 32px;
  border-radius: 8px;
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 0.75em;
  line-height: 1.5;
  text-align: left;
  white-space: pre-wrap;
}}
.slide-code h2 {{
  color: #89b4fa;
  border-left-color: #89b4fa;
  background: none;
  padding: 0 0 12px 12px;
  font-size: 1.2em;
}}
.slide-list {{
  text-align: left;
}}
.slide-list ul {{
  list-style: none;
  padding: 0;
}}
.slide-list li {{
  padding: 8px 0 8px 24px;
  position: relative;
  font-size: 0.9em;
}}
.slide-list li::before {{
  content: "\\2022";
  position: absolute;
  left: 0;
  color: #3498db;
  font-weight: bold;
  font-size: 1.2em;
}}
.slide-tip {{
  background: #fef9e7;
  border-left: 4px solid #f39c12;
  padding: 24px 32px;
  border-radius: 0 8px 8px 0;
  text-align: left;
  font-size: 0.9em;
}}
.slide-tip h2 {{
  border-left: none;
  padding-left: 0;
  color: #e67e22;
  font-size: 1.3em;
  margin-bottom: 12px;
}}
.slide-body {{
  white-space: pre-wrap;
  font-size: 0.85em;
  line-height: 1.6;
  text-align: left;
}}
</style>
</head>
<body>
<div class="reveal">
<div class="slides">
{slides_html}
</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script>
Reveal.initialize({{
  hash: true,
  slideNumber: true,
  transition: 'slide',
  width: 960,
  height: 700,
}});
</script>
</body>
</html>"""

    def _render_title_slide(self, title: str, subtitle: str, author: str) -> str:
        return f"""<section>
<h1>{html.escape(title)}</h1>
{f'<div class="subtitle">{html.escape(subtitle)}</div>' if subtitle else ''}
{f'<div class="author">{html.escape(author)}</div>' if author else ''}
</section>"""

    def _render_content_slide(self, sections: list) -> str:
        if len(sections) == 1:
            return self._render_single_section(sections[0])
        return self._render_two_sections(sections[0], sections[1])

    def _render_single_section(self, section: DataObject) -> str:
        heading = section.get("heading", "")
        body = section.get("body", "")
        fmt = section.get("format", "paragraph")
        items = section.get("items", [])
        image = section.get("image", "")
        audio = section.get("audio", "")
        video = section.get("video", "")
        background = section.get("background", "")

        heading_html = f"<h2>{html.escape(heading)}</h2>"

        if fmt == "quote":
            body_html = f'<div class="slide-quote">{heading_html}<div class="slide-body">{html.escape(body)}</div></div>'
            return f"<section>\n{body_html}\n</section>"

        if fmt == "code":
            body_html = f'<div class="slide-code">{heading_html}<div class="slide-body">{html.escape(body)}</div></div>'
            return f"<section>\n{body_html}\n</section>"

        if fmt == "tip":
            body_html = f'<div class="slide-tip">{heading_html}<div class="slide-body">{html.escape(body)}</div></div>'
            return f"<section>\n{body_html}\n</section>"

        if fmt == "list" and items:
            li_items = "".join(f"<li>{html.escape(item)}</li>" for item in items)
            list_html = f'<div class="slide-list">{heading_html}<ul>{li_items}</ul></div>'
            return f"<section>\n{list_html}\n</section>"

        body_html = f'<div class="slide-body">{html.escape(body)}</div>' if body else ""
        media_html = ""
        if image:
            media_html += f'<div class="slide-media"><img src="{html.escape(image)}" alt="" style="max-width:100%;border-radius:8px;"></div>'
        if video:
            media_html += f'<div class="slide-media"><video controls style="max-width:100%;"><source src="{html.escape(video)}"></video></div>'
        bg_style = f' data-background-image="{html.escape(background)}"' if background else ""
        return f"<section{bg_style}>\n{heading_html}\n{media_html}\n{body_html}\n</section>"

    def _render_container_slides(self, section: DataObject, children: list) -> str:
        heading = section.get("heading", "")
        fmt = section.get("format", "paragraph")
        slides = ""

        title_slide = f'<section>\n<h2>{html.escape(heading)}</h2>\n</section>'
        slides += title_slide

        for child in children:
            if not isinstance(child, DataObject):
                continue
            child_fmt = fmt
            if fmt == "quiz":
                slides += self._render_quiz_slide(child)
            else:
                slides += self._render_single_section(child)

        return slides

    def _render_quiz_slide(self, section: DataObject) -> str:
        question = section.get("heading", "")
        options = section.get("items", [])
        correct = section.get("correct_answer", 0)
        explanation = section.get("body", "")

        heading_html = f"<h2>{html.escape(question)}</h2>"
        opts_html = ""
        for oi, opt in enumerate(options):
            marker = "✅ " if oi == correct else "○ "
            opts_html += f"<li>{marker}{html.escape(opt)}</li>"
        opts_block = f"<ul>{opts_html}</ul>"
        explain_html = f'<div class="slide-body" style="margin-top:16px;font-size:0.85em;color:#666;">{html.escape(explanation)}</div>' if explanation else ""

        return f"<section>\n{heading_html}\n{opts_block}\n{explain_html}\n</section>"

    def _render_two_sections(self, s1: DataObject, s2: DataObject) -> str:
        h1 = s1.get("heading", "")
        b1 = s1.get("body", "")
        f1 = s1.get("format", "paragraph")
        items1 = s1.get("items", [])

        h2 = s2.get("heading", "")
        b2 = s2.get("body", "")
        f2 = s2.get("format", "paragraph")
        items2 = s2.get("items", [])

        def mini_section(h, b, f, items):
            parts = [f"<h3>{html.escape(h)}</h3>"]
            if f == "quote":
                parts.append(f'<blockquote>{html.escape(b)}</blockquote>')
            elif f == "list" and items:
                li = "".join(f"<li>{html.escape(it)}</li>" for it in items)
                parts.append(f"<ul>{li}</ul>")
            else:
                parts.append(f'<div class="slide-body">{html.escape(b)}</div>')
            return "\n".join(parts)

        left = mini_section(h1, b1, f1, items1)
        right = mini_section(h2, b2, f2, items2)

        return f"""<section>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:32px;text-align:left;">
<div>{left}</div>
<div>{right}</div>
</div>
</section>"""
