import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("VSP Health Symptom Checker")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input for symptoms
user_input = st.chat_input("Describe your health issues here!!!!!!!!!!!")

# Function to get a response from OpenAI with health advice
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful and cautious medical assistant. You only answer questions related to health symptoms and general medical advice. If a user asks something outside of the medical domain, politely refuse and redirect them to focus on health-related concerns."}
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": prompt}]
    )
      # Access the content directly as an attribute
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_prompt = f"User has reported the following symptoms: {user_input}. Provide a general remedy or advice."
    assistant_response = get_response(assistant_prompt)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
