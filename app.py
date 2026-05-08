import streamlit as st
from shoptalk_graph import shoptalk_app, AgentState  # أضفنا AgentState هنا
from database_utils import get_db_schema

# إعدادات الصفحة
st.set_page_config(page_title="ShopTalk Assistant", page_icon="🛒")
st.title("🛒 ShopTalk - SQL AI Assistant")
st.markdown("Ask any question about your database, and I will write the SQL, execute it, and give you the answer!")

# ذاكرة الشات (عشان يحتفظ بالأسئلة اللي فاتت)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسايل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# مربع الإدخال للمستخدم
if user_question := st.chat_input("Ex: What are the top 5 products?"):
    
    # طباعة سؤال المستخدم على الشاشة
    st.chat_message("user").markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    # تجهيز المدخلات للـ LangGraph
    schema = str(get_db_schema())
    
    # إرضاء المفتش بتحديد النوع هنا
    inputs: AgentState = {
        "question": user_question, 
        "schema": schema,
        "error": "none"
    }

    # تشغيل الذكاء الاصطناعي (مع علامة تحميل)
    with st.spinner("🤖 Thinking & Querying Database..."):
        final_state = shoptalk_app.invoke(inputs)
        bot_response = final_state.get('final_answer', 'Sorry, an error occurred.')

    # طباعة إجابة البوت على الشاشة
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})