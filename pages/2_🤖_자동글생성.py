#from dotenv import load_dotenv
#load_dotenv()

import os
import streamlit as st
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="글 생성", page_icon="🤖")
st.title("글 자동생성")

# ① 사용자 입력: OpenAI API 키(비공개), 키워드
api_key = st.text_input("OpenAI API 키를 입력하세요", type="password", help="키는 세션에만 사용되고 저장되지 않습니다.")
content = st.text_input("키워드를 입력해주세요. 예: keyword1, keyword2")

# ② 모델 선택(옵션)
model_name = st.selectbox("모델 선택", ["gpt-4o-mini", "gpt-4o", "gpt-4o-mini-translate"], index=0)

# ③ 프롬프트 템플릿
base_prompt = """너는 최고의 블로그 글쓰기 전문가야. 너는 독자를 재미있게 끌어들이는 법을 잘 알고 있어.
내가 키워드를 주면 그 키워드를 바탕으로 '반드시' HTML 코드 형식으로만 글을 작성해줘.

요구사항:
1) 글을 시작하기 전에 간단한 소개(인트로)를 먼저 작성
2) 전체는 HTML 기반으로 작성
3) 최소 1200자 이상
4) 모든 문장은 한국어
5) <nav> 태그를 포함하고, 클릭 시 해당 섹션으로 이동하도록 앵커 구성
6) 각 섹션 내용은 <p> 태그로 상세하고 길게(한 단락 300자 이상)
7) 두 개 이상의 목록 태그(<ul> 또는 <ol>)를 사용해 섹션을 구성
8) 최종 출력은 '오직 HTML 코드'만

키워드: {keywords}
"""

# ④ 실행 버튼
if st.button("글 생성"):
    if not api_key:
        st.warning("먼저 OpenAI API 키를 입력해주세요.")
        st.stop()
    if not content.strip():
        st.warning("키워드를 입력해주세요.")
        st.stop()

    with st.spinner("글 생성 중..."):
        try:
            # ⑤ 모델 인스턴스는 키가 준비된 뒤에 생성
            chat_model = ChatOpenAI(
                model=model_name,
                temperature=0.2,
                api_key=api_key,
            )

            prompt = base_prompt.format(keywords=content.strip())
            # 최신 LangChain 스타일: invoke → AIMessage 반환, .content로 본문 꺼내기
            resp = chat_model.invoke(prompt)
            html_result = resp.content if hasattr(resp, "content") else str(resp)

            # ⑥ 결과 출력 (코드 블록으로 표시)
            st.code(html_result, language="html")

        except Exception as e:
            # Streamlit Cloud에선 민감정보 보호로 에러가 가려질 수 있음
            st.error("생성 중 오류가 발생했습니다. requirements 및 API 키 설정을 확인하세요.")
            st.exception(e)
