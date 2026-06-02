import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_groq(prompt):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def skill_agent(goal):

    prompt = f"""
    What skills are required for:
    {goal}

    Give bullet points.
    """

    return ask_groq(prompt)

def roadmap_agent(goal):

    prompt = f"""
    Create a 4-week roadmap for:
    {goal}
    """

    return ask_groq(prompt)


def interview_agent(goal):

    prompt = f"""
    Generate 10 interview questions for:
    {goal}

    Mix technical and behavioral questions.
    """

    return ask_groq(prompt)

def resume_agent(resume_text, goal):

    prompt = f"""
    You are a resume reviewer.

    Career Goal:
    {goal}

    Resume:
    {resume_text}

    Analyze:

    1. Strengths
    2. Weaknesses
    3. Missing Skills
    4. Resume Improvement Suggestions

    Give detailed feedback.
    """

    return ask_groq(prompt)

def planner_agent(mode, resume_uploaded):

    if mode == "Skills Analysis":
        return ["skills"]

    elif mode == "Roadmap Only":
        return ["roadmap"]

    elif mode == "Interview Prep":
        return ["interview"]

    elif mode == "Resume Review":
        return ["resume"]

    else:

        tasks = [
            "skills",
            "roadmap",
            "interview"
        ]

        if resume_uploaded:
            tasks.append("resume")

        return tasks

st.set_page_config(
    page_title="AI Career Coach",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 AI Career Coach")
st.markdown(
    "Get a personalized roadmap, interview prep, and resume feedback."
)

goal = st.text_input(
    "Enter your career goal"
)
mode = st.selectbox(
    "What do you need help with?",
    [
        "Complete Career Guidance",
        "Skills Analysis",
        "Roadmap Only",
        "Interview Prep",
        "Resume Review"
    ]
)
uploaded_file = st.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"]
)

if st.button("Generate"):

    tasks = planner_agent(
        mode,
        uploaded_file is not None
    )

    skills = None
    roadmap = None
    questions = None
    resume_feedback = None

    if "skills" in tasks:
        with st.spinner("Generating skills..."):
            skills = skill_agent(goal)

    if "roadmap" in tasks:
        with st.spinner("Generating roadmap..."):
            roadmap = roadmap_agent(goal)

    if "interview" in tasks:
        with st.spinner("Generating interview questions..."):
            questions = interview_agent(goal)

    if "resume" in tasks and uploaded_file:

        pdf_reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in pdf_reader.pages:

            text = page.extract_text()

            if text:
                resume_text += text

        with st.spinner("Analyzing resume..."):

            resume_feedback = resume_agent(
                resume_text,
                goal
            )

    if skills:
        with st.expander("📚 Required Skills", expanded=True):
            st.markdown(skills)

    if roadmap:
        with st.expander("🗺️ 4 Week Roadmap"):
            st.markdown(roadmap)

    if questions:
        with st.expander("🎤 Interview Questions"):
            st.markdown(questions)

    if resume_feedback:
        with st.expander("📄 Resume Analysis"):
            st.markdown(resume_feedback)
    
    report = ""

    if skills:
        report += "\n\n=== REQUIRED SKILLS ===\n"
        report += skills

    if roadmap:
        report += "\n\n=== ROADMAP ===\n"
        report += roadmap

    if questions:
        report += "\n\n=== INTERVIEW QUESTIONS ===\n"
        report += questions

    if resume_feedback:
        report += "\n\n=== RESUME ANALYSIS ===\n"
        report += resume_feedback

    if report:
        st.download_button(
            label="📥 Download Career Report",
            data=report,
            file_name="career_report.txt",
            mime="text/plain"
        )