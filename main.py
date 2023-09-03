import streamlit as st
from text_generation import Client



def main():
    st.title("LLM Condense 🤖")
    client = Client(base_url="http://127.0.0.1:8080", timeout=99)

    # Get user input
    user_input = st.text_area("Enter some text here:")

    stream = st.toggle(
        label="Stream response",         
        value=False, 
        key=None, 
        help="Toggle if you prefer the response to be streamed.", 
        on_change=None, 
        disabled=True, 
        label_visibility="visible"
        )


    if stream:
        if user_input:
            if st.button(label="Generate summary!", disabled=False):
                text = ""
                for response in client.generate_stream(
                    prompt="Summarize the following text: '''{user_input}'''", 
                    max_new_tokens=512,
                    temperature=0.1,
                    seed=123,
                    ):
                    if not response.token.special:
                        text += response.token.text
                        st.write(text)  #TODO: Fix output when streaming
                # st.write(response)
    else:
        if user_input:
            if st.button(label="Generate summary!", disabled=False):
                response = client.generate(
                    prompt=f"Summarize the following text: '''{user_input}'''", 
                    max_new_tokens=256,
                    temperature=0.1,
                    seed=123,
                    ).generated_text
                st.write(response)


if __name__ == "__main__":
    st.set_page_config(
        page_title="LLM Condense",
        page_icon="🤖",
        initial_sidebar_state="expanded",
        layout="wide",
    )
    main()