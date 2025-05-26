import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Together
from streamlit.components.v1 import html
import os

# ✅ Set up Streamlit page config FIRST
st.set_page_config(
    page_title="Advanced Prompt Generator",
    page_icon="✨",
    layout="centered"
)

# ✅ Inject custom CSS for dark theme + UI styling
st.markdown(
    """
    <style>
    /* App background */
    [data-testid="stAppViewContainer"] {
        background-color: #1e1e2f;
        color: #f0f0f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 2rem 5rem;
    }

    h1 {
        text-align: center;
        color: #ffffff;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.4);
    }

    /* Label for text area */
    label[data-testid="stTextAreaLabel"] {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1.15rem;
        margin-bottom: 0.5rem;
    }

    /* Textarea styling */
    textarea {
        background-color: #2d2d44 !important;
        color: #f2f2f2 !important;
        border: 1px solid #4a4a6a !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 1.1rem !important;
    }

    /* Buttons */
    button {
        background-color: #6c63ff !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 10px 25px !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600;
    }

    button:hover {
        background-color: #5848c2 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Header
st.title("✨ AI Prompt Enhancer")
st.markdown(
    "Convert your basic prompt into a structured, detailed, and actionable **advanced prompt** suitable for AI agents or LLMs."
)

# ✅ API key (Optional: better to store in st.secrets or environment in production)
os.environ["TOGETHER_API_KEY"] = "c727254c1132b1093dfecea29ea394acbb6deb3c958619036b79fff9bb44804f"

# ✅ Prompt input
basic_prompt = st.text_area(
    "📝 Enter Your Prompt",
    placeholder="e.g., Give me the code for the login page",
    height=150
)

# ✅ Button to generate
if st.button("🚀 Generate Advanced Prompt"):
    if not os.environ.get("TOGETHER_API_KEY"):
        st.warning("⚠️ Please enter your Together API key.")
    elif not basic_prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
    else:
        try:
            # Load LLM
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

            # Run chain
            with st.spinner("🔄 Enhancing your prompt..."):
                result = chain.invoke({"basic_prompt": basic_prompt})
                st.success("✅ Prompt Enhanced Successfully!")

                # ✅ Markdown-styled output and copy button
                st.markdown("### 🎯 Enhanced Prompt")

                html(f"""
                <div style="margin-top: 1rem; background-color: #2d2d44; border-radius: 10px; padding: 1rem; color: white; font-family: monospace; position: relative;">
                    <button onclick="navigator.clipboard.writeText(document.getElementById('copy-target').innerText)"
                        style="position: absolute; top: 10px; right: 10px; background-color: #6c63ff; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-weight: bold; cursor: pointer;">
                        📋 Copy
                    </button>
                    <pre id="copy-target" style="white-space: pre-wrap;">{result['text']}</pre>
                </div>
                """, height=350)

        except Exception as e:
            st.error(f"❌ Error: {e}")
