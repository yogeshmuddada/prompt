# app.py
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Together
import os

# Set up Streamlit page config
st.set_page_config(
    page_title="Advanced Prompt Generator",
    page_icon="✨",
    layout="centered"
)

# UI Header
st.title("🧠 AI Prompt Enhancer")
st.markdown(
    "Convert your basic prompts into rich, structured, and actionable **advanced prompts** for Large Language Models (LLMs)."
)

# API Key Input (Optional — for secure handling)
together_api_key = st.text_input("🔐 Enter Your Together API Key", type="password")
if together_api_key:
    os.environ["TOGETHER_API_KEY"] = together_api_key

# Input Section
basic_prompt = st.text_area(
    "✍️ Enter a Basic Prompt",
    placeholder="e.g., Give me the code for the login page",
    height=150
)

# Button to generate
generate_button = st.button("🚀 Generate Advanced Prompt")

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
