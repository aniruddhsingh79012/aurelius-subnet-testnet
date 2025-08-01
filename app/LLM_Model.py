# filename: app.py

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import uvicorn  # ✅ Added for programmatic run

load_dotenv()

# ---- LLM Setup ----

llm = ChatGroq(
    temperature=0.1,
    model_name="llama-3.3-70b-versatile",
    max_tokens=3000,
    api_key=os.getenv("GROQ_API_KEY")  # ✅ Added api_key loading from .env
)

prompt = ChatPromptTemplate.from_template("""
You are an intelligent and helpful assistant tasked with analyzing user questions or requests thoroughly and providing thoughtful, practical suggestions or answers.

Please follow these instructions carefully:
- Think step by step before answering.
- If the user is asking for help or suggestions, deeply analyze the possible options, trade-offs, and recommendations.
- Use clear and concise language, but aim to be comprehensive and insightful.
- If clarification is needed, explain what assumptions you're making.
- Do not answer if the input is unclear or lacks necessary context — instead, ask for more information.

Now, carefully read the user's input below and respond in a structured and well-reasoned way.

User Input: {input}
""")


# ---- FastAPI Setup ----
app = FastAPI()

# ---- Request Schema ----
class RequestData(BaseModel):
    input: str

# ---- Response Schema ----
class ResponseData(BaseModel):
    assistant_message: str


# ---- Inference Endpoint ----

@app.post("/send_message/", response_model=ResponseData)
async def send_message(data: RequestData):
    formatted_prompt = prompt.format_messages(input=data.input)
    response = llm.invoke(formatted_prompt)
    return {"assistant_message": response.content}


# ✅ Run the app with uvicorn programmatically
if __name__ == "__main__":
    uvicorn.run("LLM_Model:app", host="127.0.0.1", port=5001, reload=True)
