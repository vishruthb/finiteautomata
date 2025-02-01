from graphviz import Digraph

class FiniteAutomata:
    def __init__(self):
        self.states = set()
        self.start_state = None
        self.accept_states = set()
        self.transitions = []  # List of tuples: (from_state, symbol, to_state)

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

    def draw(self, filename='fsm', format='png', view=False):
        """
        Render the automata as a diagram.
        - filename: the output filename (without extension)
        - format: output file format (png, pdf, etc.)
        - view: if True, automatically open the generated diagram.
        """
        dot = Digraph(name='FiniteAutomata', format=format)
        dot.attr(rankdir='LR')

        # Add an invisible starting node to point to the start state.
        dot.node('', shape='none')

        # Create nodes for each state.
        for state in self.states:
            shape = 'doublecircle' if state in self.accept_states else 'circle'
            dot.node(state, shape=shape)

        # Draw an edge from the invisible node to the start state.
        if self.start_state:
            dot.edge('', self.start_state)

        # Group transitions between the same states.
        grouped = {}
        for from_state, symbol, to_state in self.transitions:
            key = (from_state, to_state)
            grouped.setdefault(key, []).append(symbol)

        for (from_state, to_state), symbols in grouped.items():
            label = ', '.join(symbols)
            dot.edge(from_state, to_state, label=label)

        dot.render(filename, view=view)
        return dot


