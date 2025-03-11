from graphviz import Digraph
import os
import platform
import shutil

class FiniteAutomata:
    def __init__(self):
        self.states = set()
        self.start_state = None
        self.accept_states = set()
        self.transitions = []  # (from_state, symbol, to_state)

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
    
    def _windows_util(self):
        """Check for Graphviz 'dot' executable and attempt Windows-specific fixes."""
        if not shutil.which("dot"):
            if platform.system() == "Windows":
                default_path = r"C:\Program Files\Graphviz\bin"
                if os.path.isdir(default_path):
                    os.environ["PATH"] += os.pathsep + default_path
                if not shutil.which("dot"):
                    raise RuntimeError(
                        "Graphviz 'dot' executable not found. Please install Graphviz "
                        "and add its bin folder to your PATH (e.g., C:\\Program Files\\Graphviz\\bin)."
                    )
            else:
                pass # TODO: Add Linux and Apple ARM support

    def draw(self, filename='fsm', format='png', view=False):
        """
        Render the automata as a diagram.
        - filename: the output filename (without extension)
        - format: output file format (png, pdf, etc.)
        - view: if True, automatically open the generated diagram.
        """
        self._windows_util()

        dot = Digraph(name='FiniteAutomata', format=format)
        dot.attr(rankdir='LR')
        dot.node('', shape='none')

        for state in self.states:
            shape = 'doublecircle' if state in self.accept_states else 'circle'
            dot.node(state, shape=shape)

        if self.start_state:
            dot.edge('', self.start_state)

        grouped = {}
        for from_state, symbol, to_state in self.transitions:
            key = (from_state, to_state)
            grouped.setdefault(key, []).append(symbol)

        for (from_state, to_state), symbols in grouped.items():
            label = ', '.join(symbols)
            dot.edge(from_state, to_state, label=label)

        dot.render(filename, view=view)
        return dot