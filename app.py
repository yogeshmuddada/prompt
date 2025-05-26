import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Together
import os

# ✅ Set up Streamlit page config FIRST
st.set_page_config(
    page_title="Advanced Prompt Generator",
    page_icon="✨",
    layout="centered"
)

# ✅ Inject custom CSS
st.markdown(
    """
    <style>
    /* Background gradient for main app view */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #f0f0f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 2rem 5rem;
    }

    /* Header */
    h1 {
        text-align: center;
        color: white;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.4);
    }

    /* Text input areas */
    textarea {
        background: rgba(255, 255, 255, 0.85) !important;
        color: #333 !important;
        border-radius: 8px !important;
        padding: 10px !important;
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

# ✅ API key (Optional: can be secured using st.secrets)
os.environ["TOGETHER_API_KEY"] = "c727254c1132b1093dfecea29ea394acbb6deb3c958619036b79fff9bb44804f"

# ✅ Prompt input
basic_prompt = st.text_area(
    "📝 Enter a Basic Prompt",
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

                # Output
                st.markdown("### 🎯 Enhanced Prompt")
                st.text_area("Result", value=result["text"], height=300)

        except Exception as e:
            st.error(f"❌ Error: {e}")
