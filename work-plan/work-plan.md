# MVM 文件格式工程计划

## 阶段一：核心解析器 ✅ 已完成

### 目标
实现 .mvm 文件的基本解析能力，能读取 MODEL 和 MSG 区并输出结构化数据。

### 任务清单

- [x] **1.1 分块器（Blocker）**
  - 读取 .mvm 文件内容
  - 按 `===MODEL===` 和 `===MSG===` 分割为两个文本块
  - 处理空白行和注释
  - 错误处理：缺少区块、重复区块、顺序错误

- [x] **1.2 模型解析器（ModelParser）**
  - 解析 `@type TypeName` 类型定义
  - 解析 `@version x.y` 版本信息
  - 解析字段定义：`field: type`
  - 支持基础类型：string, text, int, float, bool, datetime, url
  - 支持复合类型：array\<T\>, map\<K,V\>, enum(a|b|c)
  - 支持可选字段：`type?`
  - 支持嵌套类型引用
  - 输出 Schema 对象

- [x] **1.3 内容解析器（MsgParser）**
  - 按 Schema 验证 MSG 区内容
  - 解析简单值：`field: value`
  - 解析多行文本：`body: |`
  - 解析数组：`[a, b, c]`
  - 解析嵌套对象：`## typeRef`
  - 类型校验与错误报告
  - 输出 DataObject

- [x] **1.4 CLI 工具**
  - `mvm parse example.mvm` 输出 JSON
  - `mvm validate example.mvm` 验证文件格式
  - `mvm show example.mvm` 显示解析结果

### 交付物
- [x] 解析器核心代码（Python）
- [x] CLI 工具（mvm_cli.py）
- [x] 示例 .mvm 文件（examples/article.mvm）

---

## 阶段二：基础 View 渲染器 ✅ 已完成

### 目标
实现基础 View 渲染器，验证"同一内容，多种呈现"的核心价值。

### 任务清单

- [x] **2.1 Web 渲染器（WebRenderer）**
  - 将解析结果渲染为 HTML
  - 支持基础排版：标题、段落、列表、引用、代码块
  - 输出完整 HTML 文件（含内联 CSS）
  - 支持 format 枚举：paragraph/quote/code/list/tip/warning

- [x] **2.2 Markdown 渲染器（MdRenderer）**
  - 将解析结果反向输出为 Markdown
  - 验证 .mvm → .md 的转换
  - 作为基准对照

- [x] **2.3 幻灯片渲染器（SlideRenderer）**
  - 将 sections 自动分页为幻灯片
  - 输出 Reveal.js 兼容的 HTML
  - 支持双栏布局、代码块暗色主题

- [x] **2.4 CLI 集成**
  - `mvm render example.mvm -r web -o output.html`
  - `mvm render example.mvm -r md -o output.md`
  - `mvm render example.mvm -r slide -o output-slides.html`

### 交付物
- [x] Web 渲染器（mvm_parser/renderers/web_renderer.py）
- [x] Markdown 渲染器（mvm_parser/renderers/md_renderer.py）
- [x] 幻灯片渲染器（mvm_parser/renderers/slide_renderer.py）
- [x] 渲染输出示例（output/ 目录）

---

## 阶段三：交互式 Web 渲染器（Interactive WebRenderer）⬅ 当前阶段

### 目标
实现"伪前端"交互能力——.mvm 文件本身不写任何 JavaScript，所有交互由 View 渲染器在渲染时注入。

### 核心原则

> **交互逻辑属于 View 层，不属于 Model/Msg 层。**
> .mvm 文件永远不需要写任何 JavaScript。
> 交互行为完全由渲染器根据 format 枚举和内容结构自动推断并注入。

### 架构设计

```
.mvm 文件（Model + Msg）
  format: tab / accordion / quiz / timeline / flashcard / ...
         ↓
InteractiveWebRenderer（View）
  读取 format 枚举 → 选择对应的交互组件模板
  注入 HTML 结构 + CSS 样式 + JavaScript 行为
         ↓
用户看到的完整交互页面
```

### 任务清单

- [ ] **3.1 交互式 Web 渲染器（InteractiveWebRenderer）**
  - 继承/扩展 WebRenderer
  - 根据 section.format 枚举注入对应交互组件
  - 所有 JS 行为内联，零外部依赖（不依赖 React/Vue）
  - 输出单个完整 HTML 文件

- [ ] **3.2 交互组件库**

  | 组件 | format 枚举 | 交互行为 | Model/Msg 需要什么 |
  |------|------------|----------|-------------------|
  | Tab 标签页 | `tab` | 点击切换内容面板 | 多个 section + tab_group 字段 |
  | 手风琴折叠 | `accordion` | 点击展开/收起 | 多个 section + accordion_group 字段 |
  | 闪卡翻转 | `flashcard` | 点击翻转查看背面 | heading=正面, body=背面 |
  | 测验问答 | `quiz` | 选择答案 → 显示对错 | items=选项, body=题目 |
  | 时间线 | `timeline` | 滚动时逐步揭示 | 多个 section 按顺序排列 |
  | 进度追踪 | `progress` | 滚动时更新阅读进度 | 纯 View 层，自动计算 |
  | 搜索过滤 | `search` | 实时搜索 sections | 纯 View 层，自动生成索引 |
  | 暗色模式 | - | 切换亮色/暗色主题 | 纯 View 层，默认开启 |
  | 全屏演示 | - | 全屏幻灯片模式 | 纯 View 层，按钮触发 |
  | 代码运行 | `code` | 一键复制 / 在线运行 | body=代码, source=语言标识 |
  | 目录导航 | - | 侧边栏目录 + 滚动高亮 | 自动从 sections 生成 |
  | 渐进式揭示 | `reveal` | 点击/滚动逐步显示内容 | 多个 section + reveal_group 字段 |

