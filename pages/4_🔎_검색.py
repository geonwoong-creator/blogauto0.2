import streamlit as st
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.callbacks import StreamlitCallbackHandler

# from dotenv import load_dotenv
# load_dotenv()


st.set_page_config(
    page_title="search",
    page_icon="🔎",
)



st.header("Search 🔎")
search_query = st.text_input("질문하기")


# if "messages" not in st.session_state:
#     st.session_state["messages"] = [
#         {"role": "assistant", "content": "안녕하세요. 저는 웹 검색이 가능한 챗봇입니다. 무엇을 도와드릴까요?"}
#     ]

# # if "messages" not in st.session_state:
# #     st.chat_message["messages"] = [
# #         {"role": "assistant", "content": "안녕하세요. 저는 웹 검색이 가능한 챗봇입니다. 무엇을 도와드릴까요?"}
# #     ]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input(placeholder="지금 대한민국 대통령은 누구야?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
    
#     with st.chat_message("assistant"):
#         st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
#         llm = OpenAI(temperature=0)
#         tool_name = ["serpapi"]
#         tools = load_tools(tool_name)
#         agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
#         response = agent.run(st.session_state.messages, callbacks=[st_cb])
#         st.session_state.messages.append({"role": "assistant", "content": response})
#         st.write(response)


if st.button("질문하기"):
    if not search_query.strip():
        st.write(f"질문을 입력해주세요.")
    else :
        try:
            # Initialize the OpenAI module, load the SerpApi tool, and run the search query using an agent
            llm=OpenAI(temperature=0,verbose=True)
            tools = load_tools(["serpapi"], llm)
            agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

            result = agent.run(search_query)
            
            st.write(result)
        except Exception as e:
            st.write(f"An error occurred: {e}")






