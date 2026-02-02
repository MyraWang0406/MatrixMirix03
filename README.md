# 投放实验决策系统 (Decision Support System)

结构可解释、胜率可复用的创意评测系统。支持结构卡片、OFAAT 变体、门禁评测与元素级贡献分析。

## 核心概念

**创意评测的最小单元是「结构组合」，而非视频文件。**

| 字段 | 结构语义 |
|------|----------|
| hook_type | 表达模式 + 认知反差（非文案本身，可统计胜率） |
| why_you_bucket | 核心动机桶（可统计、可复用） |
| why_now_trigger | 行为触发器（时机/紧迫感） |

**门禁 ≠ 结论**

- 样本不足 → 不下结论（仅提示补足数据）
- 门禁失败 → 结构暂不成立（需复测或换层）
- 仅当：跨窗稳定 + OS 不冲突 + 指标达线 → 才允许「结构成立」

## 结构卡片字段

| 字段 | 说明 |
|------|------|
| insight_gap | 用户核心阻力/缺口（用于失败解释） |
| insight_expectation | 用户期望被满足的点 |
| insight_resolution | 素材承诺如何解决 |

上述 insight_* 不参与实验对照，仅用于：失败解释 / 结构复盘 / Prompt 生成。

## 本地运行

```bash
pip install -r requirements.txt
streamlit run app_demo.py
```

本地指定端口：`streamlit run app_demo.py --server.port 3100`

## 云部署：Streamlit Community Cloud（推荐）

1. 将仓库推送到 GitHub
2. 打开 [share.streamlit.io](https://share.streamlit.io)，用 GitHub 登录
3. **New app** → 仓库 `MyraWang0406/AIGC-auto-ads`，分支 `main`
4. **Main file path**：`app_demo.py`（必填，根目录下）
5. 点击 **Deploy**

> **说明**：`app_demo.py` 使用模拟数据，无需配置 Secrets。若部署 `app.py`（LLM 生成），需在 Settings → Secrets 中配置 `OPENROUTER_API_KEY`、`OPENROUTER_MODEL`。

### 健康检查

部署后若页面加载慢，可访问：

- `https://你的app.streamlit.app/?page=health` 或 `?health=1`
- 或点击导航栏 **Health** 按钮

用于排查依赖、环境变量等问题。

## 结构卡片完整示例

```json
{
  "card_id": "sc_casual_game_001",
  "vertical": "casual_game",
  "segment": "18-45岁休闲玩家",
  "motivation_bucket": "成就感",
  "why_you_bucket": "更省事",
  "why_you_phrase": "上手快",
  "why_now_trigger_bucket": "机会出现",
  "why_now_phrase": "新手福利",
  "root_cause_gap": "用户想玩但怕上手难，需要降低门槛与爽点前置",
  "insight_gap": "怕上手难、怕投入时间无回报",
  "insight_expectation": "快速进入爽点、福利即领即用",
  "insight_resolution": "上手快+新手福利登录即送"
}
```

## 判断标准

系统能回答：**「这次没跑出来，是结构不行，还是样本不够？下次该换哪一层？」**

- 结构不行 → 门禁失败 / 跨 OS 冲突 / 某层倾向拖后腿 → 下一步变体建议指出具体字段
- 样本不够 → 决策结论显示「样本不足」，建议补足后再决策该层

## 项目结构

```
├── app_demo.py          # 主入口（Streamlit Community Cloud 部署用）
├── app.py               # LLM 生成入口（需 OPENROUTER_API_KEY）
├── eval_schemas.py      # 结构卡片 + 变体 schema
├── decision_summary.py  # 30 秒决策结论
├── variant_suggestions.py # 下一步变体建议（含因果解释）
├── requirements.txt
├── samples/             # 示例 JSON
├── .streamlit/config.toml
└── ...
```

## 联系

myrawzm0406@163.com
