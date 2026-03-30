"""
Blocker - 分块器
将 .mvm 文件内容分割为 MODEL 区和 MSG 区
"""

import re
from dataclasses import dataclass


@dataclass
class BlockResult:
    model_text: str
    msg_text: str


class BlockerError(Exception):
    pass


class Blocker:
    MODEL_MARKER = "===MODEL==="
    MSG_MARKER = "===MSG==="

    def parse(self, content: str) -> BlockResult:
        lines = content.split("\n")
        model_lines = []
        msg_lines = []
        current_block = None
        model_start = -1
        msg_start = -1

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped == self.MODEL_MARKER:
                if current_block == "model":
                    raise BlockerError(
                        f"Line {i + 1}: Duplicate MODEL block found"
                    )
                if current_block == "msg":
                    raise BlockerError(
                        f"Line {i + 1}: MODEL block must come before MSG block"
                    )
                current_block = "model"
                model_start = i
                continue

            if stripped == self.MSG_MARKER:
                if current_block == "msg":
                    raise BlockerError(
                        f"Line {i + 1}: Duplicate MSG block found"
                    )
                if current_block is None:
                    raise BlockerError(
                        f"Line {i + 1}: MSG block found before MODEL block"
                    )
                current_block = "msg"
                msg_start = i
                continue

            if current_block == "model":
                model_lines.append(line)
            elif current_block == "msg":
                msg_lines.append(line)

        if current_block is None:
            raise BlockerError("No MODEL or MSG block found in file")

        if current_block != "msg":
            raise BlockerError("MSG block is missing")

        model_text = "\n".join(model_lines).strip()
        msg_text = "\n".join(msg_lines).strip()

        if not model_text:
            raise BlockerError("MODEL block is empty")

        return BlockResult(model_text=model_text, msg_text=msg_text)
