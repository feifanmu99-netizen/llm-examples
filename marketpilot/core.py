"""Input validation and deterministic, clearly labeled demo content."""

from datetime import date, timedelta

FIELDS = ("brand", "product", "description", "advantages", "audience", "region", "goal")
PLATFORMS = ["小红书", "抖音", "Instagram", "TikTok", "LinkedIn"]

PRESET = {
    "brand": "疾羽 Badminton",
    "product": "轻量进阶羽毛球拍",
    "description": "面向美国大学生的轻量羽毛球拍，适合校园社团训练和日常对打。",
    "advantages": "轻量、易上手；适合校园社团场景。具体性能须以产品测试为准。",
    "audience": "美国大学生羽毛球初学者及校园社团成员",
    "region": "美国",
    "goal": "提升校园人群的品牌认知并获取试打报名",
    "budget": 5000,
    "platforms": ["Instagram", "TikTok"],
}


def validate_brief(brief):
    missing = [name for name in FIELDS if not str(brief.get(name, "")).strip()]
    if missing:
        raise ValueError("请完整填写品牌、产品、描述、优势、受众、地区和营销目标。")
    if not brief.get("platforms"):
        raise ValueError("请至少选择一个主要营销平台。")
    if float(brief.get("budget", 0)) < 0:
        raise ValueError("营销预算不能为负数。")


def demo_strategy(brief):
    validate_brief(brief)
    budget = float(brief["budget"])
    allocations = [
        ("内容制作", 30), ("创作者合作", 25), ("平台投放", 25),
        ("社群活动", 15), ("测试与预留", 5),
    ]
    return {
        "positioning": f"【建议】将{brief['brand']}的{brief['product']}定位为面向{brief['audience']}的场景化选择；用实际产品资料核实主张。",
        "persona": f"【假设】目标用户是{brief['region']}的{brief['audience']}，重视使用体验、同伴推荐和购买便利性。需访谈验证。",
        "selling_points": [f"【待验证】{x.strip()}" for x in brief["advantages"].replace("；", "、").split("、") if x.strip()][:4],
        "channels": [f"【建议】{p}：发布短内容并测试不同主题的互动表现。" for p in brief["platforms"]],
        "budget": [f"{name}：{pct}%（约 {budget * pct / 100:,.0f}，与输入预算同币种）" for name, pct in allocations],
        "plan": [
            "第1–7天：核对产品信息，访谈目标用户，确定素材与基线指标。",
            "第8–14天：制作内容与 A/B 文案，小范围发布并记录互动。",
            "第15–21天：根据真实数据调整主题、渠道和预算。",
            "第22–30天：集中推广有效内容，复盘线索质量与成本。",
        ],
        "kpis": [
            "品牌认知：展示量、触达量；按平台后台数据每周记录。",
            "内容互动：互动率＝互动次数／展示量；比较不同主题。",
            "转化：试打报名数和有效报名率；用带参数链接与表单去重统计。",
            "效率：每条有效报名成本＝实际花费／有效报名数；仅在产生真实数据后计算。",
        ],
    }


def demo_ads(brief, platform):
    validate_brief(brief)
    if platform not in PLATFORMS:
        raise ValueError("请选择支持的广告平台。")
    product = brief["product"]
    audience = brief["audience"]
    advantage = brief["advantages"].split("；")[0]
    return {
        "A": {
            "title": f"{product}，从下一场练习开始",
            "body": f"为{audience}准备的{product}。{advantage}。了解产品详情，看看它是否适合你的校园运动计划。",
            "selling_point": f"【待验证】{advantage}",
            "cta": "查看产品详情",
        },
        "B": {
            "title": "约上球友，开启校园羽毛球时间",
            "body": f"想和朋友一起多打几场？了解{brief['brand']}的{product}，先确认产品参数，再决定是否报名试打。",
            "selling_point": "【建议】突出校园社交与试打体验",
            "cta": "了解试打方式",
        },
    }


def demo_calendar(brief, start=None):
    validate_brief(brief)
    start = start or date.today()
    themes = ["品牌故事", "使用场景", "产品介绍", "用户问题", "社团活动", "试打邀请", "一周复盘"]
    goals = ["建立认知", "激发互动", "解释卖点", "收集反馈", "促进参与", "获取线索", "复盘优化"]
    return [
        {
            "日期": (start + timedelta(days=i)).isoformat(),
            "平台": brief["platforms"][i % len(brief["platforms"])],
            "主题": themes[i % 7],
            "内容方向": f"【建议】围绕{brief['product']}的{themes[i % 7]}制作图文或短视频；核实所有产品表述。",
            "目标": goals[i % 7],
        }
        for i in range(30)
    ]
