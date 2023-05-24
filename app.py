# Streamlit : UI -> 파이썬, run ->streamlit run app.py
import streamlit as st
import openai as op

# .streamlit에서 가져옴 (API키 보안)
op.api_key = st.secrets["api_key"]

st.title("ChatGPT & DELL-E")
st.text(" Prompt에 표현하면 ChatGPT가 구상하고 DALL-E는 그 생각을 이미지로 변환하여 드립니다.")

with st.form("form"):
    user_input = st.text_input("Prompt")
    size = st.selectbox("이미지 크기", ["1024x1024", "512x512", "256x256"])
    submit = st.form_submit_button("제출")

# submit을 누르고 user_input에 텍스트가 있을 떄
if submit and user_input: 
    gpt_prompt = [{
        "role" : "system", # 역활
        "content" : "Imagine the detail appareance of the input. Response it shortly around 20 words." # 명령
    }]

    gpt_prompt.append({
        "role" : "user", # 역활
        "content" : user_input # 명령 = 인풋내용
    })


    # 요청 로딩시 스피너
    with st.spinner("ChatGPT.. 잠시만 기다려주세요..."): 
        # op의 ChatCompletionAPI 사용 
        gpt_response = op.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = gpt_prompt
        )
    
    # gpt_response -> 문서 확인해보기
    # Access the prompt from gpt_response
    prompt = gpt_response["choices"][0]["message"]["content"]
    st.write(prompt)

    # DALL-E -> 문서 확인해보기
    # DALL-E 이미지 생성 요청
    with st.spinner("DALL-E.. 잠시만 기다려주세요..."):
        dalle_response = op.Image.create(
            prompt = prompt,
            size = size
        )
    st.image(dalle_response["data"][0]["url"])