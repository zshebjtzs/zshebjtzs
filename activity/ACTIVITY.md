# 活动档案

仅收录已审核记录。

## 2026-11-24 — [[AI] 阶段 C：升级战略局面评估](https://github.com/zshebjtzs/tree-grow-game/pull/36)

**仓库：** zshebjtzs/tree-grow-game

## 概述

完成阶段 C「战略评估升级」的第一轮完整实现。此 PR 以阶段 B 分支为基线，新增确定性、可解释的局面特征分析与动态评估层，不改变游戏规则，也不替代战术证明。

### 实现内容

1. **战略阶段识别（C1）**
   - 检测扩张、防守、根安全、围攻、多根协同、战术压力和前线控制信号。
   - 各信号可同时成立，不使用互斥的单阶段分类。
2. **动态优先级（C2）**
   - 根据当前局面信号动态调整推进、攻击、扩张、防守、根安全和围攻相关权重。
   - 动态权重只作用于当前评估，不修改共享难度配置。
3. **空间与前线控制（C3）**
   - 计算扩张前沿、争夺空间、前线覆盖和敌方推进压力。
   - 将空间控制变化纳入行动排序与局面评估。
4. **多根协同（C4）**
   - 分别计算各根节点子树覆盖的前沿区域。
   - 以活跃根覆盖率和前沿重叠情况衡量多根协同。
5. **攻防转换（C5）**
   - 独立识别进攻转向与防守转向信号。
   - 根安全与防守压力分别参与权重调整。

### 架构边界

