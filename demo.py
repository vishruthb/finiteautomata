from fiauto import FiniteAutomata

def main():
    fsm = FiniteAutomata()
    fsm.start('q0').accept('q2')
    fsm.transition('q0', 'a', 'q1')
    fsm.transition('q1', 'a', 'q1')
    fsm.transition('q1', 'b', 'q1')
    fsm.transition('q1', 'a', 'q2')
    fsm.draw('fsm_demo', view=True)

if __name__ == '__main__':
    main()
