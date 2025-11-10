# finiteautomata

Craft beautiful, minimalistic finite automata diagrams with intuitiive Python syntax and a purpose-built rendering engine.

## Features

- Define start, accept, and intermediate states with chainable calls.
- Render with an automata-first layout engine: orthogonal connectors, grouped transitions, and modern styling.
- Export to SVG, PNG, and interactive HTML in one call.
- Customize the look & feel through theming and spacing controls.

## Installation

```bash
pip install finiteautomata
```

or:

```bash
pip install finiteautomata[cairo]
```

if you want to use PNG support.

## Quickstart

```python
from finiteautomata import FiniteAutomata

fsm = FiniteAutomata()
fsm.start('q0').accept('q2')
fsm.transition('q0', 'a', 'q1')
fsm.transition('q1', 'a', 'q1')  # self-loop
fsm.transition('q1', 'b', 'q1')
fsm.transition('q1', 'a', 'q2')

fsm.draw('demo')  # writes demo.svg by default
```

### Rendering multiple formats

```python
fsm.configure_renderer(formats=('svg', 'html', 'png'))

# supply a theme for this render only.
from finiteautomata import RendererTheme

noir = RendererTheme(
    background_color="#0f172a",
    state_fill="#1e293b",
    state_border="#e2e8f0",
    accept_state_border="#38bdf8",
    transition_color="#38bdf8",
    transition_text_color="#38bdf8",
    state_text_color="#e2e8f0",
    start_indicator_color="#38bdf8",
)

outputs = fsm.draw('demo', view=True, theme=noir)
print(outputs)  # {'svg': 'demo.svg', 'html': 'demo.html', 'png': 'demo.png'}
```

## API Reference

- **`state(state: str)`**  
  Adds a state to the automaton and returns the instance for chaining.

- **`start(state: str)`**  
  Sets (and implicitly creates) the starting state.

- **`accept(state: str)`**  
  Marks a state as accepting. Accept states are rendered with a dual ring.

- **`transition(from_state: str, symbol: str, to_state: str)`**  
  Adds a transition. Multiple transitions between the same pair are automatically grouped, and self-loops are supported out of the box.

- **`configure_renderer(...)`**  
  Adjust default export formats, theming, and layout spacing.

- **`draw(filename: str = 'fsm', *, format: Optional[str] = None, formats: Optional[Iterable[str]] = None, view: bool = False, theme: Optional[RendererTheme] = None)`**  
  Renders the automaton. `formats` overrides the configured default (e.g. `('svg', 'html')`). Use `view=True` to open the first generated artifact automatically.
