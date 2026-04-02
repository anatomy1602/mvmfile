MVM：一种面向内容呈现的文件架构模式 —— 写一次，渲染无限

> GitHub: https://github.com/anatomy1602/mvmfile
> 纯 Python 实现，零前端框架依赖，.mvm 文件本身不包含任何 JavaScript

MVM = Model - View - Msg**，把内容的「结构定义」「文字信息」「呈现方式」彻底分离。

一份 `.mvm` 文件，自动渲染成网页、PPT 幻灯片、Markdown 文档——内容本身不需要任何修改。

## MVM 的核心思想

### 三要素分离

```
┌─────────────────────────────────────────────────┐
│                   .mvm 文件                       │
│                                                   │
│  ===MODEL===          ===MSG===                   │
│  ┌───────────┐       ┌───────────┐               │
│  │ 结构定义   │       │ 文字信息   │               │
│  │ 类型系统   │  +    │ 纯内容     │               │
│  │ 字段约束   │       │ 无样式     │               │
│  └───────────┘       └───────────┘               │
│         │                   │                     │
│         └───────┬───────────┘                     │
│                 ▼                                  │
│         ┌───────────┐                             │
│         │    View    │  ← 外部渲染器               │
│         │  呈现方式   │                             │
│         └───────────┘                             │
└─────────────────────────────────────────────────┘
```

| 要素 | 职责 | 类比 |
|------|------|------|
| **Model** | 定义内容有哪些字段、什么类型 | 数据库 Schema / TypeScript interface |
| **Msg** | 填充实际的文字和数据 | JSON 数据 / 数据库记录 |
| **View** | 决定怎么呈现（网页/PPT/MD/语音） | React 组件 / LaTeX 样式文件 |

**关键原则：Model 不可变，Msg 纯信息，View 只消费不修改。**

### 本质：内容层与应用层的分离

我把所有软件界面分成两层：

| 层级 | 特征 | 代表 |
|------|------|------|
| **内容层** | 纯展示，无状态，无逻辑 | MD、Mermaid、SVG、PDF、**MVM** |
| **应用层** | 有状态，有行为，可运行 | Vue、React、Angular |

判断标准很简单：**有没有"可变化的状态"和"可触发的行为"？**

- Vue/React 有 `data`、`computed`、`watch`、`emit` → **应用层**
- Mermaid 画完就定了，不会自己变 → **内容层**
- MVM 的 Model 不可变，Msg 纯信息 → **内容层**

MVM 不是要和 Vue/React 竞争，而是填补一个被忽视的空白：**内容层的独立标准**。

---

## .mvm 文件长什么样？

一个完整的例子：

```mvm
===MODEL===
@type InteractiveDemo
@version 2.0
@plugins tab, accordion, timeline, flashcard, quiz, reveal
@requires interactive, media

title: string
subtitle: string?
author: string
date: datetime
tags: array<string>
sections: array<Section>

@type Section
heading: string
body: text?
format: enum(paragraph|quote|code|list|tip|warning|tab|accordion|timeline|flashcard|quiz|reveal|scene)?
image: url?
audio: url?
video: url?
background: url?
children: array<Section>?

===MSG===
title: MVM 交互式渲染演示
subtitle: 同一内容，无限交互
author: Alice
date: 2026-03-31T12:00:00Z
tags: [MVM, 交互, 渲染器, 前端]

sections:
  ## heading: 什么是 MVM
  format: paragraph
  image: https://picsum.photos/800/300
  body: |
    MVM = Model - View - Msg
    一种面向内容呈现的文件架构模式。

  ## heading: 前端框架对比
  format: tab
    ## heading: React
      body: Meta 开发的 UI 库，采用虚拟 DOM 和 JSX 语法。
    ## heading: Vue
      body: 渐进式 JavaScript 框架，以易学易用著称。
    ## heading: Svelte
      body: 编译型框架，没有虚拟 DOM。

  ## heading: 知识测验
  format: quiz
    ## heading: MVM 的三个要素是什么？
      items:
        - Model, View, Controller
        - Model, View, Msg
        - Model, Vue, MongoDB
      correct_answer: 1
      body: MVM = Model - View - Msg。
```

### 语法要点

- `===MODEL===` 和 `===MSG===` 分割两个区域
- MODEL 区定义类型（`@type`）、字段类型（`string`/`text`/`int`/`enum`/`array`/`url`）、可选标记（`?`）
- MSG 区用 `##` 引用类型创建嵌套对象，缩进表示父子关系
- `@plugins` 声明需要的组件插件，`@requires` 声明需要的渲染能力
- `|` 表示多行文本块
- 编辑体验接近 Markdown，但结构是精确的、机器可解析的

