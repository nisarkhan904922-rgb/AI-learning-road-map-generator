"""Learning Roadmap Generator
Streamlit UI + Groq LLM.
"""

import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # loads GROQ_API_KEY from a local .env file if present

MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """You are an expert learning coach and curriculum designer.
Create realistic, practical, well-structured learning roadmaps.
Always respond in clean Markdown."""


def get_api_key() -> str | None:
    """Look for the API key in Streamlit secrets, then environment, then sidebar."""
    try:
        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY")


def build_prompt(field: str, level: str, duration: int, unit: str, hours: int) -> str:
    return f"""Create a personalized learning roadmap with these details:

- Field / domain: {field}
- Current skill level: {level}
- Total time available: {duration} {unit}
- Study time per week: {hours} hours

Structure the response exactly like this:

## Overview
A short summary of what the learner will achieve and the approach.

## Prerequisites
What to know before starting (write "None" for beginners if appropriate).

## Roadmap
Break the total time into phases (e.g., weeks or months). For each phase include:
- **Goal** of the phase
- **Topics to learn** (bullet list)
- **Hands-on practice / mini project**
- **Estimated hours**

## Recommended Resources
Free and paid courses, books, docs, or YouTube channels (well-known ones only).

## Capstone Project
One final project that proves the skills learned.

## Tips for Staying on Track
3-5 short, practical tips.

Make sure the plan fits within the time available and matches the skill level.
Do not repeat topics the learner already knows at their level."""


def stream_roadmap(client: Groq, prompt: str):
    """Yield text chunks from Groq so Streamlit can render them live."""
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.6,
        max_tokens=3000,
        stream=True,
    )
    for chunk in stream:
        text = chunk.choices[0].delta.content
        if text:
            yield text


def main() -> None:
    st.set_page_config(page_title="Learning Roadmap Generator", page_icon="🗺️", layout="centered")
    st.title("🗺️ Learning Roadmap Generator")
    st.caption("Tell me what you want to learn, and I'll build a plan that fits your time.")

    # ---- API key handling ----
    api_key = get_api_key()
    with st.sidebar:
        st.header("Settings")
        if not api_key:
            api_key = st.text_input("Groq API key", type="password", help="Get one free at console.groq.com")
        else:
            st.success("API key loaded")
        st.markdown(f"**Model:** `{MODEL}`")

    # ---- User inputs ----
    field = st.text_input("What do you want to learn?", placeholder="e.g., Data Science, Web Development, Guitar")

    level = st.selectbox("Your current level", ["Beginner", "Intermediate", "Advanced"])

    col1, col2 = st.columns(2)
    with col1:
        duration = st.number_input("Time to learn", min_value=1, max_value=60, value=3, step=1)
    with col2:
        unit = st.selectbox("Unit", ["weeks", "months"], index=1)

    hours = st.slider("Hours you can study per week", min_value=1, max_value=40, value=8)

    # ---- Generate ----
    if st.button("Generate Roadmap", type="primary", use_container_width=True):
        if not field.strip():
            st.warning("Please enter a field or topic first.")
            return
        if not api_key:
            st.error("Please provide a Groq API key in the sidebar.")
            return

        client = Groq(api_key=api_key)
        prompt = build_prompt(field.strip(), level, int(duration), unit, hours)

        try:
            st.divider()
            roadmap = st.write_stream(stream_roadmap(client, prompt))
            st.session_state["roadmap"] = roadmap
            st.session_state["filename"] = f"{field.strip().lower().replace(' ', '_')}_roadmap.md"
        except Exception as e:
            st.error(f"Something went wrong while contacting Groq: {e}")
            return

    # ---- Download ----
    if "roadmap" in st.session_state:
        st.download_button(
            "Download as Markdown",
            data=st.session_state["roadmap"],
            file_name=st.session_state["filename"],
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()
