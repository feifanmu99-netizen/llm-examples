"""Download formats for generated results."""

import csv
from io import StringIO


def calendar_csv(rows):
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=["日期", "平台", "主题", "内容方向", "目标"], extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return ("\ufeff" + output.getvalue()).encode("utf-8")


def report_markdown(brief, strategy=None, ads=None, calendar=None, mode="演示模式"):
    lines = ["# MarketPilot AI 营销策略报告", "", f"生成方式：{mode}", "", "## 品牌概览", ""]
    for key, label in [("brand", "品牌名称"), ("product", "产品名称"), ("description", "产品描述"),
                       ("advantages", "产品优势"), ("audience", "目标客户"), ("region", "目标地区"),
                       ("goal", "营销目标"), ("budget", "营销预算"), ("platforms", "主要平台")]:
        value = brief[key]
        lines.append(f"- **{label}**：{', '.join(value) if isinstance(value, list) else value}")
    if strategy:
        lines += ["", "## 营销策略", ""]
        for key, label in [("positioning", "品牌定位"), ("persona", "目标用户画像"),
                           ("selling_points", "核心营销卖点"), ("channels", "推荐营销渠道"),
                           ("budget", "预算分配建议"), ("plan", "30天营销行动计划"), ("kpis", "核心KPI及评估方法")]:
            lines += [f"### {label}", ""]
            value = strategy[key]
            lines += [f"- {x}" for x in value] if isinstance(value, list) else [value]
            lines.append("")
    if ads:
        lines += ["## 广告文案", "", f"平台：{ads['platform']}", ""]
        for version in ("A", "B"):
            ad = ads["content"][version]
            lines += [f"### 版本 {version}", "", f"- 标题：{ad['title']}", f"- 正文：{ad['body']}",
                      f"- 核心卖点：{ad['selling_point']}", f"- CTA：{ad['cta']}", ""]
    if calendar:
        lines += ["## 30天内容日历", "", "| 日期 | 平台 | 主题 | 内容方向 | 目标 |", "|---|---|---|---|---|"]
        for row in calendar:
            lines.append("| " + " | ".join(str(row[k]).replace("|", "\\|").replace("\n", " ") for k in ("日期", "平台", "主题", "内容方向", "目标")) + " |")
    return "\n".join(lines) + "\n"
