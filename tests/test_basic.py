import os
from pathlib import Path

import pytest

from finiteautomata import FiniteAutomata, RendererTheme


def build_sample_machine():
    fsm = FiniteAutomata()
    fsm.start('q0').accept('q2')
    fsm.transition('q0', 'a', 'q1')
    fsm.transition('q1', 'a', 'q1')
    fsm.transition('q1', 'b', 'q1')
    fsm.transition('q1', 'a', 'q2')
    return fsm


def test_configure_renderer_returns_self():
    fsm = FiniteAutomata()
    result = fsm.configure_renderer(formats=('svg', 'html'), horizontal_gap=240)
    assert result is fsm
    assert fsm.renderer_config.formats == ('svg', 'html')
    assert fsm.renderer_config.horizontal_gap == 240


def test_svg_render_creates_file(tmp_path):
    fsm = build_sample_machine()
    filename = tmp_path / "sample"
    outputs = fsm.draw(str(filename), formats=('svg',))
    svg_path = Path(outputs['svg'])
    assert svg_path.is_file()
    svg_content = svg_path.read_text(encoding='utf-8')
    assert '<svg' in svg_content
    assert svg_content.count('class="state"') == len(fsm.states)
    assert 'class="transition"' in svg_content


def test_html_render_embedding(tmp_path):
    fsm = build_sample_machine()
    filename = tmp_path / "sample"
    outputs = fsm.draw(str(filename), formats=('html',))
    html_path = Path(outputs['html'])
    assert html_path.is_file()
    html = html_path.read_text(encoding='utf-8')
    assert '<!DOCTYPE html>' in html
    assert '<svg' in html


def test_theme_override(tmp_path):
    fsm = build_sample_machine()
    filename = tmp_path / "theme_sample"
    theme = RendererTheme(
        background_color="#111827",
        state_fill="#1f2937",
        state_border="#f9fafb",
        accept_state_border="#60a5fa",
        transition_color="#60a5fa",
        transition_text_color="#60a5fa",
        state_text_color="#f9fafb",
        start_indicator_color="#60a5fa",
    )
    outputs = fsm.draw(str(filename), formats=('svg',), theme=theme)
    svg_path = Path(outputs['svg'])
    svg = svg_path.read_text(encoding='utf-8')
    assert theme.background_color in svg
    assert theme.state_fill in svg


def test_png_render_optional_dependency(tmp_path, monkeypatch):
    pytest.importorskip("cairosvg")
    fsm = build_sample_machine()
    filename = tmp_path / "png_sample"
    outputs = fsm.draw(str(filename), formats=('png',))
    png_path = Path(outputs['png'])
    assert png_path.is_file()
    assert png_path.suffix == '.png'
    assert png_path.stat().st_size > 0


def test_draw_uses_default_formats(tmp_path):
    fsm = build_sample_machine()
    fsm.configure_renderer(formats=('svg', 'html'))
    filename = tmp_path / "defaults"
    outputs = fsm.draw(str(filename))
    assert set(outputs.keys()) == {'svg', 'html'}
    for path in outputs.values():
        assert Path(path).is_file()

