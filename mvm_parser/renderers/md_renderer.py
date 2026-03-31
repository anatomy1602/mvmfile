"""
MdRenderer - Markdown 渲染器
将 MVM 解析结果反向输出为 Markdown
"""

from ..data_object import DataObject
from ..renderers import BaseRenderer


class MdRenderer(BaseRenderer):
    capabilities = ["tree"]
    def file_extension(self) -> str:
        return "md"

    def render(self, result) -> str:
        data = result.data
        lines = []

        title = data.get("title", "")
        subtitle = data.get("subtitle", "")
        author = data.get("author", "")
        date = data.get("date", "")
        tags = data.get("tags", [])
        sections = data.get("sections", [])

        if title:
            lines.append(f"# {title}")
            lines.append("")

        if subtitle:
            lines.append(f"> {subtitle}")
            lines.append("")

        if author or date:
            meta_parts = []
            if author:
                meta_parts.append(f"**{author}**")
            if date:
                meta_parts.append(date)
            lines.append(" | ".join(meta_parts))
            lines.append("")

        if tags:
            lines.append(" ".join(f"`{t}`" for t in tags))
            lines.append("")

        lines.append("---")
        lines.append("")

        for i, section in enumerate(sections):
            if isinstance(section, DataObject):
                lines.append(self._render_section(section, i + 1))
                lines.append("")

        return "\n".join(lines)

    def _render_section(self, section: DataObject, index: int) -> str:
        lines = []
        heading = section.get("heading", "")
        body = section.get("body", "")
        fmt = section.get("format", "paragraph")
        items = section.get("items", [])
        source = section.get("source", "")
        children = section.get("children", [])
        image = section.get("image", "")
        audio = section.get("audio", "")
        video = section.get("video", "")

        if children and fmt in ("tab", "accordion", "quiz"):
            return self._render_container_section(section, index)

        if fmt == "quote":
            if heading:
                lines.append(f"> ### {heading}")
                lines.append(">")
            if body:
                for bline in body.split("\n"):
                    lines.append(f"> {bline}")
                lines.append(">")
        elif fmt == "code":
            if heading:
                lines.append(f"### {heading}")
                lines.append("")
            if body:
                lines.append("```")
                lines.append(body)
                lines.append("```")
                lines.append("")
        else:
            if heading:
                lines.append(f"## {heading}")
                lines.append("")

        if fmt not in ("quote", "code"):
            if image:
                lines.append(f"![image]({image})")
                lines.append("")
            if video:
                lines.append(f"[video]({video})")
                lines.append("")
            if audio:
                lines.append(f"[audio]({audio})")
                lines.append("")
            if body:
                lines.append(body)
                lines.append("")

        if items:
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

        if source:
            lines.append(f"[source]({source})")
            lines.append("")

        return "\n".join(lines)

    def _render_container_section(self, section: DataObject, index: int) -> str:
        lines = []
        heading = section.get("heading", "")
        fmt = section.get("format", "paragraph")
        children = section.get("children", [])

        if heading:
            lines.append(f"## {heading}")
            lines.append("")

        if fmt == "tab":
            for i, child in enumerate(children):
                if not isinstance(child, DataObject):
                    continue
                h = child.get("heading", f"Tab {i+1}")
                b = child.get("body", "")
                lines.append(f"### {h}")
                lines.append("")
                if b:
                    lines.append(b)
                    lines.append("")
        elif fmt == "accordion":
            for child in children:
                if not isinstance(child, DataObject):
                    continue
                h = child.get("heading", "")
                b = child.get("body", "")
                lines.append(f"<details>")
                lines.append(f"<summary>{h}</summary>")
                lines.append("")
                if b:
                    lines.append(b)
                    lines.append("")
                lines.append(f"</details>")
                lines.append("")
        elif fmt == "quiz":
            for qi, child in enumerate(children):
                if not isinstance(child, DataObject):
                    continue
                q = child.get("heading", "")
                opts = child.get("items", [])
                correct = child.get("correct_answer", 0)
                explanation = child.get("body", "")
                lines.append(f"**Q{qi+1}: {q}**")
                lines.append("")
                for oi, opt in enumerate(opts):
                    marker = "✅" if oi == correct else "○"
                    lines.append(f"- {marker} {opt}")
                lines.append("")
                if explanation:
                    lines.append(f"> {explanation}")
                    lines.append("")

        return "\n".join(lines)
