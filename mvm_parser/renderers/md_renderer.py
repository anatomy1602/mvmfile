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

        if fmt == "table":
            return self._render_table_section(section)
        elif fmt == "list":
            return self._render_list_section(section)
        elif fmt == "quote":
            return self._render_quote_section(section)
        elif fmt == "code":
            return self._render_code_section(section)
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

    def _render_table_section(self, section: DataObject) -> str:
        lines = []
        heading = section.get("heading", "")
        caption = section.get("caption", "")
        columns = section.get("columns", [])
        rows = section.get("rows", [])

        if heading:
            lines.append(f"## {heading}")
            lines.append("")

        if caption:
            lines.append(f"*{caption}*")
            lines.append("")

        if columns and rows:
            header = " | ".join(col.get("label", "") for col in columns)
            lines.append(header)
            lines.append(" | ".join("---" for _ in columns))
            for row in rows:
                row_data = " | ".join(row.get(col.get("key", ""), "") for col in columns)
                lines.append(row_data)
            lines.append("")

        return "\n".join(lines)

    def _render_list_section(self, section: DataObject) -> str:
        lines = []
        heading = section.get("heading", "")
        ordered = section.get("ordered", False)
        items = section.get("items", [])

        if heading:
            lines.append(f"## {heading}")
            lines.append("")

        for i, item in enumerate(items):
            if isinstance(item, str):
                marker = f"{i+1}." if ordered else "-"
                lines.append(f"{marker} {item}")
            else:
                content = item.get("content", "")
                subitems = item.get("subitems", [])
                marker = f"{i+1}." if ordered else "-"
                lines.append(f"{marker} {content}")
                for subitem in subitems:
                    if isinstance(subitem, str):
                        lines.append(f"  - {subitem}")
                    else:
                        sub_content = subitem.get("content", "")
                        lines.append(f"  - {sub_content}")

        lines.append("")
        return "\n".join(lines)

    def _render_quote_section(self, section: DataObject) -> str:
        lines = []
        heading = section.get("heading", "")
        body = section.get("body", "")
        author = section.get("author", "")
        source = section.get("source", "")

        if heading:
            lines.append(f"## {heading}")
            lines.append("")

        if body:
            for bline in body.split("\n"):
                lines.append(f"> {bline}")
            lines.append(">")

        if author:
            lines.append(f"> — {author}")
            lines.append(">")

        if source:
            lines.append(f"> {source}")
            lines.append(">")

        return "\n".join(lines)

    def _render_code_section(self, section: DataObject) -> str:
        lines = []
        heading = section.get("heading", "")
        language = section.get("language", "")
        body = section.get("body", "")

        if heading:
            lines.append(f"## {heading}")
            lines.append("")

        if body:
            lines.append(f"```{language}")
            lines.append(body)
            lines.append("```")
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