- [ ] **3.3 扩展 MODEL 类型系统**
  - 新增交互相关字段类型（不影响现有类型）
  - `tab_group: string?` — 标签页分组标识
  - `accordion_group: string?` — 手风琴分组标识
  - `reveal_group: string?` — 渐进揭示分组标识
  - `correct_answer: int?` — 测验正确答案索引
  - `front: text?` — 闪卡正面内容
  - `back: text?` — 闪卡背面内容

- [ ] **3.4 交互式示例文件**
  - 创建包含多种交互组件的 .mvm 示例
  - 验证同一文件渲染为：交互网页 / 静态网页 / 幻灯片 / Markdown
  - 证明交互是 View 层能力，不影响内容复用

- [ ] **3.5 CLI 集成**
  - `mvm render example.mvm -r interactive -o output.html`
  - `mvm render example.mvm -r interactive --dark -o output.html`（暗色模式）

### 交付物
- InteractiveWebRenderer 代码
- 交互组件库（纯 HTML/CSS/JS，零依赖）
- 交互式示例 .mvm 文件
- 渲染效果演示

---

## 阶段四：扩展 View 渲染器

### 目标
实现更多呈现方式，展示 MVM 的"无限视图"能力。

### 任务清单

- [ ] **4.1 PPT 渲染器（PptxRenderer）**
  - 输出 .pptx 文件
  - 自动分页和排版
  - 支持主题模板

- [ ] **4.2 语音渲染器（VoiceRenderer）**
  - 调用 TTS API 朗读内容
  - 输出音频文件（mp3/wav）
  - 支持语速、音色调节

- [ ] **4.3 动态渲染器（StreamRenderer）**
  - 打字机效果输出
  - 流式逐句显示
  - 适合网页嵌入

- [ ] **4.4 PDF 渲染器（PdfRenderer）**
  - 高质量排版输出
  - 支持自定义样式

- [ ] **4.5 卡片渲染器（CardRenderer）**
  - 每个 section 一张知识卡片
  - 适合移动端/小程序

### 交付物
- 各渲染器代码
- 渲染效果示例

---

## 阶段五：工具链与生态

### 目标
完善开发工具和编辑体验，降低使用门槛。

### 任务清单

- [ ] **5.1 编辑器支持**
  - VS Code 语法高亮（.mvm 文件）
  - 语法校验（实时错误提示）
  - 代码片段（snippets）
  - 预览面板（侧边栏实时渲染，支持交互预览）

- [ ] **5.2 模板库**
  - 文章模板（Article）
  - 演示模板（Presentation）
  - 交互式教程模板（InteractiveTutorial）
  - 测验模板（Quiz）
  - 技术文档模板（TechDoc）
  - 用户自定义模板

- [ ] **5.3 转换工具**
  - Markdown → .mvm 转换器
  - .mvm → JSON 转换器
  - PPT → .mvm 逆向提取（实验性）

### 交付物
- VS Code 扩展
- 模板库
- 转换工具

---

## 阶段六：验证与发布

### 目标
用真实场景验证 MVM 格式的实用价值，准备公开发布。

### 任务清单

- [ ] **6.1 真实场景测试**
  - 技术博客：.mvm → 交互网页 + 静态网页 + PDF + 幻灯片
  - 交互教程：.mvm → 带测验/闪卡的网页
  - 会议分享：.mvm → PPT + 语音 + 讲稿
  - 知识笔记：.mvm → 交互网页 + 卡片 + 搜索

- [ ] **6.2 性能优化**
  - 大文件解析性能
  - 交互渲染性能
  - 内存占用优化

- [ ] **6.3 文档与发布**
  - 官方文档站（用 .mvm 自身构建）
  - PyPI 包发布
  - GitHub 仓库
  - 交互式示例展示站

### 交付物
- 性能测试报告
- 官方文档
- 开源仓库
- 示例展示

---

## 技术选型

| 模块 | 选定方案 | 备注 |
|------|---------|------|
| 核心语言 | Python | 已确定，阶段一完成 |
| Web 渲染 | 原生 HTML/CSS/JS（零框架依赖） | 交互组件同样零依赖 |
| PPT 生成 | python-pptx | 阶段四 |
| TTS | Edge TTS | 阶段四 |
| CLI 框架 | argparse | 已确定，阶段一完成 |
| VS Code 扩展 | 原生 API | 阶段五 |

---

## 当前状态

**阶段：三 — 交互式 Web 渲染器**
**已完成：** 阶段一（核心解析器）+ 阶段二（基础渲染器）
**下一步：** 实现 InteractiveWebRenderer，支持 Tab/手风琴/闪卡/测验/时间线等交互组件