---

## v0.2 做了什么？

### 树结构嵌套

v0.1 的 sections 是扁平列表，v0.2 支持嵌套 children：

```mvm
## heading: 前端框架对比
format: tab          ← 父节点：Tab 容器
  ## heading: React  ← 子节点：第一个 Tab
    body: ...
  ## heading: Vue    ← 子节点：第二个 Tab
    body: ...
```

这意味着你可以把 quiz 放进 tab 里，把 accordion 放进 timeline 里，做任意嵌套布局。

### 素材引用

支持图片、音频、视频、背景图的引用：

```mvm
## heading: 异世界的入口
format: scene
background: ./assets/forest.jpg
image: ./assets/alice.png
audio: ./assets/bgm.mp3
body: 爱丽丝站在森林入口。
```

### 插件系统

6 个交互组件从渲染器中提取为独立插件：

```
mvm_parser/plugins/builtin/
├── tab.py          # Tab 切换
├── accordion.py    # 手风琴折叠
├── timeline.py     # 时间线
├── flashcard.py    # 翻转闪卡
├── quiz.py         # 选择题测验
└── reveal.py       # 渐进式揭示
```

每个插件自包含 HTML 渲染 + CSS 样式 + JS 交互，渲染器只负责调度。

第三方扩展只需写一个 Python 文件：

```python
from mvm_parser.plugins.base import ComponentPlugin

class MyChartPlugin(ComponentPlugin):
    name = "chart"

    def render(self, section, children):
        return f'<div class="chart">{...}</div>'

    def get_css(self):
        return ".chart { ... }"

    def get_js(self):
        return "function initChart() { ... }"
```

### 能力声明

渲染器声明自己支持的能力，.mvm 文件声明自己需要的能力：

```python
class InteractiveWebRenderer(BaseRenderer):
    capabilities = ["interactive", "media", "tree", "dark_mode", "search", "toc"]

class MdRenderer(BaseRenderer):
    capabilities = ["tree"]
```

```mvm
@requires interactive, media
```

用不支持的渲染器渲染时会给出警告，而不是静默失败。

---

## 渲染效果

同一份 `.mvm` 文件，四种渲染输出：

### 1. 交互式网页（InteractiveWebRenderer）

