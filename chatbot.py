import streamlit as st
from openai import AzureOpenAI

azure_api_key = "api_key"
azure_endpoint = "endpoint"
deployment_id = "gpt_model"  
api_version = "api_version"

client = AzureOpenAI(
    api_key=azure_api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint,
)

st.set_page_config(page_title="Electronics Support Chatbot", page_icon="💬")
st.title("🤖 Electronics Support Chatbot")
st.write("Ask questions related to smartphones, laptops, order tracking, warranty, and more.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful customer support assistant for an electronics store. "
                "Answer only electronics-related questions such as product specifications, order tracking, returns, "
                "payment options, and warranties. Politely decline irrelevant questions."
            )
        }
    ]

for msg in st.session_state.messages[1:]:  # skip system prompt
    if msg["role"] == "user":
        st.markdown(f"**👤 You:** {msg['content']}")
    else:
        st.markdown(f"**🤖 Bot:** {msg['content']}")

user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Generating reply..."):
        response = client.chat.completions.create(
            messages=st.session_state.messages,
            model=deployment_id,
            temperature=0.7,
            max_tokens=1000,
            top_p=1.0
        )
        bot_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()
