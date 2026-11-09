"""Core and UI smoke tests. No real API key or network request is used."""

import csv
import os
from datetime import date
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest
from streamlit.testing.v1 import AppTest

from marketpilot.ai import ModelConfig, generate_strategy, get_model_config
from marketpilot.core import PRESET, demo_ads, demo_calendar, demo_strategy, validate_brief
from marketpilot.export import calendar_csv, report_markdown


def test_demo_outputs_and_exports():
    strategy = demo_strategy(PRESET)
    ads = demo_ads(PRESET, "Instagram")
    days = demo_calendar(PRESET, date(2026, 11, 8))
    assert len(days) == 30
    assert days[0]["日期"] == "2026-11-08"
    assert days[-1]["日期"] == "2026-12-07"
    assert set(ads) == {"A", "B"}
    assert ads["A"]["title"] != ads["B"]["title"]
    assert "【假设】" in strategy["persona"]
    report = report_markdown(PRESET, strategy, {"platform": "Instagram", "content": ads}, days)
    assert "## 营销策略" in report and "## 广告文案" in report and "## 30天内容日历" in report
    decoded = calendar_csv(days).decode("utf-8-sig")
    assert len(list(csv.DictReader(StringIO(decoded)))) == 30


def test_validation():
    with pytest.raises(ValueError):
        validate_brief({**PRESET, "platforms": []})


@patch.dict(os.environ, {"OPENAI_API_KEY": ""})
@patch("marketpilot.ai.get_model_config", return_value=None)
def test_streamlit_demo_buttons(_config):
    at = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py").run()
    assert not at.exception
    assert "演示模式" in at.warning[0].value
    at.button[0].click().run()  # load preset
    assert not at.exception
    assert at.session_state.brief["product"] == PRESET["product"]

    at.sidebar.radio[0].set_value("营销策略").run()
    at.button[0].click().run()
    assert not at.exception
    assert at.session_state.strategy_mode == "演示模式"
    assert at.download_button

    at.sidebar.radio[0].set_value("广告生成").run()
    at.button[0].click().run()
    assert not at.exception
    assert set(at.session_state.ads["content"]) == {"A", "B"}

    at.sidebar.radio[0].set_value("内容日历").run()
    at.button[0].click().run()
    assert not at.exception
    assert len(at.session_state.calendar) == 30
    assert at.download_button

    at.text_input(key="input_brand").set_value("更新后的品牌")
    at.button[-1].click().run()  # save the sidebar form
    assert not at.exception
    assert at.session_state.brief["brand"] == "更新后的品牌"
    assert "calendar" not in at.session_state


def test_ai_error_is_not_replaced_with_demo():
    with patch("marketpilot.ai.OpenAI") as client:
        client.return_value.chat.completions.create.side_effect = RuntimeError("API unavailable")
        with pytest.raises(RuntimeError, match="API unavailable"):
            generate_strategy(ModelConfig("DeepSeek", "deepseek-flash", "x", "https://api.deepseek.com"), PRESET)


@patch.dict(os.environ, {"DEEPSEEK_API_KEY": "x", "OPENAI_API_KEY": "y"})
def test_deepseek_configuration_takes_priority():
    config = get_model_config()
    assert config.provider == "DeepSeek"
    assert config.model == "deepseek-flash"
    assert config.base_url == "https://api.deepseek.com"
