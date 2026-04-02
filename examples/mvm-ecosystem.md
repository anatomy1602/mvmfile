# MVM 核心生态

> 让存档变成内容

**MVM Team** | 2026-04-01T12:00:00Z

`MVM` `生态` `游戏存档` `AI`

---

## 核心定位

> MVM 不是"更好的 Markdown"，也不是"通用内容协议"。
> MVM 是"可分享的游戏/AI 过程协议"。
>
> — ChatGPT 分析
>
> https://chatgpt.com/s/t_69cc95a0277481919e49d360c06a1ceb
>

## 核心洞察

> 没有人把这三件事打通：可读 + 可渲染 + 可交换。
> MVM 要做的是：统一"可读 + 可渲染 + 可交换"的内容中间层。
>
> — ChatGPT 分析
>
> https://chatgpt.com/s/t_69cc95a0277481919e49d360c06a1ceb
>

## 为什么现在有机会？

1. AI 爆发：生成内容多，需要展示
2. 游戏 UGC 爆发：玩家想分享过程，但缺格式
3. 多端消费：Web / 视频 / 移动，内容需要多形态
4. 这三点叠加：正好需要一个"内容中间层"


## MVM 的独特优势

*与现有方案对比*

特性 | Markdown | Notion | Ink | MVM
--- | --- | --- | --- | ---
可读性 | 优 | 优 | 优 | 优
游戏语义 | 差 | 差 | 优 | 优
跨系统 | 优 | 差 | 差 | 优
可渲染 | 中 | 优 | 优 | 优
可交换 | 优 | 差 | 差 | 优


## 生态分层

<details>
<summary>Layer 1: 运行时层</summary>

- SillyTavern 前端
- AI 模型（GPT-4/Claude/Gemini）
- 扩展（LWB/变量插件等）

</details>

<details>
<summary>Layer 2: 数据层</summary>

- 角色卡 PNG
- 聊天记录 JSONL
- 扩展数据

</details>

<details>
<summary>Layer 3: 内容层 ← MVM 在这里</summary>

- 用户想分享的内容
- MVM 格式（Model + Msg）
- 语义化结构（chapters/scenes）

</details>

<details>
<summary>Layer 4: 呈现层</summary>

- NovelRenderer（小说）
- VisualRenderer（视觉小说）
- TimelineRenderer（时间线）
- CharacterRenderer（角色卡）

</details>

<details>
<summary>Layer 5: 分享层</summary>

- 论坛帖子
- Git 仓库
- 压缩文件

</details>


## 工作流程


## 核心原则

### 语义优先

MVM 不按"维度"设计，按"语义"设计。

| ❌ 维度设计 | ✅ 语义设计 |
|-----------|-----------|
| 一维：列表 | list |
| 二维：表格 | table |
| 三维：时间线 | timeline |

### 人机双友好

- 人可以直接阅读 .mvm 文件
- 程序可以精确解析
- AI 可以理解和生成

### 内容与呈现分离

同一个 MVM 文件可以渲染为：
- 小说
- 视觉小说
- 时间线
- 网页

### 不绑定任何平台

- 不依赖 SillyTavern
- 不依赖特定 AI 模型
- 不依赖特定前端


## 实现路线

<details>
<summary>Phase 1: Killer Demo（决定生死）</summary>

目标：用一个真实案例证明 MVM 的价值。

| 任务 | 优先级 | 说明 |
|------|--------|------|
| 选择真实游戏存档 | 高 | SillyTavern / 视觉小说 / 模拟经营 |
| 手动转换成 MVM | 高 | 展示"存档 → 内容"的过程 |
| 多种方式渲染 | 高 | Novel / Visual / Timeline |
| 分享测试 | 中 | 让别人能点开就看 |

</details>

<details>
<summary>Phase 2: 生态工具</summary>

目标：降低使用门槛。

| 任务 | 优先级 | 说明 |
|------|--------|------|
| SillyTavern 导出插件 | 高 | 一键导出 MVM |
| AI 辅助生成 | 高 | 用户描述意图，AI 生成 MVM |
| 在线渲染器 | 中 | 无需安装，直接查看 |

</details>

<details>
<summary>Phase 3: 社区生态</summary>

目标：建立内容市场。

| 任务 | 优先级 | 说明 |
|------|--------|------|
| 多平台转换器 | 中 | TavernAI / Oobabooga 等 |
| 内容市场 | 中 | 分享 MVM 文件的平台 |
| 社区插件 | 低 | 新的渲染器、新的转换器 |

</details>


## 风险与挑战

- 可能做成"没人用的优雅协议"
- 生态难启动
- 容易过度设计
- 如果只做协议，不落地
- 如果成功：游戏 → 内容、AI → 内容、数据 → 内容
- 如果失败：一个很优雅的 YAML 语法 😄


## 关键建议

```python
# 不要先做协议

# 先做这个：

# 1. 一个 Demo：把某个游戏存档 → MVM → 可视化页面
# 2. 找一个具体场景：
#    - AI 跑团记录
#    - 视觉小说存档
#    - 模拟经营游戏记录
# 3. 做"分享体验"：让别人能点开就看、可交互、可传播

# Killer Demo 比继续设计协议重要 10 倍
```


## 核心使命

> MVM 的使命是：定义"内容的中间语言"，
> 让游戏 → 内容、AI → 内容、数据 → 内容。
>
> — MVM Team
>
> https://github.com/anatomy1602/mvmfile
>

## 总结

这份文档展示了 MVM 的核心生态：

1. **核心定位**：让存档变成内容
2. **独特优势**：可读 + 可渲染 + 可交换
3. **生态分层**：运行时 → 数据 → 内容 → 呈现 → 分享
4. **工作流程**：用户侧 + 接收者侧
5. **实现路线**：Killer Demo → 生态工具 → 社区生态

**关键路径**：
1. 先做 Killer Demo（决定生死）
2. 再做生态工具（降低门槛）
3. 最后做社区生态（扩大影响）

**如果成功**：
MVM 会成为游戏/AI 内容的通用格式
存档不再是"运行时数据"，而是"可分享的内容"

**如果失败**：
会变成一个很优雅的 YAML 语法

**所以，Killer Demo 比继续设计协议重要 10 倍。**

