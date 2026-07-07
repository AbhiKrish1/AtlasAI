from pydantic import BaseModel


class ScriptResponse(BaseModel):
    """
    Response returned by the ScriptAgent.
    """

    title: str
    hook: str
    script: str
    estimated_duration: int