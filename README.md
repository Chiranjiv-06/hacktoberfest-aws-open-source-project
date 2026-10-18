⚡ IssueLens: Multimodal AI Bug Report Workbench & MCP Server

Automated multimodal issue triage turning raw stack traces, error logs, and screenshots into reproducible GitHub issues in seconds.

Built for **Hacktoberfest Hack Day Nagpur × AWS SBG RTMSSU (2026)**.

---

## 🏆 Targeted Challenge Tracks
- **Best Use of Gemma 4:** Multimodal reasoning across application crash screenshots and raw stack traces using `gemma-4-26b-a4b-it` via Google GenAI SDK.
- **Best Open-Source AI Project (DigitalOcean & DEV Relay):**
  - Conforms to the **Agent Skill Open Standard** (`.skills/issuelens-skill/SKILL.md`).
  - Native **Model Context Protocol (MCP)** server (`mcp_server.py`) compatible with Antigravity, Cursor, and Claude Code.
  - DigitalOcean AI runtime harness specification (`harness.json`).
  - Released under the permissive **MIT License**.

---

## 🛠️ Architecture & Tech Stack
- **AI Core:** Gemma 4 / Gemini API
- **Protocol:** Model Context Protocol (MCP) via FastMCP
- **Workbench UI:** Streamlit
- **Schema Validation:** Pydantic v2
- **Standard:** Agent Skill Open Standard (`agentskills.io/v1`)

---

## 🚀 Quickstart Setup

1. **Activate Environment & Install:**
   ```bash
   source venv/Scripts/activate
   pip install -r requirements.txt
