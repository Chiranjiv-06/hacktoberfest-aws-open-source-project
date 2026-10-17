---
name: issuelens-skill
description: Automated diagnostic tool that ingests terminal stack traces and UI screenshots to produce structured, reproducible GitHub issues using Gemma open-weights.
license: MIT
metadata:
  author: Chiranjiv Kuhikar
  standard: agentskills.io/v1
  model_target: gemma-4-26b-a4b-it
compatibility: Requires Python 3.10+, google-genai, pydantic
---

# IssueLens Diagnostic Skill

## Purpose
Analyzes software errors, extracts verified evidence, identifies missing reproduction steps, and outputs clean Markdown issues.

## Parameters
- logs (string, required): Stack trace or terminal output.
- context (string, optional): Context of user actions when the crash occurred.
- image_path (string, optional): Path to error screenshot.
