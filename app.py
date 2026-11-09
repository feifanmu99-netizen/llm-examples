"""MarketPilot AI — Streamlit entry point."""

import streamlit as st

from marketpilot.ai import generate_ads, generate_calendar, generate_strategy, get_model_config
from marketpilot.core import PLATFORMS, PRESET, demo_ads, demo_calendar, demo_strategy, validate_brief
from marketpilot.export import calendar_csv, report_markdown

st.set_page_config(page_title="MarketPilot AI | AI 营销策划", page_icon="📈", layout="wide")
st.markdown("""
<style>
  .stApp {background: #ffffff; color: #12233f;}
  [data-testid="stSidebar"] {background: #f5f8ff;}
  h1, h2, h3 {color: #102b57; letter-spacing: -0.02em;}
  div.stButton > button[kind="primary"], div.stDownloadButton > button[kind="primary"] {
    background: #1769d1; border-color: #1769d1;
  }
  .block-container {max-width: 1220px; padding-top: 2.5rem;}
</style>
""", unsafe_allow_html=True)

FIELD_LABELS = {
    "brand": "品牌名称", "product": "产品名称", "description": "产品描述",
    "advantages": "产品优势", "audience": "目标客户", "region": "目标国家或地区",
    "goal": "营销目标",
}


def clear_results():
    for name in ("strategy", "ads", "calendar", "strategy_mode", "ads_mode", "calendar_mode"):
        st.session_state.pop(name, None)


def load_preset():
    for key, value in PRESET.items():
        st.session_state[f"input_{key}"] = value.copy() if isinstance(value, list) else value
    st.session_state.brief = PRESET.copy()
    clear_results()


if "brief" not in st.session_state:
    st.session_state.brief = None
for field in FIELD_LABELS:
    st.session_state.setdefault(f"input_{field}", "")
st.session_state.setdefault("input_budget", 5000)
st.session_state.setdefault("input_platforms", [])

with st.sidebar:
    st.markdown("## MarketPilot AI")
    st.caption("品牌信息与页面导航")
    section = st.radio("导航", ["品牌概览", "营销策略", "广告生成", "内容日历"], label_visibility="collapsed")
    st.divider()
    st.button("载入羽毛球拍预设案例", on_click=load_preset, use_container_width=True)
    with st.form("brand_form"):
        st.markdown("### 品牌信息输入")
        for field, label in FIELD_LABELS.items():
            if field in ("description", "advantages"):
                st.text_area(label, key=f"input_{field}", height=86)
            else:
                st.text_input(label, key=f"input_{field}")
        st.number_input("营销预算（按自选币种）", min_value=0, step=500, key="input_budget")
        st.multiselect("主要营销平台", PLATFORMS, key="input_platforms")
        saved = st.form_submit_button("保存品牌信息", type="primary", use_container_width=True)
    if saved:
        candidate = {field: st.session_state[f"input_{field}"].strip() for field in FIELD_LABELS}
        candidate["budget"] = st.session_state.input_budget
        candidate["platforms"] = list(st.session_state.input_platforms)
        try:
            validate_brief(candidate)
        except ValueError as exc:
            st.error(str(exc))
        else:
            if candidate != st.session_state.brief:
                clear_results()
            st.session_state.brief = candidate
            st.success("品牌信息已保存。")

model_config = get_model_config()
mode = f"真实 AI 模式 · {model_config.provider} ({model_config.model})" if model_config else "演示模式"
st.title("MarketPilot AI")
st.caption("从品牌信息到可执行的 30 天营销计划")
if model_config:
    st.info(f"已检测到 {model_config.provider} API Key。点击生成按钮将请求 {model_config.model}；模型输出仍需人工核实。")
else:
    st.warning("演示模式：未检测到 DeepSeek 或 OpenAI API Key。生成按钮只展示本地预设建议，不会调用真实 AI。")

brief = st.session_state.brief
if not brief:
    st.info("请在左侧填写并保存品牌信息，或载入羽毛球拍预设案例。")
    st.stop()


