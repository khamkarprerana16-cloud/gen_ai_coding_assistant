import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="GenAI Coding Assistant")

st.title("GenAI Coding Assistant")

st.write(
    "Generate, explain, debug, and improve Python code "
    "using AI."
)

task = st.selectbox(
    "Select a task",
    [
        "Generate Code",
        "Explain Code",
        "Debug Code",
        "Optimize Code"
    ]
)

user_input = st.text_area(
    "Enter your prompt or code",
    height=200
)

if st.button("Submit"):

    if user_input.strip() == "":
        st.warning("Please enter a prompt or code.")

    else:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            try:
                api_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                api_key = None

        if not api_key:
            st.error(
                "API key not found. Add GROQ_API_KEY "
                "to your environment or app secrets."
            )

        else:
            if task == "Generate Code":
                instruction = (
                    "Generate simple, readable Python code "
                    "for this requirement:\n"
                )

            elif task == "Explain Code":
                instruction = (
                    "Explain the following code in simple "
                    "language, step by step:\n"
                )

            elif task == "Debug Code":
                instruction = (
                    "Find errors in the following code, "
                    "explain them, and provide corrected code:\n"
                )

            else:
                instruction = (
                    "Suggest improvements to this code. "
                    "Provide an improved version and explain "
                    "the changes:\n"
                )

            prompt = instruction + user_input

            try:
                client = Groq(api_key=api_key)

                with st.spinner("Generating response..."):
                    response = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.2
                    )

                st.subheader("AI Response")
                st.markdown(
                    response.choices[0].message.content
                )

            except Exception as e:
                st.error("Unable to generate a response.")
                st.write(str(e))
