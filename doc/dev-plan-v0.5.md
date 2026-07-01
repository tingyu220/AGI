# Project Yu — 后续开发计划

> 版本：V0.5 | 日期：2026-07-01 | 状态：概念验证完成，进入工程化开发

---

## 1. 当前阶段评估

### 1.1 已完成

| 模块 | 文件 | 完成度 | 说明 |
|------|------|--------|------|
| 实体 / 关系 | `entity.py` `relation.py` | 100% | 纯数据类，功能简单 |
| 知识图谱 | `knowledge_graph.py` | 70% | 支持实体增查 + 关系增查，仅正向查询、内存存储 |
| 语言学习器 | `language_learner.py` | 40% | 支持 3 种句式（是/颜色是/可以），存在关键词顺序冲突 Bug |
| 推理引擎 | `reasoning_engine.py` | 30% | 仅单跳字符串匹配，无真正的多步推理 |
| 记忆管理 | `memory_manager.py` `memory.py` | 50% | 支持记录+查看，无分类/遗忘/持久化 |
| 自我模型 | `self_model.py` | 30% | 仅支持计数，无能力边界感知 |

### 1.2 未完成

- **多步推理**（README Milestone-4）— 完全未实现
- **数据持久化** — KnowledgeGraph 和 Memory 均全内存
- **测试体系** — `tests/` 为空
- **Crow5 标准目录** — 原项目已补齐，但需在 README 中记录
- **版本管控** — Git 无提交记录
- **Perception / Goals / Action 模块** — 仅有设计文档

### 1.3 已知缺陷

| ID | 缺陷 | 严重度 | 文件 |
|----|------|--------|------|
| BUG-01 | `是` 关键词贪婪匹配，`水果是可以食用的` 被误拆 | 🔴 高 | `language_learner.py:21` |
| BUG-02 | 推理引擎仅做字符串匹配，无图遍历 | 🔴 高 | `reasoning_engine.py:31-64` |
| BUG-03 | 无持久化，重启即失忆 | 🔴 高 | `knowledge_graph.py` `memory_manager.py` |
| BUG-04 | `query()` 只返回 `results[0]`，丢失多结果 | 🟡 中 | `reasoning_engine.py:37` |
| BUG-05 | `add_relation` 无去重，重复关系无限增长 | 🟡 中 | `knowledge_graph.py:18` |
| BUG-06 | 版本号混乱：README V0.1 vs main.py V0.5 | ⚪ 低 | `README.md` `main.py` |

---

## 2. 开发阶段与里程碑

```
M1 (基础补齐) → M2 (持久化) → M3 (语言修复) → M4 (多步推理) → M5 (架构升级)
|____ 1.5h ____|____ 2.5h ____|____ 2.0h ____|____ 1.5h ____|____ 2.0h ____|
```

### M1：工程基础补齐

**目标**：让项目从"原型脚本"变成"可迭代的工程项目"

| # | 任务 | 预估工时 | 交付物 |
|---|------|----------|--------|
| M1.1 | 验证 Crow5 标准目录完整性 | 5 min | `doc/` `prototype/` `project/frontend/` `project/backend/` `database/` `utils/` |
| M1.2 | 统一版本号为 V0.5.0 | 5 min | README 与 main.py 一致 |
| M1.3 | 首次 Git 提交 | 5 min | `.gitignore` + `git init` + 首次 commit |
| M1.4 | 编写核心模块单元测试 | 1 h | `tests/test_knowledge_graph.py` `test_language_learner.py` `test_reasoning_engine.py` `test_memory_manager.py` `test_self_model.py` |

**验收**：
```bash
pytest tests/ -v           # 全部通过
git log --oneline           # 至少有 1 条提交
python -c "import main"     # 输出显示 V0.5.0
```

---

### M2：SQLite 持久化存储

**目标**：实现重启后数据不丢失，对齐 README Milestone-2

| # | 任务 | 预估工时 | 交付物 |
|---|------|----------|--------|
| M2.1 | 设计 SQLite Schema + DB 工具类 | 45 min | `database/schema.sql` `utils/db.py` |
| M2.2 | KnowledgeGraph 接入 SQLite | 45 min | 启动从 DB 加载，写入实时落盘 |
| M2.3 | MemoryManager 接入 SQLite | 30 min | memories 表持久化 |
| M2.4 | 持久化集成测试 | 10 min | `tests/test_persistence.py` |

**验收**：
```bash
python -c "
from brain.knowledge_graph import KnowledgeGraph
kg = KnowledgeGraph(db_path='data/brain.db')
kg.add_relation('猫', '是', '动物')
import sys; sys.exit(0)
"
python -c "
from brain.knowledge_graph import KnowledgeGraph
kg = KnowledgeGraph(db_path='data/brain.db')
r = kg.query('猫', '是')
assert len(r) >= 1 and r[0].obj == '动物', '持久化失败'
print('PASS')
"
```

