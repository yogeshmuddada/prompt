# app.py
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Together
import os

st.markdown(
    """
    <style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #f0f0f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        min-height: 100vh;
        padding: 2rem 5rem;
    }

    /* Title style */
    .title {
        font-size: 3rem;
        font-weight: 700;
        color: #fff;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.4);
    }

    /* Subtitle/description */
    .subtitle {
        font-size: 1.25rem;
        color: #ddd;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }

    /* Input and output boxes */
    .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.85);
        color: #333;
        border-radius: 8px;
        padding: 10px;
        font-size: 1.1rem;
    }

    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.85);
        color: #333;
        border-radius: 8px;
        padding: 10px;
        font-size: 1.1rem;
    }

    .stButton>button {
        background-color: #6c63ff;
        color: white;
        font-size: 1.25rem;
        padding: 10px 25px;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        transition: background-color 0.3s ease;
        margin-top: 1rem;
    }

    .stButton>button:hover {
        background-color: #5848c2;
        cursor: pointer;
    }

    /* Result text area */
    .result-textarea textarea {
        background: rgba(0, 0, 0, 0.7);
        color: #fff;
        font-family: monospace;
        font-size: 1rem;
        border-radius: 8px;
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Set up Streamlit page config
st.set_page_config(
    page_title="Advanced Prompt Generator",
    page_icon="✨",
    layout="centered"
)

# UI Header
st.title("AI Prompt Enhancer")
st.markdown(
    "Convert your basic prompts into rich, structured, and actionable **advanced prompts** for Large Language Models (LLMs)."
)

# API Key Input (Optional — for secure handling)
os.environ["TOGETHER_API_KEY"] = "c727254c1132b1093dfecea29ea394acbb6deb3c958619036b79fff9bb44804f"

# Input Section
basic_prompt = st.text_area(
    "Enter a Basic Prompt",
    placeholder="e.g., Give me the code for the login page",
    height=150
)

# Button to generate
generate_button = st.button("🤔Generate Advanced Prompt")

# LangChain Setup
if generate_button:
    if not together_api_key:
        st.warning("⚠️ Please enter your Together API Key.")
    elif not basic_prompt.strip():
        st.warning("⚠️ Please enter a basic prompt.")
    else:
        # Initialize LLM
        try:
            llm = Together(
                model="meta-llama/Llama-3-8b-chat-hf",
                temperature=0.7,
                max_tokens=1024,
            )

            # Prompt Template
            prompt_template = PromptTemplate(
                input_variables=["basic_prompt"],
                template="""
You are a senior AI prompt engineer. Your task is to convert the following basic user prompt into a rich, structured, and actionable advanced prompt suitable for large language models or AI agents.

Make sure the enhanced prompt is detailed, clear, and focused.

Include (based on context):
1. Objective
2. Context or Background
3. Expected Output
4. Subtasks or Questions to Explore
5. Tools, Tech, or Resources to Consider
6. Relevant Examples
7. Best Practices for Understanding or Implementation

Basic Prompt: {basic_prompt}

Advanced Prompt:
"""
            )

            # Chain
            chain = LLMChain(llm=llm, prompt=prompt_template)

            # Run
            with st.spinner("🔄 Enhancing your prompt..."):
                result = chain.invoke({"basic_prompt": basic_prompt})
                st.success("✅ Prompt Enhanced Successfully!")

                # Display result
                st.markdown("### ✨ Enhanced Prompt")
                st.text_area("Result", value=result["text"], height=300)

        except Exception as e:
            st.error(f"❌ Error occurred: {e}")
