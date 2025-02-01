# falib

A Python library for creating finite automata diagrams with intuitive syntax.

## Features

- Define start, accept, and intermediate states.
- Add transitions (including self-loops).
- Render state diagrams using Graphviz.

## Syntax Documentation

- **`state(state: str)`**  
    Adds a state to the automata.  
    **Usage:**  
    ```python
    fsm.state('q0')
    ```

- **`start(state: str)`**  
    Sets the starting state of the automata. If the state does not already exist, it will be created.  
    **Usage:**  
    ```python
    fsm.start('q0')
    ```

- **`accept(state: str)`**  
    Marks a state as an accepting state. Accept states are displayed with a double circle in the diagram.  
    **Usage:**  
    ```python
    fsm.accept('q1')
    ```

- **`transition(from_state: str, symbol: str, to_state: str)`**  
    Adds a transition from one state to another, where the `symbol` denotes the input triggering the transition.  
    Self-loops are supported by setting `from_state` equal to `to_state`.  
    **Usage:**  
    ```python
    fsm.transition('q0', 'a', 'q1')  # Transition from q0 to q1 on input 'a'
    fsm.transition('q1', 'b', 'q1')  # Self-loop on q1 for input 'b'
    ```

- **`draw(filename: str = 'fsm', format: str = 'png', view: bool = False)`**  
    Renders the finite automata as a diagram using Graphviz.
    - `filename`: Base name for the output file (without extension).
    - `format`: File format (e.g., `'png'`, `'pdf'`).
    - `view`: If set to `True`, the diagram is automatically opened after rendering.
    
    **Usage:**  
    ```python
    fsm.draw('my_automata', view=True)
    ```
    The method groups transitions with the same source and destination, listing multiple symbols where applicable.