![interactive](https://picsum.photos/800/450)

- 左侧目录导航 + 搜索
- Tab 切换、手风琴折叠、时间线、闪卡翻转、选择题测验、渐进式揭示
- 暗色模式切换
- 响应式布局
- **所有交互由渲染器注入，.mvm 文件零 JavaScript**

### 2. 网页（WebRenderer）

简洁的 HTML + CSS 页面，适合静态文档展示。

### 3. Markdown（MdRenderer）

反向输出为 Markdown 格式，树结构渲染为嵌套列表。

### 4. 幻灯片（SlideRenderer）

基于 Reveal.js 的幻灯片，每个 section 一页，支持嵌套内容的垂直幻灯片。

---

## 技术架构

```
mvmfile-design/
├── mvm_parser/               # 核心解析库
│   ├── blocker.py            # 区块分割器（MODEL / MSG）
│   ├── model_parser.py       # 模型解析器（类型定义 → Schema）
│   ├── msg_parser.py         # 内容解析器（文本 → DataObject）
│   ├── schema.py             # Schema 数据结构
│   ├── data_object.py        # DataObject 数据结构
│   ├── parser.py             # 统一解析入口
│   ├── plugins/              # 插件系统
│   │   ├── base.py           # ComponentPlugin 抽象基类
│   │   ├── loader.py         # 插件加载器（目录扫描 + 动态导入）
│   │   └── builtin/          # 内置组件插件
│   │       ├── tab.py
│   │       ├── accordion.py
│   │       ├── timeline.py
│   │       ├── flashcard.py
│   │       ├── quiz.py
│   │       └── reveal.py
│   └── renderers/            # 渲染器
│       ├── __init__.py       # BaseRenderer（能力声明基类）
│       ├── web_renderer.py   # HTML 网页
│       ├── md_renderer.py    # Markdown
│       ├── slide_renderer.py # Reveal.js 幻灯片
│       └── interactive_renderer.py  # 交互式网页
├── mvm_cli.py                # CLI 工具
└── examples/                 # 示例文件
    ├── interactive-demo.mvm  # 完整交互演示
    └── tree-demo.mvm         # 树结构演示
```

### 解析流程

```
.mvm 文件
    ↓
Blocker（分块器）
    ↓ 分离 ===MODEL=== 和 ===MSG===
    ↓
ModelParser（模型解析器）
    ↓ @type / field: type → Schema 对象
    ↓
MsgParser（内容解析器）
    ↓ 按 Schema 验证 + 缩进嵌套解析 → DataObject
    ↓
{ schema, data }
    ↓
ViewRenderer（视图渲染器）
    ↓ 接收 schema + data，检查 @requires 能力匹配
    ↓ 加载 @plugins 声明的插件
    ↓ 递归渲染树结构
    ↓
HTML / Markdown / 幻灯片 / ...
```

### CLI 使用

```bash
# 解析为 JSON
python mvm_cli.py parse examples/interactive-demo.mvm

# 验证格式
python mvm_cli.py validate examples/interactive-demo.mvm

# 渲染为交互式网页
python mvm_cli.py render examples/interactive-demo.mvm -r interactive -o output.html

# 渲染为 Markdown
python mvm_cli.py render examples/interactive-demo.mvm -r md -o output.md

# 渲染为幻灯片
python mvm_cli.py render examples/interactive-demo.mvm -r slide -o slides.html

# 加载自定义插件
python mvm_cli.py render demo.mvm -r interactive --plugin-dir ./my-plugins/

# 暗色模式
python mvm_cli.py render demo.mvm -r interactive --dark -o dark.html
```

---

## 和现有方案的对比

### vs PPT

| | PPT | MVM |
|---|---|---|
| 内容与样式 | 混在一起 | 完全分离 |
| 换风格 | 逐页修改或重新套模板 | 换渲染器 |
| 多格式输出 | 仅 PPT / PDF | 网页 + PPT + MD + 语音... |
| 版本管理 | 二进制，无法 diff | 纯文本，Git 友好 |

### vs Markdown

| | Markdown | MVM |
|---|---|---|
| 结构定义 | 隐式（`#` `**` 符号） | 显式（类型系统 + Schema） |
| 类型系统 | 无 | string/text/int/enum/array/url |
| 多视图 | 主要是文本类 | 任意（网页/动画/语音/3D） |
| 交互组件 | 无 | Tab/测验/闪卡/时间线... |

### vs LaTeX

| | LaTeX | MVM |
|---|---|---|
| 学习曲线 | 极陡 | 平缓（类 Markdown） |
| 渲染目标 | 主要 PDF | 任意 |
| 扩展方式 | 宏包 | View 渲染器 + 插件 |

### vs Vue/React

| | Vue/React | MVM |
|---|---|---|
| 定位 | 应用层 | 内容层 |
| 状态管理 | 有 | 无（Model 不可变） |
| 事件交互 | 有 | 无（纯展示） |
| 关系 | 可作为 MVM 的 View 渲染器 | 可输出给 Vue/React 消费 |


## 适用场景

1. **技术文档**：写一次，自动生成网页版 + PDF 版 + 幻灯片版
2. **教学课件**：交互式测验、闪卡、渐进式揭示，内容与交互分离
3. **AI 生成内容**：AI 输出结构化 Model+Msg，View 渲染器负责呈现
4. **多平台分发**：同一份内容适配公众号、知乎、掘金、PPT
5. **知识管理**：纯文本 + Git 版本管理 + 精确结构化


## 项目状态

- **版本**：v0.2
- **语言**：Python（零外部依赖）
- **渲染**：纯 HTML/CSS/JS（零前端框架依赖）
- **协议**：MIT

### v0.2 完成清单

- [x] 树结构嵌套（children 递归解析 + 递归渲染）
- [x] 素材引用（图片/音频/视频/背景）
- [x] 插件系统（ComponentPlugin 基类 + 动态加载 + 6 个内置插件）
- [x] @plugins / @requires 声明解析
- [x] 能力声明系统（渲染器 capabilities + 降级策略）
- [x] 4 个渲染器（Web / MD / Slide / Interactive）
- [x] CLI 工具（parse / validate / show / render）

## 最后

MVM 的核心信念：

> **内容本身永远不变，呈现方式是无限的外衣。**

`.mvm` 文件 = 结构化的骨架（Model）+ 自然语言的血肉（Msg），呈现方式（View）由渲染器决定。

欢迎来 GitHub 看代码、提 Issue、写插件。

**https://github.com/anatomy1602/mvmfile**
