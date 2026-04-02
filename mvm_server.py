"""
MVM HTTP Server - HTTP 服务器，用于动态渲染 MVM 文件
"""

import http.server
import socketserver
import urllib.parse
import json
import os
import sys
from pathlib import Path

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

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")


class MVMRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self.serve_index()
        elif path == "/api/render":
            self.serve_render(query)
        elif path == "/api/list":
            self.serve_list()
        elif path.startswith("/static/"):
            self.serve_static(path[8:])
        else:
            self.send_error(404, "Not Found")

    def serve_index(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MVM 渲染服务器</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .header h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .header p {
            color: #666;
        }
        .controls {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .control-group {
            margin-bottom: 15px;
        }
        .control-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #333;
        }
        select, button {
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
        }
        select {
            width: 100%;
            max-width: 400px;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            font-weight: 600;
            transition: background 0.3s;
        }
        button:hover {
            background: #5568d3;
        }
        .preview {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            min-height: 400px;
        }
        .preview iframe {
            width: 100%;
            height: 600px;
            border: none;
            border-radius: 8px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎨 MVM 渲染服务器</h1>
            <p>动态渲染 MVM 文件到多种格式</p>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <label for="file-select">选择文件：</label>
                <select id="file-select">
                    <option value="">-- 请选择 --</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="renderer-select">渲染器：</label>
                <select id="renderer-select">
                    <option value="web">Web Renderer</option>
                    <option value="md">Markdown Renderer</option>
                    <option value="slide">Slide Renderer</option>
                    <option value="interactive">Interactive Renderer</option>
                </select>
            </div>
            
            <button onclick="render()">渲染</button>
        </div>
        
        <div class="preview">
            <div id="loading" class="loading">
                请选择文件和渲染器，然后点击"渲染"按钮
            </div>
            <iframe id="preview" style="display: none;"></iframe>
        </div>
    </div>
    
    <script>
        async function loadFiles() {
            const response = await fetch('/api/list');
            const files = await response.json();
            const select = document.getElementById('file-select');
            files.forEach(file => {
                const option = document.createElement('option');
                option.value = file;
                option.textContent = file;
                select.appendChild(option);
            });
        }
        
        async function render() {
            const file = document.getElementById('file-select').value;
            const renderer = document.getElementById('renderer-select').value;
            
            if (!file) {
                alert('请选择文件');
                return;
            }
            
            const loading = document.getElementById('loading');
            const preview = document.getElementById('preview');
            
            loading.style.display = 'block';
            preview.style.display = 'none';
            loading.textContent = '正在渲染...';
            
            try {
                const response = await fetch(`/api/render?file=${encodeURIComponent(file)}&renderer=${renderer}`);
                const html = await response.text();
                
                const blob = new Blob([html], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                preview.src = url;
                
                loading.style.display = 'none';
                preview.style.display = 'block';
            } catch (error) {
                loading.textContent = '渲染失败：' + error.message;
            }
        }
        
        loadFiles();
    </script>
</body>
</html>"""
        
        self.wfile.write(html.encode("utf-8"))

    def serve_render(self, query):
        file = query.get("file", [""])[0]
        renderer_name = query.get("renderer", ["web"])[0]
        
        if not file:
            self.send_error(400, "Missing file parameter")
            return
        
        file_path = os.path.join(EXAMPLES_DIR, file)
        if not os.path.exists(file_path):
            self.send_error(404, f"File not found: {file}")
            return
        
        try:
            parser = MVMParser()
            result = parser.parse_file(file_path)
            
            if renderer_name not in RENDERERS:
                self.send_error(400, f"Unknown renderer: {renderer_name}")
                return
            
            renderer = RENDERERS[renderer_name]()
            missing = renderer.check_requirements(result.schema.requires)
            if missing:
                print(f"Warning: Renderer '{renderer_name}' does not support: {', '.join(missing)}")
            
            output = renderer.render(result)
            
            self.send_response(200)
            if renderer_name == "md":
                self.send_header("Content-type", "text/markdown; charset=utf-8")
            else:
                self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(output.encode("utf-8"))
            
        except MVMParseError as e:
            self.send_error(500, f"Parse error: {e}")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")

    def serve_list(self):
        files = []
        if os.path.exists(EXAMPLES_DIR):
            for f in os.listdir(EXAMPLES_DIR):
                if f.endswith(".mvm"):
                    files.append(f)
        
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(files, ensure_ascii=False).encode("utf-8"))

    def serve_static(self, path):
        file_path = os.path.join(EXAMPLES_DIR, path)
        if not os.path.exists(file_path):
            self.send_error(404, "Not Found")
            return
        
        self.send_response(200)
        if path.endswith(".css"):
            self.send_header("Content-type", "text/css; charset=utf-8")
        elif path.endswith(".js"):
            self.send_header("Content-type", "application/javascript; charset=utf-8")
        else:
            self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        
        with open(file_path, "rb") as f:
            self.wfile.write(f.read())


def run_server(port=9000):
    import io
    import locale
    import codecs
    
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    with socketserver.TCPServer(("", port), MVMRequestHandler) as httpd:
        print("MVM 渲染服务器启动成功！")
        print(f"访问地址: http://localhost:{port}")
        print(f"示例文件目录: {EXAMPLES_DIR}")
        print("按 Ctrl+C 停止服务器")
        print()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n服务器已停止")
            httpd.shutdown()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="MVM HTTP Server")
    parser.add_argument("--port", type=int, default=9000, help="Port to listen on (default: 9000)")
    args = parser.parse_args()
    
    run_server(args.port)