---

### M3：语言学习器修复与增强

**目标**：修复关键词顺序冲突，扩展句式覆盖

| # | 任务 | 预估工时 | 交付物 |
|---|------|----------|--------|
| M3.1 | 修复 `是` 关键词贪婪匹配 | 30 min | 先匹配多词模式，再匹配单词模式 |
| M3.2 | 支持否定句（不是/不能） | 20 min | 正确识别并存储否定关系 |
| M3.3 | 支持复合句拆分 | 40 min | `苹果是红色水果` → 颜色=红色 + 是=水果 |
| M3.4 | 扩展新句式（有/属于/能） | 30 min | 新增 3 种常见中文句式 |

**验收**：
```bash
# "水果是可以食用的" → 水果 --可以--> 食用  ✓
# "水果不是人" → 正确识别否定  ✓
# "苹果是红色水果" → 双关系拆分  ✓
pytest tests/test_language_learner.py -v
```

---

### M4：多步推理引擎

**目标**：实现 README Milestone-4「苹果能吃吗 → 能，因为苹果是水果，水果可以食用」

| # | 任务 | 预估工时 | 交付物 |
|---|------|----------|--------|
| M4.1 | 实现 BFS 传递推理链路 | 45 min | `reasoning_engine.py` 中 `transitive_reason()` |
| M4.2 | 多结果返回 | 20 min | 不再只取 `results[0]`，返回全部匹配 |
| M4.3 | 反向查询支持 | 25 min | `什么是红色水果` → `苹果` |

**验收**：
```python
# 输入：苹果是水果 + 水果可以吃
# 问：苹果能吃吗
# 答：能，因为 苹果 是 水果，水果 可以 食用
python -c "
from brain.knowledge_graph import KnowledgeGraph
from brain.reasoning_engine import ReasoningEngine
kg = KnowledgeGraph(db_path='data/brain.db')
kg.add_relation('苹果', '是', '水果')
kg.add_relation('水果', '可以', '食用')
re = ReasoningEngine()
result = re.answer('苹果能吃吗', kg)
assert '可' in result, f'FAIL: {result}'
print('PASS')
"
```

---

### M5：架构升级（后续可选）

| # | 任务 | 预估工时 | 说明 |
|---|------|----------|------|
| M5.1 | 引入 NetworkX 替代自定义图 | 45 min | 对齐 README 技术栈，支持图算法 |
| M5.2 | 短期/长期记忆分离 | 30 min | 容量限制 + 分类存储 |
| M5.3 | Perception 模块独立化 | 30 min | 从 LanguageLearner 中拆分感知层 |
| M5.4 | Goals / Action 模块骨架 | 15 min | 接口定义 + 基础实现 |

---

## 3. 工时汇总

| 里程碑 | 任务数 | 预估总工时 |
|--------|--------|------------|
| M1 工程基础 | 4 | 1.5 h |
| M2 持久化 | 4 | 2.5 h |
| M3 语言修复 | 4 | 2.0 h |
| M4 多步推理 | 3 | 1.5 h |
| M5 架构升级 | 4 | 2.0 h |
| **合计** | **19** | **9.5 h** |

---

## 4. 风险矩阵

| 风险 | 等级 | 缓解措施 |
|------|------|----------|
| 重构破坏现有功能 | 高 | M1 先补测试锁定当前行为 |
| SQLite Schema 设计不当 | 中 | 预留扩展字段（时间戳、权重、置信度） |
| 推理引擎复杂度膨胀 | 中 | 用 BFS 而非规则堆砌，统一推理策略 |
| 多步推理性能下降 | 低 | 当前数据量小，后续可加索引优化 |

---

## 5. 建议执行顺序

```
第 1 步：M1 工程基础（1.5h）
  └── 原因：为后续所有改动提供测试安全网 + 版本追溯

第 2 步：M2 SQLite 持久化（2.5h）
  └── 原因：解决重启失忆问题，后续推理增强依赖数据完整性

第 3 步：M3 语言学习修复（2.0h）
  └── 原因：解析质量直接影响知识图谱质量

第 4 步：M4 多步推理（1.5h）
  └── 原因：对齐 README Milestone-4，核心能力达标

第 5 步：M5 架构升级（2.0h）
  └── 原因：技术栈对齐 README，但不阻塞核心功能
```

---

## 6. 下一步行动

**建议立即执行 M1**：测试框架搭建 + 版本统一 + Git 初始化。
这是后续所有工作的安全网，风险最低、依赖最少。

**是否按此计划开始执行？**
