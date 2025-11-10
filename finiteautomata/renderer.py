import os
import sys
import webbrowser
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


@dataclass
class RendererTheme:
    background_color: str = "#ffffff"
    state_fill: str = "#f7f9fc"
    state_border: str = "#1f2933"
    accept_state_border: str = "#0070f3"
    transition_color: str = "#0b7285"
    transition_text_color: str = "#0b7285"
    state_text_color: str = "#1f2933"
    start_indicator_color: str = "#1f2933"
    font_family: str = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"


@dataclass
class RendererConfig:
    formats: Sequence[str] = field(default_factory=lambda: ("svg",))
    theme: RendererTheme = field(default_factory=RendererTheme)
    canvas_padding: int = 96
    horizontal_gap: int = 220
    vertical_gap: int = 160
    state_radius: int = 36
    arrow_size: int = 12


class AutomataRenderer:
    def __init__(
        self,
        states: Iterable[str],
        start_state: Optional[str],
        accept_states: Iterable[str],
        transitions: Iterable[Tuple[str, str, str]],
        config: Optional[RendererConfig] = None,
    ):
        self.states = list(states)
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.transitions = list(transitions)
        self.config = config or RendererConfig()
        self._positions: Dict[str, Tuple[float, float]] = {}
        self._levels: Dict[str, int] = {}
        self._grouped_transitions: Dict[Tuple[str, str], List[str]] = {}
        self._compute_layout()
        self._group_transitions()

    def render(self, filename: str, formats: Sequence[str], view: bool = False) -> Dict[str, str]:
        outputs: Dict[str, str] = {}
        for fmt in formats:
            fmt_lower = fmt.lower()
            if fmt_lower == "svg":
                outputs["svg"] = self._render_svg(filename)
            elif fmt_lower == "html":
                outputs["html"] = self._render_html(filename)
            elif fmt_lower == "png":
                outputs["png"] = self._render_png(filename)
            else:
                raise ValueError(f"Unsupported output format '{fmt}'. Expected one of svg, png, html.")

        if view and outputs:
            self._open(outputs, filename)

        return outputs

    # Layout -----------------------------------------------------------------
    def _compute_layout(self) -> None:
        levels: Dict[str, int] = {}
        adjacency: Dict[str, List[str]] = {}
        for src, _, dst in self.transitions:
            adjacency.setdefault(src, []).append(dst)

        if self.start_state and self.start_state in self.states:
            queue = [self.start_state]
            levels[self.start_state] = 0
            while queue:
                current = queue.pop(0)
                for nxt in adjacency.get(current, []):
                    if nxt == current:
                        continue
                    tentative = levels[current] + 1
                    if nxt not in levels or tentative < levels[nxt]:
                        levels[nxt] = tentative
                        queue.append(nxt)

        remaining_states = [s for s in self.states if s not in levels]
        if remaining_states:
            max_level = max(levels.values(), default=-1)
            for state in sorted(remaining_states):
                max_level += 1
                levels[state] = max_level

        self._levels = levels

        levels_to_states: Dict[int, List[str]] = {}
        for state, level in levels.items():
            levels_to_states.setdefault(level, []).append(state)

        for level_states in levels_to_states.values():
            level_states.sort()

        positions: Dict[str, Tuple[float, float]] = {}
        for level, level_states in sorted(levels_to_states.items()):
            for idx, state in enumerate(level_states):
                x = level * self.config.horizontal_gap
                y = idx * self.config.vertical_gap
                positions[state] = (x, y)

        # center positions vertically
        if positions:
            ys = [pos[1] for pos in positions.values()]
            min_y, max_y = min(ys), max(ys)
            offset = (max_y - min_y) / 2
            for state, (x, y) in positions.items():
                positions[state] = (x, y - offset)

        self._positions = positions

    def _group_transitions(self) -> None:
        grouped: Dict[Tuple[str, str], List[str]] = {}
        for src, symbol, dst in self.transitions:
            key = (src, dst)
            grouped.setdefault(key, []).append(symbol)
        self._grouped_transitions = grouped

    # Rendering ---------------------------------------------------------------
    def _render_svg(self, filename: str) -> str:
        svg_content = self._build_svg()
        path = f"{filename}.svg"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg_content)
        return path

    def _render_html(self, filename: str) -> str:
        svg_content = self._build_svg(inline=True)
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{filename} · Finite Automata</title>
  <style>
    :root {{
      color-scheme: light dark;
      font-family: {self.config.theme.font_family};
      background: {self.config.theme.background_color};
      margin: 0;
      padding: 0;
    }}
    body {{
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: {self.config.theme.background_color};
    }}
    svg {{
      max-width: min(90vw, 1200px);
      height: auto;
      box-shadow: 0 24px 60px rgba(15, 23, 42, 0.12);
      border-radius: 18px;
    }}
    .state:hover {{
      filter: drop-shadow(0 12px 28px rgba(15, 23, 42, 0.24));
    }}
  </style>
