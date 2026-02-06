from pydantic import BaseModel

class query_schema(BaseModel):
    question : str
    answer : str
    cluster : int

class query_schema_response(BaseModel):
    question: str
    userid: int
    question : str
    answer : str
    cluster : int
    latency_ms : float