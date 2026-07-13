from backend.agents.scene_planner import ScenePlanner
from backend.agents.script_agent import ScriptAgent

script_agent = ScriptAgent()

scene_planner = ScenePlanner()

script = script_agent.generate(
    "5 Amazing Facts About Black Holes"
)

scene_plan = scene_planner.generate(script)

print(scene_plan)