- `PositionAnalyze

> AI 战略局面评估升级，体现策略评估与决策架构演进。

## 2026-11-23 — [建议：扩展为统一的 CCF 信息学竞赛资料归档平台](https://github.com/tangyixiao/CSP-2026/issues/71)

**仓库：** tangyixiao/CSP-2026

提出将单一赛事资料归档项目抽象为统一 CCF 信息学竞赛资料归档平台的架构建议，涵盖通用平台核心、赛事独立数据模块与跨赛事索引。

> 外部仓库的架构设计提案，具有技术讨论价值；Issue 仍开放，作为外部贡献归档，不列为已完成成果。

## 2026-11-22 — [AI 决策架构重构与六档难度升级](https://github.com/zshebjtzs/tree-grow-game/pull/33)

**仓库：** zshebjtzs/tree-grow-game

## 目标

统一 AI 决策与搜索架构，为未来不同游戏模式提供适配器扩展点；增加六档难度，并通过结构性评估提升局面理解。当前仅实现 TreeGrow 适配器，不实现 Quick/Campaign 的玩法规则。

## 已完成

### A0：审计与基线
- 新增 `docs/AI-A0-AUDIT.md`，记录原 AI 架构、风险点和测试缺口。
- 新增可复现的 AI 锦标赛工具 `npm run tournament:ai`，支持红蓝交换配对与配对统计。
- 记录原四档 AI 的 CI 性能基线。

### A1：统一决策架构
- 修复 `PositionKey` 未包含 `hasUsedRootGrowth` 的状态键错误，并增加回归测试。
- 根层搜索不再按静态评分宽度提前排除合法候选。
- 六档难度共用评估权重、战术筛选和搜索算法，难度差异由搜索预算控制。
- 新增 `TreeGrowAIAdapter` 与 `AIAdapterRegistry`，将 TreeGrow 状态、规则、战斗、行动生成、评估、战术和解释逻辑移出通用控制器。
- `SearchEngine` 通过状

> AI 决策架构重构与六档难度升级，体现算法和系统设计。

## 2026-11-22 — [修复 AI 将已生长根节点误判为可生长节点的问题](https://github.com/zshebjtzs/tree-grow-game/pull/32)

**仓库：** zshebjtzs/tree-grow-game

## 问题
AI 偶尔会把已经完成首次生长的根节点再次作为生长父节点，违反“根节点不能分支”的规则。典型场景是：AI 有 R1、R2、R3 三个未被摧毁的根节点，R1 已经生长且首枝仍存活，R2、R3 尚未生长；AI 却可能再次选择 R1，而不是从 R2 或 R3 首次生长。

此外，原逻辑还存在另一种边界缺陷：若根节点的首枝被摧毁，`childrenIds` 变空，旧判断会错误地重新允许该根节点生长。

## 修复
- 为节点增加持久化状态 `hasUsedRootGrowth`，记录根节点是否已经使用过首次生长机会。
- 根节点成功创建第一根枝条时标记；后代被摧毁时不重置。
- AI 候选生成阶段直接排除已使用首次生长机会的根节点，即使其首枝仍然存活也不能再次成为父节点。
- `RuleEngine` 与玩家节点选择入口同步检查该状态，避免不同入口的规则判断不一致。
- `GameState` 序列化、反序列化和克隆保留该状态，并兼容旧存档（旧存档仍有存活子节点时可推断已使用）。

## 回归测试
- 多根节点场景：R1 已生长且首枝仍存活，R2、R3 未生长；AI 候选不得包含 

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-22 — [修复直接攻击非堡垒分叉节点时的整树摧毁结算](https://github.com/zshebjtzs/tree-grow-game/pull/31)

**仓库：** zshebjtzs/tree-grow-game

## 问题说明

直接攻击非堡垒分叉节点时，旧逻辑只删除被攻击节点及其后代，没有继续从其父节点向上回溯。当其父链上不存在其他非根分叉节点时，防守根节点因此错误保留。

## 修复内容

- 统一非堡垒节点的战斗回溯逻辑：始终从被攻击节点的父节点开始寻找最近的非根分叉祖先。
- 被攻击节点自身不再作为保护终点。
- 找到其他非根分叉祖先时，保留并冻结该祖先分叉节点，摧毁目标枝及路径下游。
- 找不到时，回溯至根节点并摧毁整棵防守树，不产生冻结。
- 战斗事件改为依据实际规则结算结果生成解释，避免直接攻击分叉节点时错误显示为局部分支摧毁。
- 更新 GAME-RULES.md 第 6.2、6.3 节。
- 更新和扩展 CombatResolver 回归测试，覆盖直接攻击分叉节点、祖先分叉保护、整树摧毁及战斗事件说明。

## 验收重点

1. 直接攻击分叉节点，父链不存在其他非根分叉节点：根节点及整棵树被摧毁。
2. 直接攻击分叉节点，父链存在其他非根分叉节点：最近祖先分叉节点保留并冻结，其他分支不受影响。
3. 普通叶节点/链节点攻击行为保持原有预期。
4. 堡垒仍不能被直接攻击。
5.

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-21 — [修复回放地图背景与逐步导航动画问题](https://github.com/zshebjtzs/tree-grow-game/pull/29)

**仓库：** zshebjtzs/tree-grow-game

## 修改内容

- 将正式对局地图视口的深色渐变、网格纹理和边缘暗角应用到回放地图区域，并统一画布边框与阴影效果。
- 修复连续点击「下一步」时重复请求同一目标步骤的问题。
- 新增独立的回放导航目标状态：每次新请求立即取代旧目标，取消旧动画，只播放最新目标步骤的动画。
- 上一步、时间线定位、播放/暂停、离开回放等操作会清理或使旧导航任务失效，避免过期异步回调覆盖新位置。
- 增加导航目标状态的边界与连续请求测试。

## 设计约束

- 不重放被跳过步骤的动画。
- 动画只读取已验证棋谱快照，不执行规则逻辑、不触发 AI、不修改权威对局状态。
- 保留现有回放音效生命周期与动画取消机制。
- 不修改存档、棋谱格式或正式对局规则。

## 验收重点

- 回放地图周边背景与正式对局视觉一致。
- 快速连续点击下一步时，最终只播放最后目标步骤的动画。
- 快速反向导航、暂停、播放、时间线拖动和离开回放不会让旧动画或旧请求覆盖新状态。

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-21 — [对局回放音效：同步行动事件与播放控制](https://github.com/zshebjtzs/tree-grow-game/pull/28)

**仓库：** zshebjtzs/tree-grow-game

## 概述

为只读对局回放接入正式对局已有的音效系统，使回放动画与声音按实际行动结算顺序同步。

## 实现内容

- 新增 `ReplayAudioScheduler`，将已验证回放时间线转换为音效调用，不重新执行规则或 AI。
- 复用现有 `AudioController` 的生长、战斗、摧毁、冻结、回合切换和胜利音效。
- 在 `ReplayAnimationController` 中增加行动/动画段级音效生命周期钩子。
- 覆盖普通生长、战斗、连锁摧毁、冻结、根节点摧毁、胜利、跳过回合及冻结型无摧毁战斗。
- 暂停、定位、动画替换和销毁时取消回放音效，避免旧行动声音残留。
- 4× 速度下对过密的同类提示音进行节流；不改变音效音高。
- 在回放工具栏增加音效开关与音量控制，与正式对局共享同一个音频状态。
- 音频解锁失败或浏览器不支持音频时，不影响回放。

## 测试

新增回放音效调度测试，覆盖事件顺序、胜利分支、冻结型战斗、跳过回合、4× 节流、音频解锁期间取消，以及动画控制器生命周期联动。

## 验收重点

1. 生长 → 战斗 → 连锁摧毁 → 冻结 → 回合切换

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-21 — [回放视觉动画 A0–A4：行动复现、时间线交互与回归验证](https://github.com/zshebjtzs/tree-grow-game/pull/27)

**仓库：** zshebjtzs/tree-grow-game

## 开发范围

一次性完成回放视觉动画系统 A0–A4，复用正式对局动画，不重新执行游戏逻辑。

## A0：代码审查

- 正式对局已有 `PresentationController`、`AnimationController` 和 Canvas 动画绘制实现。
- 棋谱前后快照与事件可用于重建生长和战斗动画。
- 补齐回放需要的战斗事件标识，不修改存档 Schema。

## A1–A2：自动播放动画

- 抽取正式对局与回放共用的动画时长定义。
- 新增 `ReplayAnimationTimeline` 与 `ReplayAnimationController`。
- 复用正式对局的生长、战斗和连锁摧毁视觉效果。
- 自动播放等待行动动画完成后再提交回放步骤。
- 支持暂停、中断及 0.5×/1×/2×/4×速度。

## A3：时间线交互

- 拖动进度条时暂停播放并取消正在执行的动画。
- 拖动过程中只绘制目标快照，作为轻量静态预览。
- 松开后，相邻的前进一步播放完整行动动画；跨步骤或向后定位则直接切换快照。
- 行动列表点击和“下一步”复用相邻步骤动画。
- 连续拖

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-21 — [修复回放切换步骤时节点与连线残留](https://github.com/zshebjtzs/tree-grow-game/pull/26)

**仓库：** zshebjtzs/tree-grow-game

## 问题
引入 F5「地图底图只绘制一次、播放时仅更新节点图层」优化后，地图与动态节点仍绘制在同一张 Canvas 上。`renderNodes()` 没有清除上一帧，导致已摧毁节点及其连线在回放切换步骤时残留。

## 修复
- `CanvasDrawer` 使用独立离屏 Canvas 缓存静态地图。
- `renderMap()` 在离屏 Canvas 绘制地图，并合成到可见 Canvas。
- `renderNodes()` 每帧清空可见 Canvas、恢复地图缓存，再绘制当前节点与连线。
- 正式对局、教程和回放统一使用相同的绘制生命周期。

## 测试
- 增加 CanvasDrawer 回归测试，验证每帧先清除旧像素、恢复底图，再绘制当前节点；空节点帧也不会保留上一帧节点。
- 等待 GitHub Actions 执行完整测试与构建。

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-20 — [大型存档与长棋谱性能优化：F0–F5](https://github.com/zshebjtzs/tree-grow-game/pull/23)

**仓库：** zshebjtzs/tree-grow-game

## 目标

一次性完成大型存档与长棋谱性能优化 F0–F5。保留现有 MatchHistory 前后快照结构、悔棋语义和完整校验规则；不重构棋谱存储模型，不设置新的固定文件大小上限。

## F0：性能审查与现有架构优化
- 记录存档/回放数据流与性能热点，新增可复现的 replay 基准脚本。
- 快照链使用结构比较，避免构造大型临时 JSON 字符串。
- 每步只完整验证新的 after 快照；before 仍与上一步 after 做完整结构比较。
- 复用已验证的历史对象，减少整份棋谱重复深拷贝。

## F1：取消硬限制
- 移除回放导入 20 MiB 文件大小拒绝，不增加替代性的固定文件大小上限。
- 保留地图、节点、行动链、回合顺序、路径连通性和末端快照等验证。

## F2：存档压缩
- 新存档采用紧凑 JSON；支持时使用 gzip，只有压缩后确实更小时才使用压缩格式。
- 新格式带 TGSV 版本标识，兼容旧版纯 JSON .sav / .json 存档。
- 正式读档和回放导入共用解码器。

## F3：Worker 后台导入
- 使用 ES Module Web

> 大型存档与长棋谱性能优化，体现性能分析和工程优化。

## 2026-11-17 — [R0–R4：完成独立对局回放系统](https://github.com/zshebjtzs/tree-grow-game/pull/22)

**仓库：** zshebjtzs/tree-grow-game

## 本次范围：R0–R4

完成独立对局回放系统的架构、存档校验、工作区、控制系统与自动化验收。

### R0：回放基础架构
- `ReplaySession`：第 0 步为历史起点，第 N 步为第 N 个行动后的快照；快照深拷贝，回放状态独立。
- `ReplayController`：任意跳转、首末步、前后步、播放/暂停、0.5×/1×/2×/4×；手动跳转会中断自动播放。
- `AppState` 增加独立 `replay` screen。

### R1：存档与棋谱校验
- 新增 `ReplaySaveValidator`：重建独立地图，验证地图种子、基地、节点坐标/区域、快照结构、行动数据、行动前后链路和棋谱末端与存档当前状态的一致性。
- 增加行动方与行动前回合一致性、行动后回合切换、新节点编号、根节点路径端点及地图连通路径校验。
- 对旧存档缺失棋谱的情况，只生成“保存时局面”这一帧并明确标记历史不完整，不伪造此前行动。
- 校验失败时不替换现有回放会话。

### R2：独立只读回放工作区
- 主菜单新增独立“对局回放”入口，与新游戏、读取存档分开。
- 支持导入 

> 独立对局回放系统，属于重要的系统架构与功能交付。

## 2026-11-17 — [人机对战：基地选址与玩家先后手选择](https://github.com/zshebjtzs/tree-grow-game/pull/21)

**仓库：** zshebjtzs/tree-grow-game

## 本次修改

### 1. 双方基地均由玩家选择
- 人机与双人模式统一采用固定顺序：先选择红方基地，再选择蓝方基地。
- 移除 AI 自动随机选择蓝方基地及距离筛选逻辑。
- 蓝方基地选择阶段支持自动保存与恢复。

### 2. 人机对战增加玩家先后手选择
- 主菜单对局配置增加“玩家先后手”选项。
- 玩家可选择红方先手或蓝方后手。
- 阵营配置贯穿 AI 初始化、Worker 请求、回合调度、行动验证、UI 提示、结算展示、存档和再来一局。
- 双人模式保持原有红方先手行为。

### 3. 测试
- 扩展 AppState 与 RematchConfig 对蓝方玩家配置的验证。
- 新增 AI 阵营映射单元测试。

请重点验收红方玩家（AI 蓝方）和蓝方玩家（AI 红方）两种开局及后续回合切换。

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-15 — [chore(release): prepare v1.2.0](https://github.com/zshebjtzs/tree-grow-game/pull/20)

**仓库：** zshebjtzs/tree-grow-game

## Release preparation for v1.2.0

- Synchronize `package.json` version to `1.2.0`.
- Add the Chinese release notes at `.github/releases/v1.2.0.md`.
- Update the tag-triggered offline release workflow to publish those notes automatically.

## Validation

- CI and Windows Desktop Build must pass on the latest PR head before merge.
- The `v1.2.0` tag will be created only after this PR is merged and final release assets are verified.

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-15 — [修复连锁摧毁未能摧毁 AI 根节点的问题](https://github.com/zshebjtzs/tree-grow-game/pull/18)

**仓库：** zshebjtzs/tree-grow-game

## 问题
玩家攻击触发连锁摧毁时，如果回溯链到达 AI 根节点，根节点可能被当作普通分叉保护点而保留，导致 AI 树残留。

## 修复
- 连锁摧毁寻找保护性分叉点时排除根节点。
- 普通非根分叉节点仍按原规则保留并冻结。
- 攻击链抵达根节点时，将根节点及其所有子枝一并纳入摧毁集合。

## 回归测试
- 新增根节点具有多个子枝时，攻击链抵达根节点应摧毁整棵树的测试。
- 验证根节点被删除后，不能再作为生长父节点。
- 原有普通分叉保留、冻结与整树摧毁测试继续覆盖。

## CI
最新提交的 `npm test` 已通过；生产构建与 Pages 产物验证正在运行。

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-15 — [chore: migrate project licensing to GPL and CC BY-NC-SA](https://github.com/zshebjtzs/tree-grow-game/pull/19)

**仓库：** zshebjtzs/tree-grow-game

## Summary
- License project source code under GNU GPL-3.0-or-later.
- License original project documentation and game-design text under CC BY-NC-SA 4.0.
- Add contribution guidance and third-party license notices.
- Keep third-party components under their original licenses.
- Include license and notice files in Windows offline and desktop release packages.
- Remove the old MIT notice from the current root license while clarifying that previously published MIT permissions are not revoked.

## Sc

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-15 — [修复 Pages 环境下教程 AI Worker 加载失败](https://github.com/zshebjtzs/tree-grow-game/pull/17)

**仓库：** zshebjtzs/tree-grow-game

## 问题
Pages 生产环境中，教程回合切换后蓝方 AI Worker 无法启动，导致教程对局无法继续。

## 修复
- 将浏览器默认 Worker 创建改为 Vite 可静态分析的 `new Worker(new URL(...), { type: 'module' })` 形式。
- 保留测试环境注入 Worker 构造器的能力。
- 增加 Worker 生产入口路径与运行时错误诊断测试，并增强请求异常恢复。

## 验证
- GitHub Actions `npm test`、AI 决策基准、Production Build、Pages 构建产物验证全部通过。

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-15 — [完善新手教程实战流程与 AI 对战体验](https://github.com/zshebjtzs/tree-grow-game/pull/16)

**仓库：** zshebjtzs/tree-grow-game

## 改动内容
- 将教程入口名称调整为「新手教程」。
- 增加教学目标校验与合法偏离后的反馈处理。
- 为实战、战斗和攻击章节接入蓝方 AI 自动回应，支持连续多轮交替。
- 完善对局结束反馈、重试当前章节及章节切换时的 AI 请求清理。
- 增加教程 AI 控制器与流程测试，并更新教程架构文档。

## 验证
- 自动化测试通过。
- AI 决策耗时基准通过。
- Production Build 与 Pages 构建产物验证通过。

目标分支：main

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-15 — [feat: add complete interactive tutorial experience](https://github.com/zshebjtzs/tree-grow-game/pull/15)

**仓库：** zshebjtzs/tree-grow-game

## Summary

- Add an isolated tutorial runtime built on deterministic, validated scenarios.
- Route player, AI, and tutorial growth through the shared authoritative growth action service.
- Add a dedicated interactive tutorial entry and responsive learning workspace, separate from normal match UI and persistence.
- Teach board topology, node selection, legal growth, turn order, root first-growth rules, ordinary combat and freeze resolution, enemy-base invasion, branching, fortresses, and a final

> 完整交互式新手教程，体现教学流程与游戏规则系统的整合。

## 2026-11-14 — [feat(ai): implement F0-F3 AI architecture and search upgrades](https://github.com/zshebjtzs/tree-grow-game/pull/14)

**仓库：** zshebjtzs/tree-grow-game

## Summary

Completes Stage F0 baseline, F1 tactical evaluation, F2 fixed difficulty profiles, and the first F3 search-engine increment.

## F0 — Architecture and performance baseline
- Document the AI decision pipeline, implementation boundaries, performance hotspots, and target architecture.
- Add `npm run benchmark:ai` with repeatable p50/p95/mean/max measurements.
- Run the benchmark in CI as an observational baseline.
- Remove the artificial 300ms Worker response delay.

## F1 — Tactical an

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-14 — [feat: complete match lifecycle with statistics, results and rematch](https://github.com/zshebjtzs/tree-grow-game/pull/12)

**仓库：** zshebjtzs/tree-grow-game

## Scope
Stage E1 + E2 + E3 are implemented together on this development branch. No merge has been performed.

## Stage E1 — Match data
- Add match-scoped tracking for player statistics, structural peaks, combat outcomes, and the full event journal.
- Capture immutable result snapshots with winner/reason, elapsed duration, per-side metrics, and event history.
- Integrate tracking with growth, combat, freeze, root destruction, victory, and skipped turns.
- Persist tracker state in manual saves an

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-14 — [fix: prevent start button event from being treated as rematch config](https://github.com/zshebjtzs/tree-grow-game/pull/13)

**仓库：** zshebjtzs/tree-grow-game

## 问题
点击“创建对局”时，`addEventListener('click', beginNewMatch)` 会把浏览器的 `MouseEvent` 作为第一个参数传入 `beginNewMatch(configOverride)`。该事件对象被误当作重赛配置，导致 `createRematchConfig()` 抛出 `Cannot rematch from an invalid match configuration`，新局初始化中断。

## 修复
将监听器改为 `() => beginNewMatch()`，避免将 DOM 事件对象传入配置参数。Rematch 按钮仍显式传入上一局配置，不受影响。

## 验证
等待 PR CI（测试、构建、Pages 验证）完成后再合并。

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-14 — [fix: reject attacks against fortress nodes](https://github.com/zshebjtzs/tree-grow-game/pull/11)

**仓库：** zshebjtzs/tree-grow-game

## Summary
- Reject growth into an enemy fortress area in RuleEngine before a node is created.
- Keep the current turn and game state unchanged when a fortress target is rejected; the existing HUD feedback and legal-area preview consume the same RuleEngine result.
- Add defensive guards so CombatResolver and CombatEvent cannot process fortress targets.
- Revalidate simulated AI moves and ensure all difficulty levels treat a fortress-only target as no legal move.
- Update GAME-RULES.md to describ

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-14 — [feat: complete Stage D in-game presentation](https://github.com/zshebjtzs/tree-grow-game/pull/10)

**仓库：** zshebjtzs/tree-grow-game

## Summary

Completes Stage D (D1–D3) as one presentation-layer upgrade.

### D1 — Presentation foundation
- Add reusable animation and presentation controllers.
- Animate node growth and provide selection, hover, and turn feedback.
- Replace common disruptive alerts with in-game feedback.

### D2 — Combat presentation
- Animate combat targets and affected branches before applying the resolved state.
- Explain combat outcomes using immutable snapshots derived from `CombatResolver` results.
- Kee

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-12 — [feat: Stage C map viewport navigation and visual stage](https://github.com/zshebjtzs/tree-grow-game/pull/8)

**仓库：** zshebjtzs/tree-grow-game

## Stage C · C1 + C2

### C1 — Map viewport
- Add locked/unlocked navigation modes; unlocked mode ignores map gameplay input and blocks game-state toolbar actions.
- Add pointer-captured drag navigation with click suppression after a drag.
- Add bounded pan offsets, centered zoom transforms, and a reset-to-default action.
- Keep map rendering and logical coordinates unchanged; centralize screen-to-world coordinate mapping.

### C2 — Map presentation
- Replace the stark white unused canvas-contai

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-12 — [test: Stage C gameplay regression and Pages release verification](https://github.com/zshebjtzs/tree-grow-game/pull/9)

**仓库：** zshebjtzs/tree-grow-game

## Stage C · C3 + C4

### C3 — Regression coverage
- Expand CanvasDrawer tests for bounded panning, reset-to-default, screen-to-logical coordinate mapping, locked/unlocked mode, and viewport resize behavior.
- Expand AI regression coverage across easy/medium/hard to ensure returned moves are accepted by RuleEngine.
- Cover no-legal-move handling and combat simulation freeze/turn-transition semantics.

### C4 — GitHub Pages build verification
- Add `npm run verify:pages` to validate the productio

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-12 — [feat: Stage B gameplay UX and responsive map layout](https://github.com/zshebjtzs/tree-grow-game/pull/7)

**仓库：** zshebjtzs/tree-grow-game

## 阶段二：对局体验与页面适配

### 本次改动
- 将游戏界面改为视口约束的纵向布局，为地图分配可收缩的剩余空间。
- 新增 `calculateCanvasFit`，按 Canvas 容器实际宽高计算 3:2 地图显示尺寸；保留 1800×1200 逻辑坐标、地图种子和存档格式。
- 使用 `ResizeObserver` 监听地图容器变化；点击坐标继续通过 Canvas bounding rect 映射，避免缩放后命中位置偏移。
- 默认完整显示地图，并新增 50%–200% 地图缩放、滚动查看和一键适应窗口。
- 重构对局 HUD：模式/难度、双方节点数量、回合状态和节点图例。
- 新增暂停/继续、重新开始、返回主菜单控制；暂停时锁定地图点击与跳过回合，AI 思考或战斗动画期间阻止危险的状态切换。
- Canvas 节点绘制增加分叉/堡垒结构标识；保留原有合法区域高亮、冻结状态与战斗动画。
- 新增视口尺寸和缩放测试，并保留既有 Canvas 绘制回归测试。

### 验证
- CI 执行 `npm test` 与 `npm run build`。
- 静态 DOM ID 

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-12 — [feat: redesign main menu and match startup flow](https://github.com/zshebjtzs/tree-grow-game/pull/6)

**仓库：** zshebjtzs/tree-grow-game

## Summary
- Replace the always-visible setup toolbar with a dedicated main menu and match setup screen.
- Add a separate application screen state and immutable match configuration snapshot.
- Preserve the existing PVP/PVE base-selection and gameplay logic.
- Add local recent-match persistence and a Continue Game entry, while retaining .sav file import/export.
- Add focused unit tests for application navigation and match configuration.
- Restore an AI turn automatically when continuing a PVE sav

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-12 — [feat: highlight legal growth destinations](https://github.com/zshebjtzs/tree-grow-game/pull/5)

**仓库：** zshebjtzs/tree-grow-game

## Summary
- Add a RuleEngine preview API that derives legal destination areas by reusing `canGrow()`.
- Highlight every legal destination polygon with a translucent teal overlay while preserving red/blue base tinting.
- Synchronize previews with node selection, turn ownership, animation state, AI turns, new games, and loaded saves.
- Allow direct clicks on enemy nodes when their occupied area is a highlighted legal attack target.

## Validation
- `npm test` — passed
- `npm run build` — passed



> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-11 — [feat: add Windows offline desktop release](https://github.com/zshebjtzs/tree-grow-game/pull/4)

**仓库：** zshebjtzs/tree-grow-game

## Summary
- Add a portable native Windows desktop host using Win32 and WebView2.
- Preserve the existing Vite frontend, Canvas rendering, and module AI Web Worker.
- Add per-monitor DPI awareness and package the application as a portable ZIP.
- Add CI compilation, packaging, and WebView2/AI Worker smoke tests.
- Update the Windows offline distribution section in README with both browser and desktop download/startup methods.

## Validation
- Windows Desktop Build has already passed on the featur

> Windows 离线桌面发行，体现桌面封装、构建与分发工程。

## 2026-11-08 — [fix: bundle AI worker for GitHub Pages](https://github.com/zshebjtzs/tree-grow-game/pull/3)

**仓库：** zshebjtzs/tree-grow-game

## Summary
- Fix the AI Worker entry path so Vite bundles the Worker and its module dependencies for GitHub Pages.
- Rewrite `README.md` in Simplified Chinese, covering the game's concept, core gameplay, implementation architecture, technology stack, development, deployment, and project structure.
- Add `GAME-RULES.md` at the repository root with the complete setup, turn, growth, combat, fortress, branch destruction, freeze, AI, save/load, and victory rules.
- Link the detailed rules document fr

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-08 — [feat: complete Tree Grow Game v1.0](https://github.com/zshebjtzs/tree-grow-game/pull/1)

**仓库：** zshebjtzs/tree-grow-game

## Summary
- Complete the core Tree Grow Game gameplay, topology, combat, save/load, rendering, and AI implementation.
- Add regression tests and GitHub Actions CI.
- Add GitHub Pages deployment and Windows offline release workflows.
- Preserve match mode and AI difficulty in save files.

## Validation
- GitHub Actions CI passed on the latest head commit.
- Local gameplay verification completed by the maintainer.
- Windows offline launch and Pages deployment remain post-merge release checks.

> TreeGrow v1.0 核心版本交付，代表独立项目从开发到可运行产品的完整落地。

## 2026-11-08 — [fix: enable GitHub Pages during deployment](https://github.com/zshebjtzs/tree-grow-game/pull/2)

**仓库：** zshebjtzs/tree-grow-game

## Summary
- Enable GitHub Pages automatically from the Pages deployment workflow when the site has not yet been enabled.
- Keep the existing build, test, artifact upload, and deployment sequence unchanged.

## Validation
- The failing run confirmed `npm install`, all 28 tests, and `npm run build` pass.
- The failure was `actions/configure-pages@v5` returning `Not Found` because no Pages site was enabled/configured.
- This change sets `enablement: true`; the workflow run after merge will verify 

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-07 — [docs: add Simplified Chinese README](https://github.com/zshebjtzs/my-agent-skills/pull/7)

**仓库：** zshebjtzs/my-agent-skills

## Summary

- Add `README.zh-CN.md` as a complete Simplified Chinese translation of the root README.
- Preserve the existing English `README.md` as the repository's default landing page.
- Add reciprocal language-switch links between the English and Simplified Chinese README files.
- Keep code examples, commands, file paths, identifiers, and technical literals intact.

## Context

This is a documentation follow-up to the already merged #6. It adds the Chinese-language counterpart without replaci

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-07 — [docs: comprehensively upgrade root README](https://github.com/zshebjtzs/my-agent-skills/pull/6)

**仓库：** zshebjtzs/my-agent-skills

## Summary

- Replace the outdated root README with a complete project guide aligned with the current implementation.
- Document the bilingual VitePress portal, collections, repository layout, Skill discovery and download behavior.
- Explain local Skill submission through JSON fields or ZIP upload, including the actual validation limits.
- Explain external Skill registration, build-time source resolution, review workflow, and manual publication process.
- Document validation/security boundaries,

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-07 — [feat: support ZIP Skill submissions with maintainer review](https://github.com/zshebjtzs/my-agent-skills/pull/5)

**仓库：** zshebjtzs/my-agent-skills

## Summary
- Add a ZIP upload field to the local Skill Issue form while preserving the JSON text submission path.
- Validate uploaded ZIP attachments with bounded download and decompression, safe paths, symlink/special-file rejection, duplicate-path checks, UTF-8 text-only validation, and required SKILL.md structure.
- Create one review PR containing the complete Skill directory; include README and SKILL.md preview links, file tree, file count, and size summary.
- Keep external Skill submission 

> ZIP Skill 提交与维护者审核流程，体现文件处理和安全校验设计。

## 2026-11-07 — [feat: automate local Skill submissions via Issues](https://github.com/zshebjtzs/my-agent-skills/pull/4)

**仓库：** zshebjtzs/my-agent-skills

## Summary
- Add a dedicated **Add a local Skill** Issue Form.
- Accept required `SKILL.md`, optional `README.md`, and optional additional text files through a JSON path-to-content map.
- Extend the existing Issue workflow to create a Skill directory and open a PR automatically.
- Validate category, paths, duplicate directories, file count, and total text size.
- Update README instructions for the new submission flow.

## Workflow
1. Submit a local Skill Issue.
2. GitHub Actions creates `skills/

