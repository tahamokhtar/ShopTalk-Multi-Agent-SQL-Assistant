import os
import warnings

# 🛑 1. إغلاق جميع التحذيرات المزعجة من جذور النظام
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import plotly.express as px
from shoptalk_graph import shoptalk_app, AgentState
from database_utils import get_db_schema
import time
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# إعدادات الصفحة
st.set_page_config(page_title="ShopTalk Pro", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# الشريط الجانبي
with st.sidebar:
    lottie_ai = load_lottieurl("https://lottie.host/80131ee6-0567-4a0b-ae93-f11181f01633/K782aW34h7.json")
    if lottie_ai:
        st_lottie(lottie_ai, height=150, key="ai_animation")
        
    st.title("⚙️ ShopTalk Pro")
    st.caption("Powered by Gemini 2.5 Flash & LangGraph")
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    with st.expander("📄 View Database Schema"):
        st.code(get_db_schema(), language="sql")
        
    st.divider()

st.title("🛒 ShopTalk - AI Data Analyst")
st.markdown("Ask anything about your business data, and get instant answers & visualizations.")

@st.cache_data(ttl=3600)  # الكاش هيتجدد كل ساعة
def get_cached_schema():
    return str(get_db_schema())

if "messages" not in st.session_state:
    st.session_state.messages = []

# استخدمنا enumerate عشان نطلع رقم (i) لكل رسالة ونستخدمه كـ Key
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sql" in message:
            with st.expander("🛠️ View SQL & Raw Data"):
                st.code(message["sql"], language="sql")
                if "df" in message:
                    st.dataframe(message["df"], use_container_width=True)
        if "fig" in message:
            # 👇 التعديل هنا: ضفنا key=f"history_chart_{i}"
            st.plotly_chart(message["fig"], use_container_width=True, key=f"history_chart_{i}")

if user_question := st.chat_input("Ex: Show me a histogram of product prices..."):
    
    # 🚪 أمر الخروج الذكي
    if user_question.strip().lower() in ["اطلع", "خروج", "exit", "quit", "برا"]:
        st.chat_message("user").markdown(user_question)
        st.chat_message("assistant").markdown("👋 **أشوفك على خير يا هندسة!**\n\n*(السيستم تم إيقافه، اضغط `Ctrl + C` في الـ Terminal لإغلاق السيرفر بالكامل)*")
        st.stop()

    st.chat_message("user").markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    schema = get_cached_schema()
    inputs: AgentState = {"question": user_question, "schema": schema, "error": "none"}

    with st.chat_message("assistant"):
        with st.status("🧠 Processing your request...", expanded=True) as status:
            st.write("🕵️‍♂️ Agent 1: Generating optimized SQL query...")
            final_state = shoptalk_app.invoke(inputs)            
            st.write("⚙️ Agent 2: Executing query on database...")
            time.sleep(0.2)
            
            st.write("📊 Agent 3: Analyzing results & rendering visuals...")
            time.sleep(0.2)
            status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

        bot_response = final_state.get('final_answer', 'I couldn\'t process that.')
        sql_query = final_state.get('sql_query', '-- No SQL generated')

        # 1. عرض الإجابة النصية للذكاء الاصطناعي
        st.markdown(bot_response)
        
        # 2. استخراج الـ DataFrame فوراً من الـ SQL عشان نرسمها
        df = None
        if "SELECT" in sql_query.upper():
            try:
                import sqlite3
                conn = sqlite3.connect('shoptalk.db')
                df = pd.read_sql_query(sql_query, conn)
                conn.close()
            except Exception:
                pass

        # 3. عرض الـ SQL والجدول في الـ Expander زي ما طلبت (بدون المساس بالديزاين)
        with st.expander("🛠️ View SQL & Raw Data"):
            st.code(sql_query, language="sql")
            if df is not None and not df.empty:
                st.dataframe(df, use_container_width=True)
        
        # 4. نظام ذكي لرسم البيانات تلقائياً وعرضها تحت الإجابة مباشرة
        fig = None
        # لو النتيجة فيها عمودين أو أكتر، هنرسمها تلقائياً
        if df is not None and not df.empty and len(df.columns) >= 2:
            cols = df.columns
            x_col = cols[0]
            y_col = cols[1]
            
            # استنتاج نوع الرسمة من كلمات اليوزر، أو اختيار Bar كافتراضي
            ai_chart = "bar" 
            q_lower = user_question.lower()
            if any(w in q_lower for w in ["pie", "دائرة", "نسبة", "توزيع"]):
                ai_chart = "pie"
            elif any(w in q_lower for w in ["line", "trend", "تاريخ", "شهر", "يوم", "زمن"]):
                ai_chart = "line"
            elif any(w in q_lower for w in ["scatter", "تبعثر"]):
                ai_chart = "scatter"
            elif any(w in q_lower for w in ["area", "مساحة"]):
                ai_chart = "area"

            try:
                custom_colors = px.colors.qualitative.Prism
                pie_colors = px.colors.qualitative.Pastel

                if ai_chart == "bar":
                    fig = px.bar(df, x=x_col, y=y_col, color=x_col, color_discrete_sequence=custom_colors)
                elif ai_chart == "pie":
                    fig = px.pie(df, names=x_col, values=y_col, hole=0.4, color_discrete_sequence=pie_colors)
                elif ai_chart == "line":
                    fig = px.line(df, x=x_col, y=y_col, markers=True, color_discrete_sequence=[custom_colors[1]])
                elif ai_chart == "scatter":
                    fig = px.scatter(df, x=x_col, y=y_col, color=x_col, color_discrete_sequence=custom_colors)
                elif ai_chart == "area":
                    fig = px.area(df, x=x_col, y=y_col, color_discrete_sequence=[custom_colors[2]])

                if fig:
                    fig.update_layout(
                        title_text=f"<b>📊 Data Visualization</b>",
                        title_font=dict(size=18, family="Arial", color="#1f77b4"),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=20, r=20, t=50, b=20),
                        xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=True, gridcolor='lightgray')
                    )
                    # عرض الرسمة هنا (بره الـ Expander) عشان تظهر تحت الرد مباشرة
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            except Exception:
                pass

    # حفظ الرسالة بالرسمة والبيانات في الـ History عشان تفضل موجودة
    msg_data = {"role": "assistant", "content": bot_response, "sql": sql_query}
    if df is not None: msg_data["df"] = df
    if fig is not None: msg_data["fig"] = fig
    
    st.session_state.messages.append(msg_data)