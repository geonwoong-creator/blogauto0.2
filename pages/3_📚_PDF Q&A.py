import os
import streamlit as st
from PyPDF2 import PdfReader

# ✅ v0.2+ 권장 임포트
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs or []:
        reader = PdfReader(pdf)
        for page in reader.pages:
            # 일부 PDF는 extract_text()가 None을 반환할 수 있음 → 방어 코드
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    return text


def get_text_chunks(text: str):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    return splitter.split_text(text)


def get_vectorstore(text_chunks, openai_api_key: str):
    embeddings = OpenAIEmbeddings(
        api_key=openai_api_key,
        model="text-embedding-3-small",
    )
    return FAISS.from_texts(texts=text_chunks, embedding=embeddings)


def get_conversation_chain(vectorstore, openai_api_key: str):
    llm = ChatOpenAI(
        api_key=openai_api_key,
        model="gpt-4o-mini",
        temperature=0.2,
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )
    return chain


def handle_userinput(user_question: str):
    if not st.session_state.conversation:
        st.warning("먼저 PDF를 업로드하고 ‘Process’를 눌러 벡터스토어를 생성하세요.")
        return

    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response.get("chat_history", [])

    for i, message in enumerate(st.session_state.chat_history):
        role = "user" if i % 2 == 0 else "ai"
        with st.chat_message(role):
            st.write(message.content)


def main():
    st.set_page_config(page_title="PDF Q&A", page_icon="📚")
    st.header("PDF Q&A 📚")

    # 🔐 API 키 입력(Secrets → 환경변수 순 → 입력창)
    sidebar_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")
    env_key = os.getenv("OPENAI_API_KEY")
    secrets_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None
    openai_api_key = sidebar_key or secrets_key or env_key

    if not openai_api_key:
        st.info("계속하려면 OpenAI API 키를 입력하거나 Secrets/환경변수에 설정하세요.")

    # 세션 상태 초기화
    st.session_state.setdefault("conversation", None)
    st.session_state.setdefault("chat_history", [])

    # 질문 입력
    user_question = st.text_input("PDF에 질문하기:")
    if user_question:
        handle_userinput(user_question)

    # 사이드바: PDF 업로드 & 처리
    with st.sidebar:
        st.subheader("PDF 파일")
        pdf_docs = st.file_uploader(
            "PDF를 업로드하고 ‘Process’를 누르세요",
            type=["pdf"],
            accept_multiple_files=True
        )
        if st.button("Process"):
            if not openai_api_key:
                st.warning("먼저 OpenAI API 키를 입력하세요.")
                st.stop()
            if not pdf_docs:
                st.warning("PDF 파일을 업로드하세요.")
                st.stop()

            with st.spinner("Processing..."):
                # 1) PDF 텍스트 추출
                raw_text = get_pdf_text(pdf_docs)
                if not raw_text.strip():
                    st.error("PDF에서 텍스트를 추출하지 못했습니다. 스캔본/이미지 PDF일 수 있어요.")
                    st.stop()

                # 2) 청크 분할
                chunks = get_text_chunks(raw_text)

                # 3) 벡터스토어 생성
                vectorstore = get_vectorstore(chunks, openai_api_key)

                # 4) 대화 체인 구성
                st.session_state.conversation = get_conversation_chain(vectorstore, openai_api_key)

                st.success("준비 완료! 이제 질문을 입력해보세요.")


if __name__ == "__main__":
    main()
