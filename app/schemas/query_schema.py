from pydantic import BaseModel

class query_schema(BaseModel):
    id:int
    question: str
    userid: int
    question : str
    answer : str
    cluster : int
    latency_ms : float
