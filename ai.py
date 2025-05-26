pip install langchain
pip install langchain-community
pip install together
pip install openai
pip install pydantic

from langchain.llms import Together
print("✅ All modules imported successfully!")

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import Together
import os

# ✅ Set your Together API key
os.environ["TOGETHER_API_KEY"] = "c727254c1132b1093dfecea29ea394acbb6deb3c958619036b79fff9bb44804f"  # replace with your actual key

# ✅ Use a supported model
llm = Together(
    model="meta-llama/Llama-3-8b-chat-hf",
    temperature=0.7,
    max_tokens=1024,
)

# ✅ Define the prompt

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

# ✅ Create the chain
prompt_chain = LLMChain(llm=llm, prompt=prompt_template)

# ✅ Try invoking the chain
simple_prompt = input("Give me the code for the login page")
try:
    result = prompt_chain.invoke({"basic_prompt": simple_prompt})
    print("🔹 Enhanced Prompt:\n")
    print(result["text"])
except Exception as e:
    print("❌ Error:", e)
