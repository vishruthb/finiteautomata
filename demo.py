from finiteautomata import FiniteAutomata, RendererTheme

def main():
    fsm = FiniteAutomata()
    fsm.configure_renderer(formats=('svg', 'html'))

    fsm.start('q0').accept('q2')
    fsm.transition('q0', 'a', 'q1')
    fsm.transition('q1', 'a', 'q1')
    fsm.transition('q1', 'b', 'q1')
    fsm.transition('q1', 'a', 'q2')

    dusk_theme = RendererTheme(
        background_color="#0f172a",
        state_fill="#1e293b",
        state_border="#e2e8f0",
        accept_state_border="#38bdf8",
        transition_color="#38bdf8",
        transition_text_color="#38bdf8",
        state_text_color="#e2e8f0",
        start_indicator_color="#38bdf8",
    )

    outputs = fsm.draw('fsm_demo', view=True, theme=dusk_theme)
    for fmt, path in outputs.items():
        print(f"Generated {fmt.upper()} diagram at {path}")

if __name__ == '__main__':
    main()
