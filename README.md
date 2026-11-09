# MarketPilot AI

MarketPilot AI 是一个基于 Python 和 Streamlit 的中文 AI 营销策划 Web 应用，用于蓝色光标校园招聘 AI 应用测评。输入品牌信息后，可生成营销策略、A/B 广告文案和 30 天内容日历，并导出 Markdown 报告和 CSV 表格。

## 功能

- 品牌信息输入：品牌、产品、优势、受众、地区、目标、预算和主要平台；提供“羽毛球拍面向美国大学生”预设案例。
- 营销策略：品牌定位、用户画像、核心卖点、推荐渠道、预算建议、30 天行动计划、KPI 与评估方法。
- 广告文案：小红书、抖音、Instagram、TikTok、LinkedIn 五个平台，各生成 A/B 两版。
- 内容日历：连续 30 天的日期、平台、主题、内容方向和目标；支持 CSV 下载。
- 结果导出：Markdown 营销策略报告和 CSV 日历。
- 演示模式：无 API Key 时展示明确标注的本地预设建议，不调用 AI。AI 请求失败时直接显示错误，不会自动切换成演示结果。

报告中的建议和假设应由使用者结合真实产品资料与投放数据核实；应用不会自动生成市场规模、竞品价格或真实投放效果。

## 技术栈与结构

- Python 3.11+、Streamlit、OpenAI Python SDK
- `app.py`：Streamlit 主入口和页面交互
- `marketpilot/core.py`：输入校验和演示内容
- `marketpilot/ai.py`：DeepSeek / OpenAI 兼容接口调用与响应校验
- `marketpilot/export.py`：Markdown 和 CSV 导出
- `tests/`：基础测试
- `examples_backup/`：原仓库的 Chatbot 和各示例页面、原测试，供参考；不会作为新应用侧边栏页面
- `requirements-original.txt`：原始应用依赖清单

## Windows PowerShell 本地运行

在仓库根目录执行：

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

如已有可用 `.venv`，可跳过创建虚拟环境。启动后打开命令行显示的本地地址。点击左侧“载入羽毛球拍预设案例”，即可在演示模式下体验全部生成按钮。

要启用 DeepSeek 真实 AI，请在本机的 `.streamlit/secrets.toml` 中填写 `DEEPSEEK_API_KEY`，或设置同名环境变量。这个文件已由 `.gitignore` 排除。应用使用 DeepSeek 官方兼容接口 `https://api.deepseek.com` 和 `deepseek-flash` 模型。原有 OpenAI 接入仍可通过 `OPENAI_API_KEY` 使用；两个密钥都存在时优先使用 DeepSeek。请勿把密钥写入源码、README、测试或提交记录。本项目不会要求在网页表单中输入密钥。

运行基础测试：

```powershell
.\.venv\Scripts\python.exe -m pip install pytest
.\.venv\Scripts\python.exe -m pytest tests -q
```

## 部署到 Streamlit Community Cloud

将仓库部署为 Streamlit 应用时，主文件选择 `app.py`，依赖使用根目录的 `requirements.txt`，Python 选择受支持的 3.11 或更高版本。若需真实 AI，在 Cloud 的应用 Secrets 中配置 `DEEPSEEK_API_KEY`（或 `OPENAI_API_KEY`）；未配置时应用以演示模式运行。部署前请确认所用模型账户、权限和费用设置。原示例保留在 `examples_backup/`，不会显示在新应用侧边栏。

## 开源来源与修改说明

本仓库由 [streamlit/llm-examples](https://github.com/streamlit/llm-examples) Fork 而来。原项目的 `LICENSE`（Apache License 2.0）原样保留，原 `Chatbot.py`、`pages/` 示例和 `app_test.py` 移至 `examples_backup/`，原 `requirements.txt` 备份为 `requirements-original.txt`。MarketPilot AI 的页面、生成逻辑、导出功能和测试是在此基础上新增的。原示例可能需要 `requirements-original.txt` 中的额外依赖，且不是当前应用的运行范围。
