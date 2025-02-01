from falib import FiniteAutomata

def main():
    # q0 is the start state, q1 is accepting.
    # 'a' transitions q0 to q1, and 'b' is a self-loop on q1.
    fsm = FiniteAutomata()
    fsm.start('q0').accept('q1')
    fsm.transition('q0', 'a', 'q1')
    fsm.transition('q1', 'b', 'q1')
    fsm.draw('fsm_demo', view=True)

if __name__ == '__main__':
    main()