> 基于 Issue 的 Skill 提交流程自动化，体现 GitHub 工作流设计。

## 2026-11-07 — [feat: add Simplified Chinese and English portal](https://github.com/zshebjtzs/my-agent-skills/pull/3)

**仓库：** zshebjtzs/my-agent-skills

## Summary
- Add VitePress locale configuration for Simplified Chinese and English, including a built-in language switcher.
- Localize navigation, category labels, sidebar, footer, homepage hero, category landing pages, and Skill detail actions.
- Generate English routes for the homepage, all Skill categories, and each discovered Skill while preserving original Skill documentation content.
- Keep per-Skill ZIP downloads pointed at the shared downloads directory.

## Validation
- GitHub Pages wor

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。

## 2026-11-07 — [feat: add VitePress Skill portal and GitHub Pages deployment](https://github.com/zshebjtzs/my-agent-skills/pull/2)

**仓库：** zshebjtzs/my-agent-skills

## Summary

Build a static Skill catalog directly into the existing repository.

### Included
- VitePress-based GitHub Pages site with Personal / Community / Shared categories.
- Automatic discovery of local Skills through `SKILL.md`, with README-first online previews.
- ZIP download containing only the selected Skill directory.
- External Skill manifest and GitHub Issue → Actions → PR submission flow.
- Pages build/deployment workflow, local search, and documentation.

### Compatibility
- Prese

> VitePress 技能门户与 GitHub Pages 部署，体现工具平台化交付。

## 2026-11-01 — [Add GitHub Spec Kit as a community submodule](https://github.com/zshebjtzs/my-agent-skills/pull/1)

**仓库：** zshebjtzs/my-agent-skills

## Summary
- Add `github/spec-kit` under `community/spec-kit` as a Git submodule.
- Pin the submodule to upstream commit `7370e592f3cd9c06e5b698983957e227c75b30e2`.
- Add `.gitmodules` with the upstream repository URL.

## Usage
Clone with `git clone --recurse-submodules https://github.com/zshebjtzs/my-agent-skills.git` to fetch the submodule contents. For an existing clone, run `git submodule update --init --recursive`.

To update the pinned upstream revision later, run `git submodule update --

> 已完成的常规功能、缺陷修复、测试、文档或维护变更；保留在完整活动档案，不占主页精选位。
