from logging import disable
import streamlit as st
import time
from bookerReaderModule import BookerReaderModule

bookReader = BookerReaderModule()

if "url_exist" not in st.session_state:
    st.session_state.url_exist = None
if "use_url" not in st.session_state:
    st.session_state.use_url = False

st.title("RAGy Chatbot")

# # After getting URL from user it process URL and will show progress here. NOTE: will be manage from document loading class
def show_progress_bar():
    progress_text = "Processing URL, Please wait!"
    # print(f"{progress_text} {st.session_state.load_file_progress_disabled}")
    progress_container = st.empty()
    my_bar = progress_container.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    st.info("File has been processed")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {"role": "assistant", "content": "Hi, how can I assist you today?"})

    # Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message QA Chatbot..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

    query = [msg["content"]
             for msg in st.session_state.messages if msg["role"] == "user"][-1].lower()

    # Process Query here and get response
    if st.session_state.url_exist == None:
        url = bookReader.check_if_url_contains(query)
        if url:
            st.session_state.url_exist = url

    # print("this is the line", st.session_state.use_url,st.session_state.url_exist)
    if st.session_state.url_exist and "yes" in query.lower().split(" "):
        print("st.session_state.url_exist -> ", st.session_state.url_exist)
        bookReader.preProcessDataIndexing(fileType="WEBURL", fileURL=st.session_state.url_exist)
        show_progress_bar()
        st.session_state.use_url = False
        st.session_state.url_exist = None
        assistant_response = "Processing URL"
    elif st.session_state.url_exist and "no" in query.lower().split(" "):
        st.session_state.use_url = False
        st.session_state.url_exist = None
        assistant_response = "Anything else I can do for you?"
    elif st.session_state.url_exist:
        assistant_response = f"Do you want to talk about \"{st.session_state.url_exist}\""
        st.session_state.use_url = True
    # print("this is the line", st.session_state.use_url,st.session_state.url_exist)
    else:
        assistant_response = "Process Query"
        assistant_response = bookReader.process_user_query(query)
        print(assistant_response)
        if st.session_state.url_exist:
            st.session_state.url_exist = None

    # # Simulate stream of response with milliseconds delay
    if "\n" in assistant_response:
        for chunk in assistant_response.split("\n"):
            for item in chunk.split():
                full_response += item + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            full_response += "\n"
    else:
        for item in assistant_response.split():
            full_response += item + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")

    message_placeholder.markdown(assistant_response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})
