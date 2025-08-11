#from dotenv import load_dotenv
#load_dotenv()

from langchain_openai import ChatOpenAI
import streamlit as st

chat_model = ChatOpenAI()

st.set_page_config(
    page_title="글 생성",
    page_icon="🤖",
)



st.title('글 자동생성')

content = st.text_input('키워드를 입력해주세요. EX(keyword1,keyword2,)')

if st.button('글 생성'):
    with st.spinner('글 생성 중.....'):
        result = chat_model.predict("너는 최고의 블로그 글쓰기 전문가야. 너는 독자를 어떻게하면 재미있게 할수있는 알고있어. 내가 키워드를 주면 키워드를 바탕으로  html코드 형식으로 글를 써줄꺼야. 무조건 html형식으로 만들어줘 글을 쓸때 내가 알려주는 조건에 맞춰서 써줘 1. 글을 쓰기 전에, 글에 대한 간단한 소개를 먼저 적으세요. 2.게재된 기사는 HTML을 기반으로 합니다. 3. 1200자 이상을 만족합니다. 4. 모든 것을 한국어로 써주세요 5. <nav> 태그를 넣고 클릭한 후 이동합니다 6. <p>tag를 사용하여 섹션의 내용을 최대한 상세하고 길게 작성합니다. 7. 두 개 이상의 목록 태그를 사용하여 섹션을 구성합니다. 8. <p>tag로 쓰기는 300자 이상이어야 합니다. 9.html코드만 알려줘 키워드:" + content)
        st.code(result, language='cshtml')