</head>
<body>
{svg_content}
</body>
</html>
"""
        path = f"{filename}.html"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        return path

    def _render_png(self, filename: str) -> str:
        try:
            import cairosvg  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "PNG output requires the optional dependency 'cairosvg'. "
                "Install it via `pip install finiteautomata[cairo]`."
            ) from exc

        svg_content = self._build_svg(inline=True)
        png_path = f"{filename}.png"
        cairosvg.svg2png(bytestring=svg_content.encode("utf-8"), write_to=png_path)
        return png_path

    # Helpers ----------------------------------------------------------------
    def _build_svg(self, inline: bool = False) -> str:
        if not self._positions:
            canvas_width = canvas_height = 2 * self.config.canvas_padding + self.config.state_radius * 2
        else:
            xs = [pos[0] for pos in self._positions.values()]
            ys = [pos[1] for pos in self._positions.values()]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)
            canvas_width = (
                max_x - min_x + 2 * self.config.canvas_padding + self.config.state_radius * 2
            )
            canvas_height = (
                max_y - min_y + 2 * self.config.canvas_padding + self.config.state_radius * 2
            )

        view_box = f"0 0 {canvas_width:.2f} {canvas_height:.2f}"
        theme = self.config.theme

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" '
            f'width="{canvas_width:.2f}" height="{canvas_height:.2f}" '
            f'style="background:{theme.background_color}; font-family:{theme.font_family};">'
        ]

        origin = (self.config.canvas_padding + self.config.state_radius, canvas_height / 2)
        position_cache = {
            state: (
                origin[0] + (self._positions[state][0] if self._positions else 0),
                origin[1] + (self._positions[state][1] if self._positions else 0),
            )
            for state in self.states
        }

        svg_parts.append(self._render_transitions(position_cache, theme))
        svg_parts.append(self._render_states(position_cache, theme))

        svg_parts.append("</svg>")
        svg_output = "\n".join(svg_parts)
        return svg_output if inline else svg_output + "\n"

    def _render_states(
        self, position_cache: Dict[str, Tuple[float, float]], theme: RendererTheme
    ) -> str:
        parts: List[str] = []

        if self.start_state and self.start_state in position_cache:
            sx, sy = position_cache[self.start_state]
            arrow_x = sx - self.config.state_radius - 48
            parts.append(
                f'<g class="start-indicator">'
                f'<path d="M {arrow_x} {sy} L {arrow_x + 24} {sy - 18} L {arrow_x + 24} {sy + 18} Z" '
                f'fill="{theme.start_indicator_color}" opacity="0.72"/>'
                f'<line x1="{arrow_x + 24}" y1="{sy}" x2="{sx - self.config.state_radius}" y2="{sy}" '
                f'stroke="{theme.start_indicator_color}" stroke-width="3" opacity="0.72"/>'
                f"</g>"
            )

        for state, (x, y) in position_cache.items():
            is_accept = state in self.accept_states
            circle = (
                f'<g class="state" transform="translate({x},{y})">'
                f'<circle r="{self.config.state_radius}" fill="{theme.state_fill}" '
                f'stroke="{theme.state_border}" stroke-width="2" />'
            )
            if is_accept:
                circle += (
                    f'<circle r="{self.config.state_radius - 6}" fill="none" '
                    f'stroke="{theme.accept_state_border}" stroke-width="3" />'
                )
            circle += (
                f'<text text-anchor="middle" dominant-baseline="middle" '
                f'fill="{theme.state_text_color}" font-size="18" font-weight="600">{state}</text>'
                f"</g>"
            )
            parts.append(circle)
        return "\n".join(parts)

    def _render_transitions(
        self, position_cache: Dict[str, Tuple[float, float]], theme: RendererTheme
    ) -> str:
        parts: List[str] = []
        for (src, dst), symbols in self._grouped_transitions.items():
            if src not in position_cache or dst not in position_cache:
                continue
            src_pos = position_cache[src]
            dst_pos = position_cache[dst]
            path_d, label_pos = self._transition_path(src, dst, src_pos, dst_pos)
            label = ", ".join(symbols)
            parts.append(
                f'<g class="transition">'
                f'<path d="{path_d}" fill="none" stroke="{theme.transition_color}" '
                f'stroke-width="2.4" marker-end="url(#arrowhead)" opacity="0.82"/>'
                f'<text x="{label_pos[0]:.2f}" y="{label_pos[1]:.2f}" '
                f'fill="{theme.transition_text_color}" font-size="15" '
                f'text-anchor="middle" dominant-baseline="central">{label}</text>'
                f"</g>"
            )

        marker = (
            '<defs>'
            '<marker id="arrowhead" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">'
            f'<path d="M 0 0 L 12 6 L 0 12 z" fill="{theme.transition_color}" />'
            "</marker>"
            "</defs>"
        )
        return marker + "\n" + "\n".join(parts)

    def _transition_path(
        self,
        src: str,
        dst: str,
        src_pos: Tuple[float, float],
        dst_pos: Tuple[float, float],
    ) -> Tuple[str, Tuple[float, float]]:
        radius = self.config.state_radius
        if src == dst:
            start_x, start_y = src_pos
            loop_radius = radius * 1.2
            top_y = start_y - radius * 2.1
            path = (
                f"M {start_x + radius * 0.3:.2f} {start_y - radius:.2f} "
                f"C {start_x + loop_radius:.2f} {top_y:.2f} "
                f"{start_x - loop_radius:.2f} {top_y:.2f} "
                f"{start_x - radius * 0.3:.2f} {start_y - radius:.2f}"
            )
            label_pos = (start_x, top_y - 14)
            return path, label_pos

        sx, sy = src_pos
        dx, dy = dst_pos
        direction = 1 if dx >= sx else -1
        start_point = (sx + radius * direction, sy)
        end_point = (dx - radius * direction, dy)

        level_diff = self._levels.get(dst, 0) - self._levels.get(src, 0)
        vertical_offset = 0
        if level_diff == 0:
            vertical_offset = radius * 2.8
            if dy >= sy:
                vertical_offset *= -1

        mid_x = (start_point[0] + end_point[0]) / 2 + direction * radius * 0.6
        bend_y = dy + vertical_offset

        path = (
            f"M {start_point[0]:.2f} {start_point[1]:.2f} "
            f"L {mid_x:.2f} {start_point[1]:.2f} "
            f"L {mid_x:.2f} {bend_y:.2f} "
            f"L {end_point[0]:.2f} {end_point[1]:.2f}"
        )
        label_pos = ((start_point[0] + end_point[0]) / 2, (start_point[1] + bend_y) / 2 - 12)
        return path, label_pos

    def _open(self, outputs: Dict[str, str], filename: str) -> None:
        open_target = None
        for preference in ("html", "svg", "png"):
            if preference in outputs:
                open_target = outputs[preference]
                break
        if not open_target:
            return
        path = os.path.abspath(open_target)
        if open_target.endswith(".html"):
            webbrowser.open(f"file://{path}")
        elif open_target.endswith(".svg"):
            webbrowser.open(f"file://{path}")
        elif open_target.endswith(".png"):
            if os.name == "nt":
                os.startfile(path)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                os.system(f"open '{path}'")
            else:
                os.system(f"xdg-open '{path}'")

