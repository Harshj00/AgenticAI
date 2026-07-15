import unittest

from agent import Agent
from tools.calculator import calculator


class AgentFeaturesTests(unittest.TestCase):
    def test_calculator_supports_scientific_functions_and_words(self):
        self.assertEqual(calculator({"expression": "sin(pi/2) + 2"}), "3.0")
        self.assertEqual(calculator({"expression": "2^10"}), "1024")

    def test_agent_remembers_name_for_the_session(self):
        agent = Agent()
        agent.run("My name is Asha")
        self.assertEqual(agent.session_name, "Asha")


if __name__ == "__main__":
    unittest.main()