def run_generation(state_key, mode_key, demo_fn, ai_fn):
    st.session_state.pop(state_key, None)
    st.session_state.pop(mode_key, None)
    try:
        with st.spinner("正在生成，请稍候…" if model_config else "正在载入演示内容…"):
            value = ai_fn() if model_config else demo_fn()
    except Exception as exc:
        st.error(f"{model_config.provider} 请求失败：{exc}" if model_config else f"演示内容生成失败：{exc}")
    else:
        st.session_state[state_key] = value
        st.session_state[mode_key] = mode


if section == "品牌概览":
    st.header("品牌概览")
    left, right = st.columns(2, gap="large")
    with left:
        st.subheader(brief["brand"])
        st.write(brief["description"])
        st.markdown(f"**产品：** {brief['product']}")
        st.markdown(f"**产品优势：** {brief['advantages']}")
    with right:
        st.markdown(f"**目标客户：** {brief['audience']}")
        st.markdown(f"**目标地区：** {brief['region']}")
        st.markdown(f"**营销目标：** {brief['goal']}")
        st.markdown(f"**营销预算：** {brief['budget']:,.0f}（按输入币种）")
        st.markdown(f"**主要平台：** {', '.join(brief['platforms'])}")
    st.divider()
    st.subheader("工作流程")
    st.write("在左侧选择营销策略、广告生成和内容日历，逐项生成内容；已生成结果会保存在当前浏览器会话中。")

elif section == "营销策略":
    st.header("AI 营销策略生成")
    st.write("输出品牌定位、用户画像、卖点、渠道、预算、30 天行动计划和 KPI。")
    if st.button("生成营销策略", type="primary"):
        run_generation("strategy", "strategy_mode", lambda: demo_strategy(brief), lambda: generate_strategy(model_config, brief))
    strategy = st.session_state.get("strategy")
    if strategy:
        st.caption(f"生成方式：{st.session_state.strategy_mode}。假设、建议及产品主张需要人工验证。")
        for field, label in [("positioning", "品牌定位"), ("persona", "目标用户画像"),
                             ("selling_points", "核心营销卖点"), ("channels", "推荐营销渠道"),
                             ("budget", "预算分配建议"), ("plan", "30 天营销行动计划"),
                             ("kpis", "核心 KPI 及评估方法")]:
            st.subheader(label)
            value = strategy[field]
            if isinstance(value, list):
                for item in value:
                    st.markdown(f"- {item}")
            else:
                st.write(value)
        report = report_markdown(brief, strategy, st.session_state.get("ads"),
                                 st.session_state.get("calendar"), st.session_state.strategy_mode)
        st.download_button("下载 Markdown 营销策略报告", report.encode("utf-8"),
                           file_name="marketpilot-strategy.md", mime="text/markdown", type="primary")

elif section == "广告生成":
    st.header("AI 广告文案生成")
    platform = st.selectbox("选择广告平台", PLATFORMS)
    if st.button("生成 A/B 广告文案", type="primary"):
        run_generation("ads", "ads_mode",
                       lambda: {"platform": platform, "content": demo_ads(brief, platform)},
                       lambda: {"platform": platform, "content": generate_ads(model_config, brief, platform)})
    ads = st.session_state.get("ads")
    if ads:
        st.caption(f"平台：{ads['platform']} · 生成方式：{st.session_state.ads_mode}")
        a, b = st.columns(2, gap="large")
        for col, version in ((a, "A"), (b, "B")):
            with col:
                ad = ads["content"][version]
                st.subheader(f"版本 {version}")
                st.markdown(f"**广告标题**  {ad['title']}")
                st.write(ad["body"])
                st.markdown(f"**核心卖点：** {ad['selling_point']}")
                st.markdown(f"**CTA：** {ad['cta']}")

elif section == "内容日历":
    st.header("30 天内容营销日历")
    if st.button("生成内容日历", type="primary"):
        run_generation("calendar", "calendar_mode", lambda: demo_calendar(brief),
                       lambda: generate_calendar(model_config, brief))
    calendar = st.session_state.get("calendar")
    if calendar:
        st.caption(f"共 {len(calendar)} 天 · 生成方式：{st.session_state.calendar_mode}")
        st.dataframe(calendar, use_container_width=True, hide_index=True)
        st.download_button("下载 CSV 营销日历", calendar_csv(calendar),
                           file_name="marketpilot-calendar.csv", mime="text/csv", type="primary")
