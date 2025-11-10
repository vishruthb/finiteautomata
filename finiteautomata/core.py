from typing import Iterable, Optional, Sequence, TYPE_CHECKING

from .renderer import AutomataRenderer, RendererConfig

if TYPE_CHECKING:
    from .renderer import RendererTheme

class FiniteAutomata:
    def __init__(self):
        self.states = set()
        self.start_state = None
        self.accept_states = set()
        self.transitions = []  # (from_state, symbol, to_state)
        self.renderer_config = RendererConfig()

    def state(self, state):
        """Add a state to the automata."""
        self.states.add(state)
        return self

    def start(self, state):
        """Define the start state."""
        self.state(state)
        self.start_state = state
        return self

    def accept(self, state):
        """Mark a state as accepting."""
        self.state(state)
        self.accept_states.add(state)
        return self

    def transition(self, from_state, symbol, to_state):
        """
        Define a transition from one state to another.
        Example: transition('q0', 'a', 'q1') makes input 'a' cause a move from q0 to q1.
        Self-transitions (where from_state == to_state) are supported.
        """
        self.state(from_state)
        self.state(to_state)
        self.transitions.append((from_state, symbol, to_state))
        return self
    
    def configure_renderer(
        self,
        *,
        formats: Optional[Sequence[str]] = None,
        theme: Optional["RendererTheme"] = None,
        canvas_padding: Optional[int] = None,
        horizontal_gap: Optional[int] = None,
        vertical_gap: Optional[int] = None,
        state_radius: Optional[int] = None,
    ):
        """
        Update the rendering configuration.

        - formats: iterable of output formats to use when draw() is called without overrides.
        - theme: RendererTheme instance to customize colors and typography.
        - numeric parameters adjust spacing and sizing heuristics.
        """
        if formats is not None:
            self.renderer_config.formats = tuple(formats)
        if theme is not None:
            self.renderer_config.theme = theme
        if canvas_padding is not None:
            self.renderer_config.canvas_padding = canvas_padding
        if horizontal_gap is not None:
            self.renderer_config.horizontal_gap = horizontal_gap
        if vertical_gap is not None:
            self.renderer_config.vertical_gap = vertical_gap
        if state_radius is not None:
            self.renderer_config.state_radius = state_radius
        return self

    def draw(
        self,
        filename: str = 'fsm',
        *,
        format: Optional[str] = None,
        formats: Optional[Iterable[str]] = None,
        view: bool = False,
        theme: Optional["RendererTheme"] = None,
    ):
        """
        Render the automata using the custom rendering engine.

        - filename: base filename used for outputs
        - format: legacy single-format parameter (superseded by `formats`)
        - formats: iterable of requested formats (svg, png, html)
        - view: automatically open the first generated artifact
        - theme: optional RendererTheme to override colors for this render
        """
        selected_formats: Sequence[str]
        if formats is not None:
            selected_formats = tuple(formats)
        elif format is not None:
            selected_formats = (format,)
        else:
            selected_formats = self.renderer_config.formats

        renderer = AutomataRenderer(
            self.states,
            self.start_state,
            self.accept_states,
            self.transitions,
            config=self._effective_config(theme),
        )
        outputs = renderer.render(filename, selected_formats, view=view)
        return outputs

    def _effective_config(self, theme_override: Optional["RendererTheme"]) -> RendererConfig:
        if theme_override is None:
            return self.renderer_config
        config_copy = RendererConfig(
            formats=self.renderer_config.formats,
            theme=theme_override,
            canvas_padding=self.renderer_config.canvas_padding,
            horizontal_gap=self.renderer_config.horizontal_gap,
            vertical_gap=self.renderer_config.vertical_gap,
            state_radius=self.renderer_config.state_radius,
            arrow_size=self.renderer_config.arrow_size,
        )
        return config_copy