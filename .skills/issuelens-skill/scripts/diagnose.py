import sys
import os
from google import genai
from pydantic import BaseModel, Field

class BugReport(BaseModel):
    title: str = Field(description="Issue title")
    root_cause: str = Field(description="Probable reason")
    evidence: list[str] = Field(description="Visible facts")
    missing_info: list[str] = Field(description="Omitted context")
    suggested_patch: str = Field(description="Recommended fix")

def run(log_text: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        return
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[f"Extract structured issue from log:\n{log_text}"]
    )
    print(response.text)

if __name__ == "__main__":
    sample = sys.argv[1] if len(sys.argv) > 1 else "KeyError: 'order' in server.py line 42"
    run(sample)
