import os
import streamlit as st
from PIL import Image
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

st.set_page_config(page_title="IssueLens - AI Bug Workbench", layout="wide")
st.title("IssueLens: Multimodal Bug Report Workbench")
st.caption("Powered by Gemma 4 | Compliant with Agent Skill Open Standard & MCP")

api_key = os.environ.get("GEMINI_API_KEY", "")

class BugReport(BaseModel):
    title: str = Field(description="Clear, concise issue title")
    root_cause_hypothesis: str = Field(description="Probable reason for failure")
    evidence_observed: list[str] = Field(description="Concrete details seen in image or logs")
    missing_reproduction_info: list[str] = Field(description="Details the reporter omitted")
    reproduction_steps: list[str] = Field(description="Numbered reproduction steps")
    suggested_patch: str = Field(description="Markdown code patch or fix recommendation")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_image = st.file_uploader("1. Error Screenshot (Optional)", type=["png", "jpg", "jpeg"])
    log_text = st.text_area("2. Stack Trace / Terminal Logs", height=200, placeholder="Paste exception logs here...")
    user_notes = st.text_input("3. What were you trying to do?", placeholder="e.g. Submitting checkout form")
    run_btn = st.button("Generate Structured Issue", type="primary", use_container_width=True)

with col2:
    if run_btn:
        if not api_key:
            st.error("GEMINI_API_KEY environment variable is not set!")
        elif not uploaded_image and not log_text.strip():
            st.warning("Please provide at least a screenshot or a log snippet.")
        else:
            with st.spinner("Analyzing with Gemma 4..."):
                try:
                    client = genai.Client(api_key=api_key)
                    contents = []
                    
                    if uploaded_image:
                        img = Image.open(uploaded_image)
                        contents.append(img)
                    
                    prompt = f"""
                    Analyze this software failure.
                    Context provided by user: {user_notes}
                    Logs:
                    {log_text}
                    
                    Extract all technical facts and provide an actionable bug report following the schema.
                    """
                    contents.append(prompt)
                    
                    try:
                        response = client.models.generate_content(
                            model="gemma-4-26b-a4b-it",
                            contents=contents,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                response_schema=BugReport
                            )
                        )
                    except Exception:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=contents,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                response_schema=BugReport
                            )
                        )
                    
                    report = BugReport.model_validate_json(response.text)
                    
                    st.subheader(f"[Issue] {report.title}")
                    st.info(f"**Hypothesis:** {report.root_cause_hypothesis}")
                    
                    st.markdown("### Evidence Observed")
                    for item in report.evidence_observed:
                        st.markdown(f"- {item}")
                        
                    st.markdown("### Missing Information")
                    for item in report.missing_reproduction_info:
                        st.markdown(f"- {item}")
                        
                    st.markdown("### Suggested Fix")
                    st.markdown(report.suggested_patch)
                    
                    md_export = (
                        f"# {report.title}\n\n"
                        f"## Root Cause Hypothesis\n{report.root_cause_hypothesis}\n\n"
                        f"## Evidence\n" + "\n".join([f"- {e}" for e in report.evidence_observed]) + "\n\n"
                        f"## Missing Info\n" + "\n".join([f"- {m}" for e in report.missing_reproduction_info]) + "\n\n"
                        f"## Fix\n{report.suggested_patch}"
                    )
                    
                    st.download_button(
                        label="Download GitHub Issue (.md)",
                        data=md_export,
                        file_name="issue.md",
                        mime="text/markdown"
                    )
                    
                except Exception as e:
                    st.error(f"Execution Error: {e}")
