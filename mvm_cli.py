"""
MVM CLI - 命令行工具
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mvm_parser.parser import MVMParser, MVMParseError
from mvm_parser.renderers.web_renderer import WebRenderer
from mvm_parser.renderers.md_renderer import MdRenderer
from mvm_parser.renderers.slide_renderer import SlideRenderer
from mvm_parser.renderers.interactive_renderer import InteractiveWebRenderer

RENDERERS = {
    "web": WebRenderer,
    "md": MdRenderer,
    "slide": SlideRenderer,
    "interactive": InteractiveWebRenderer,
}


def cmd_parse(args):
    parser = MVMParser()
    try:
        result = parser.parse_file(args.file)
    except MVMParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        print(f"Output written to {args.output}")
    else:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))


def cmd_validate(args):
    parser = MVMParser()
    try:
        result = parser.parse_file(args.file)
        print(f"Valid: {args.file}")
        print(f"  Schema version: {result.schema.version}")
        print(f"  Root type: {result.schema.root_type}")
        print(f"  Types defined: {', '.join(result.schema.types.keys())}")
        print(f"  Data fields: {', '.join(result.data.fields.keys())}")
    except MVMParseError as e:
        print(f"Invalid: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)


def cmd_show(args):
    parser = MVMParser()
    try:
        result = parser.parse_file(args.file)
        print(result.data)
    except MVMParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)


def cmd_render(args):
    parser = MVMParser()
    try:
        result = parser.parse_file(args.file)
    except MVMParseError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)

    renderer_name = args.renderer
    if renderer_name not in RENDERERS:
        print(f"Error: Unknown renderer '{renderer_name}'", file=sys.stderr)
        print(f"Available renderers: {', '.join(RENDERERS.keys())}", file=sys.stderr)
        sys.exit(1)

    renderer = RENDERERS[renderer_name]()
    kwargs = {}
    if renderer_name == "interactive" and args.dark:
        kwargs["dark"] = True
    if renderer_name == "interactive" and hasattr(renderer, "load_plugins_from_dir"):
        if args.plugin_dir:
            count = renderer.load_plugins_from_dir(args.plugin_dir)
            if count:
                print(f"Loaded {count} plugin(s) from {args.plugin_dir}", file=sys.stderr)
        mvm_dir = os.path.dirname(os.path.abspath(args.file))
        plugins_dir = os.path.join(mvm_dir, "plugins")
        if os.path.isdir(plugins_dir):
            count = renderer.load_plugins_from_dir(plugins_dir)
            if count:
                print(f"Loaded {count} plugin(s) from {plugins_dir}", file=sys.stderr)
    missing = renderer.check_requirements(result.schema.requires)
    if missing:
        print(
            f"Warning: Renderer '{renderer_name}' does not support: {', '.join(missing)}",
            file=sys.stderr,
        )
    output = renderer.render(result, **kwargs)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Rendered to {args.output} (renderer: {renderer_name})")
    else:
        print(output)


def main():
    p = argparse.ArgumentParser(
        prog="mvm",
        description="MVM file format parser & renderer - .mvm 文件格式解析器与渲染器",
    )
    sub = p.add_subparsers(dest="command", help="Available commands")

    p_parse = sub.add_parser("parse", help="Parse .mvm file and output JSON")
    p_parse.add_argument("file", help="Path to .mvm file")
    p_parse.add_argument("-o", "--output", help="Output file path (default: stdout)")

    p_validate = sub.add_parser("validate", help="Validate .mvm file format")
    p_validate.add_argument("file", help="Path to .mvm file")

    p_show = sub.add_parser("show", help="Show parsed data object")
    p_show.add_argument("file", help="Path to .mvm file")

    p_render = sub.add_parser("render", help="Render .mvm file to specific format")
    p_render.add_argument("file", help="Path to .mvm file")
    p_render.add_argument(
        "-r", "--renderer",
        choices=list(RENDERERS.keys()),
        default="web",
        help="Renderer to use (default: web)",
    )
    p_render.add_argument("-o", "--output", help="Output file path (default: stdout)")
    p_render.add_argument("--dark", action="store_true", help="Dark mode (interactive renderer only)")
    p_render.add_argument("--plugin-dir", help="Additional plugin directory to load")

    args = p.parse_args()

    if args.command == "parse":
        cmd_parse(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "show":
        cmd_show(args)
    elif args.command == "render":
        cmd_render(args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
