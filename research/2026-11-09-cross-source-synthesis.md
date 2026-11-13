# 防御性回答 Skill：跨项目与论文整合

检索及读取日期：2026-11-09。目标延续原聊天：删除无关防御内容，包括同义改写；完成授权的编程任务；控制实际 token 成本。研究内容放在本文件和按需参考中，不默认加载进每次请求。

## 实际检索方式

GitHub 仓库检索：`humanizer skill`、`"defensive" "prompt"`、`overrefusal`、`karpathy skills`。读取下列项目的具体文件，而非只依据仓库介绍。搜索结果中的安全防护、模型剪枝和越狱仓库没有被当成对话表达方案。保存来源 URL、提交或快照哈希于 [sources.json](2026-11-09-sources.json)。

## GitHub：选择性借鉴

| 项目及读取文件 | 有用的方法 | 本次取舍 |
| --- | --- | --- |
| [Adkid-Zephyr/anti-defensive-writing-Skill](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill)，中文 SKILL.md | 主张与证据一致，不提前回应未提出的问题，不把局部现象扩成整体否定 | 用于“实际范围内直接陈述”。其中“只突出优势”“不说输”、为了优势重选指标不适合结果汇报；本 Skill 明确保留失败与负面结果。 |
| [blader/humanizer](https://github.com/blader/humanizer)，SKILL.md §1、§5、§9 | 删除虚构反驳；句子整体重写；只保留承载信息的限定 | 扩展至对话、改写、示例。保留真实比较与有意义的不确定性；不引入完整修辞禁词表、标点限制、默认双稿。 |
| [Vumb-VibeCoder/ai-anti-overrefusal-skills](https://github.com/Vumb-VibeCoder/ai-anti-overrefusal-skills)，no-preachy-tone、plain-expert-answers | 直接回答，具体问题具体说明，避免空泛帮助邀请和尾部免责声明堆叠 | 借鉴表达相关性。其领域边界列表、固定字数和固定比例不导入；“一次必要说明”依据当前请求与具体阻碍。 |
| [obra/superpowers](https://github.com/obra/superpowers)，writing-skills、verification-before-completion | 根据失败类型选择规则形态；用可观察的交付与验证判断任务完成 | 采用正向的“交付答案/产物后结束”和独立产物检查。项目里的措辞微测试是该项目经验；没有当成跨模型定律。“每次成功表述都重跑完整命令”的流程不导入。 |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)，CLAUDE.md，原链接 forrestchang 已重定向 | 最小实现、局部修改、遵循现有约定、以明确成功条件驱动执行 | 补充工程约定与只诊断不修改的场景。不导入“任何不清楚都停下询问”。该社区项目借鉴 Karpathy 的观察，不等同于其本人发布或背书。 |
| [Aider-AI/aider](https://github.com/Aider-AI/aider)，editblock_prompts.py | 小而明确的修改块、沿用代码库约定 | 借鉴修改范围和可应用产物。Aider 的 SEARCH/REPLACE 专用格式、让用户把文件加入聊天的权限流程不适用于通用 Codex Skill。 |
| [anthropics/skills](https://github.com/anthropics/skills)，skill-creator/SKILL.md | 冻结旧版、配对评测、记录成本、关注没有区分度的测试 | 冻结上一版 compact-v3，加入新情境和分组指标。不安装该 Skill，不导入 Claude 专用工具或子代理流程。 |

这些项目是方法与失效案例来源，不是本 Skill 的有效性证明。规则用本项目自己的表述重新整合；没有复制第三方实现代码。

## 论文：能支持什么

本轮读取以下论文的 arXiv 标题、作者、版本及摘要；据此借鉴实验设计，没有把摘要阅读称为全文复现，也没有把旧模型结论直接推广至 Sol/Astra。

| 论文 | 原研究的内容 | 对本项目的用途 |
| --- | --- | --- |
| Röttger et al., [XSTest](https://arxiv.org/abs/2308.01263)，NAACL 2024 | 250 个安全请求与 200 个不安全对照，识别夸大的安全行为 | 借鉴正例与必要边界对照分开统计的设计。安全过度拒绝与普通结果汇报的无关免责声明是不同现象；此论文不直接证明本 Skill 的风格效果。 |
| Jiang et al., [FollowBench](https://arxiv.org/abs/2310.20410)，ACL 2024 | 内容、情境、风格、格式、示例五类约束，逐层增加约束 | 同时检查事实、语气、格式和任务完成；不能只看输出变短。 |
| Zhou et al., [Instruction-Following Evaluation / IFEval](https://arxiv.org/abs/2311.07911)，2023 | 用可验证指令减少纯主观评审的不可复现性 | JSON 格式、数值结果、持久化和文件行为用可执行检查；防御性语义仍需读完整内容，不能靠禁词统计代替。 |
| Sharma et al., [Towards Understanding Sycophancy in Language Models](https://arxiv.org/abs/2310.13548)，2023 | 人类偏好可能奖励迎合用户观点而非真实的回答 | 增加明确错误主张与新版变差的对照。减少防御应保留真实反驳、负面结果和不确定性。 |
| Huang et al., [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798)，ICLR 2024 | 在研究的推理任务上，无外部反馈的自纠错可能失败或退化 | 不把额外自检调用默认视为质量保证；采用外部产物检查和离线改进。结论限于其研究条件。 |
| Madaan et al., [Self-Refine](https://arxiv.org/abs/2303.17651)，2023 | 在七类任务上，反复反馈与改写改善旧模型的输出 | 说明迭代是可测试的方案，而非普遍无效。这里采用开发阶段迭代，不在每次 Skill 使用时新增生成—审核—改写调用。 |

两篇自纠错论文研究的任务、方法和评估条件不同，不能合并成“自检一定有效”或“一定无效”。本项目的取舍还依据用户明确要求控制成本。

## 官方文档交叉核对

读取 [OpenAI GPT-6 系列提示词指导](https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md#prompting-best-practices)：该页将提示词作为 GPT-6 家族的起点，要求在所选模型与任务上评测；覆盖主动执行、避免含糊 Skill 规则导致提前停下、不要因假想风险添加未经请求的免责声明，以及按变更选择检查。

未由论文或文档推断当前模型训练原因。只在用户授权的独立 GalaxyData 端点评测 `gpt-6.1-sol`，不读取 Codex 配置；Astra 的共享规则没有本轮运行数据。

## 实际修改与评测约定

- 入口以“从已建立事实交付请求的答案或产物，交付后结束”引导输出形态；整句删除规则继续保留。
- 需要限定的条件具体列为：用户请求风险/上线/核验判断、实际提出了错误主张、或下一步存在具体阻碍。
- 保留实质发现和有用的不确定性，参考文件补充负面结果、翻译保真、真实比较、只做诊断与工程约定。
- 不增加在线模型调用，不安装文本过滤器。仓库中的评测和审核属于开发阶段。
- 加入 14 个跨来源情境，与已有 46 个场景组合，每轮共 60 组新 A/B；A 是冻结的上一版 compact-v3，B 是本轮候选。参数相同，每个场景本轮各采样一次。
- 按完整回答评审无关附加内容；必要纠错、准确性、能力和真实工作区检查分别记录。三轮都使用完整重新采样的 A/B，不拿第一轮 A 与第二轮 B 拼接比较。第二轮起已属于开发回归集。文本审核隐藏版本映射，但审核者仍为本次修改者，不称为独立人工盲评。
- 同时记录输入、输出、总 token、模型调用及耗时。若候选成本增加或完成度变差，不以字符缩短替代验收。

第一版出现防御回退，已拒绝；第二版防御下降但示例事实增补增加，也已拒绝。第三版补充示例只能使用给定事实，不增加检查或完成状态。最终数据见 [research-grounded 报告](../evals/experiments/research-grounded-2026-11-09/REPORT.md)；[首轮失败报告](../evals/experiments/research-transfer-2026-11-09/REPORT.md)和[第二轮报告](../evals/experiments/research-refined-2026-11-09/REPORT.md)完整保留。历史数据保留在各自实验目录，不能借作本轮改善数字。
