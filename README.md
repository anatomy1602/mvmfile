# mvmfile

> MVM = Model - View - Msg，一种面向内容呈现的文件架构模式。

## 最简介绍

**MVM** 是一种将内容的「结构定义」「文字信息」「呈现方式」彻底分离的文件格式：

- **Model**：结构定义，类型规则，定义"内容长什么样"
- **Msg**：文字信息，实际内容，纯信息不含样式
- **View**：呈现方式，渲染结果，由渲染器决定

**核心价值**：写一次，渲染无限——同一份 `.mvm` 文件可以自动渲染成网页、PPT 幻灯片、Markdown 文档、交互式页面等多种格式。

## 快速开始

### 1. 安装依赖

```bash
# 克隆仓库
git clone https://github.com/anatomy1602/mvmfile.git
cd mvmfile

# 环境要求：Python 3.6+
# 无外部依赖，纯 Python 实现
```

### 2. 渲染示例文件

```bash
# 渲染为交互式网页
python mvm_cli.py render examples/mvm-ecosystem.mvm --output output.html --renderer interactive

# 渲染为 Markdown
python mvm_cli.py render examples/mvm-ecosystem.mvm --output output.md --renderer md

# 渲染为幻灯片
python mvm_cli.py render examples/mvm-ecosystem.mvm --output output-slide.html --renderer slide

# 渲染为网页
python mvm_cli.py render examples/mvm-ecosystem.mvm --output output-web.html --renderer web
```

### 3. 启动 HTTP 服务器

```bash
# 启动渲染服务器（端口 9000）
python mvm_server.py --port 9000

# 访问：http://localhost:9000
```

## 核心功能

- **多渲染器**：Web、Markdown、Slide、Interactive
- **插件系统**：手风琴、标签页、时间线、闪卡、测验、揭示、表格、列表、引用、代码块
- **结构化**：类型系统、字段约束、嵌套结构
- **人机双友好**：编辑体验接近 Markdown，程序可以精确解析
- **版本管理友好**：纯文本格式，Git diff 清晰可见
- **零依赖**：纯 Python 解析，纯 HTML/CSS 渲染

## 项目结构

```
mvmfile/
├── examples/            # 示例 .mvm 文件
├── mvm_parser/          # 核心解析器
│   ├── plugins/         # 组件插件
│   └── renderers/       # 渲染器
├── mvm_cli.py           # 命令行工具
├── mvm_server.py        # HTTP 服务器
└── work-plan/           # 设计文档和工作计划
```

## 更多信息

- **架构设计**：[mvm-architecture.md](work-plan/mvm-architecture.md)
- **v0.2 计划**：[v0.2-plan.md](work-plan/v0.2-plan.md)
- **v0.3 计划**：[v0.3-plan.md](work-plan/v0.3-plan.md)
- **Interactive 演示模式**：[interactive-presentation-mode.md](work-plan/interactive-presentation-mode.md)
- **工作安排**：[work-plan.md](work-plan/work-plan.md)

## 如何贡献

1. Fork 仓库
2. 创建分支
3. 提交更改
4. 发起 Pull Request

## 协议

MIT
