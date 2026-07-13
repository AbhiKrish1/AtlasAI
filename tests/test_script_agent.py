from backend.agents.script_agent import ScriptAgent

agent = ScriptAgent()

result = agent.generate(
    "5 Amazing Facts About Black Holes"
)

print(result)