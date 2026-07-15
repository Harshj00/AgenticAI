from agent import Agent


def run_tests():
    a = Agent()
    print('Q: What is 25*18?')
    print('A:', a.run('What is 25*18?'))
    print('\nQ: Tell me the current time and date in India')
    print('A:', a.run('Tell me the current time and date in India'))


if __name__ == '__main__':
    run_tests()
