import os
import csv
import queue
import threading
import streamlit as st
# replace this with your HF key
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = st.secrets["hf_token"]

# from embedchain import App
# app = App.from_config("mistral.yaml")
# with open("linksCSV.csv", "r+") as csvFile:
#     for row in csv.reader(csvFile):
#         print(row)
#         app.add(row[0], data_type="pdf_file")
# # app.add("https://en.wikipedia.org/wiki/Elon_Musk")
# print(app.query("A patient comes in with pathologic nipple discharge. What's the best imaging study to order? Please give me one."))
# # Answer: The net worth of Elon Musk today is $258.7 billion.


import os

import streamlit as st

from embedchain import App
from embedchain.helpers.callbacks import (StreamingStdOutCallbackHandlerYield,
                                          generate)



@st.cache_resource
def ec_app():
    app = App.from_config("mistral.yaml")
    with open("linksCSV.csv", "r+") as csvFile:
        for row in csv.reader(csvFile):
            print(row)
            app.add(row[0], data_type="pdf_file")
    return app

st.title("💬 Chatbot")
st.caption("🚀 An Embedchain app powered by Mistral!")
app = ec_app()
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """
        Hi! I'm a chatbot. I can answer questions and learn new things!\n
        Ask me anything and if you want me to learn something do `/add <source>`.\n
        I can learn mostly everything. :)
        """,
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything!"):

    # if prompt.startswith("/add"):
    #     with st.chat_message("user"):
    #         st.markdown(prompt)
    #         st.session_state.messages.append({"role": "user", "content": prompt})
    #     prompt = prompt.replace("/add", "").strip()
    #     with st.chat_message("assistant"):
    #         message_placeholder = st.empty()
    #         message_placeholder.markdown("Adding to knowledge base...")
    #         app.add(prompt)
    #         message_placeholder.markdown(f"Added {prompt} to knowledge base!")
    #         st.session_state.messages.append({"role": "assistant", "content": f"Added {prompt} to knowledge base!"})
    #         st.stop()

    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("Thinking...")
        full_response = ""

        answer, citation = app.chat(prompt, citations=True)

        full_response += answer

        if citation:
            full_response += "\n\n**Sources**:\n"
            urlSet = set()
            for i, citations in enumerate(citation):
                url = citations[1]['url']
                if url in urlSet:
                    continue
                full_response += f"{i+1}. {citations[1]['url']}\n"
                urlSet.add(url)

        msg_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


        # q = queue.Queue()

        # def app_response(result):
        #     print('in')
        #     answer, citations = app.chat(prompt,citations=True)
        #     result["answer"] = answer
        #     result["citations"] = citations

        # results = {}
        # thread = threading.Thread(target=app_response, args=(results,))
        # thread.start()

        # for answer_chunk in generate(q):
        #     full_response += answer_chunk
        #     msg_placeholder.markdown(full_response)

        # thread.join()
        # answer, citations = results["answer"], results["citations"]
        # if citations:
        #     full_response += "\n\n**Sources**:\n"
        #     for i, citations in enumerate(citations):
        #         full_response += f"{i+1}. {citations[1]}\n"

        # msg_placeholder.markdown(full_response)
        # st.session_state.messages.append({"role": "assistant", "content": full_response})