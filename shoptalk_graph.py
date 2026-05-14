import os
import sqlite3
import langchain_community
import pandas as pd
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

# --- التعديلات الجديدة للـ API والـ Caching ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from database_utils import get_db_schema

load_dotenv()

# تفعيل الـ LLM Caching في ملف قاعدة بيانات منفصل
set_llm_cache(SQLiteCache(database_path="llm_cache.db"))

# إعداد Gemini 3.0 Flash 
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key="AIzaSyBcfW-6BSTfIJI5SsEY54I6bRqvzt0fN-s",
    temperature=0  # درجة حرارة صفر مهمة جداً هنا عشان توليد الـ SQL يكون دقيق ومفيهوش إبداع يكسر الـ Syntax
)

# ... (باقي كود الـ AgentState والـ Nodes زي ما هو بدون تغيير) ...
class AgentState(TypedDict, total=False): 
    question: str
    schema: str
    sql_query: str
    db_result: str
    error: str
    final_answer: str

def generate_sql_node(state: AgentState):
    print("-> [Agent 1] Generating/Fixing SQL...")
    schema = state.get("schema", "")
    question = state.get("question", "")
    error = state.get("error", "none")
    
    if error != "none":
        prompt = f"Fix this SQL error: {error}. Schema:\n{schema}\nQuestion: {question}\nReturn ONLY SQL."
    else:
        prompt = f"Write a SQL query for this schema:\n{schema}\nQuestion: {question}\nReturn ONLY the SQL query code. No backticks."
        
    response = llm.invoke(prompt)
    
    raw_content = str(response.content)
    sql = raw_content.replace('```sql', '').replace('```', '').strip()
    
    return {"sql_query": sql}

def execute_sql_node(state: AgentState):
    print("-> [Agent 2] Executing SQL in SQLite...")
    sql = state.get("sql_query", "")
    try:
        conn = sqlite3.connect('shoptalk.db')
        result = pd.read_sql_query(sql, conn)
        conn.close()
        return {"db_result": result.to_string(), "error": "none"}
    except Exception as e:
        print(f"   [!] Error found: {e} -> Sending back to Agent 1")
        return {"error": str(e)}

def generate_response_node(state: AgentState):
    print("-> [Agent 3] Formulating final response...")
    question = state.get("question", "")
    db_result = state.get("db_result", "")
    
    prompt = f"The user asked: '{question}'. The database returned this raw data:\n{db_result}\nWrite a clear, short, and natural response answering the user directly."
    response = llm.invoke(prompt)
    
    return {"final_answer": str(response.content)}

def check_for_errors(state: AgentState):
    if state.get("error", "none") != "none":
        return "needs_fix"
    return "all_good"

# --- بناء المعمارية (The Graph) ---
workflow = StateGraph(AgentState)

workflow.add_node("sql_generator", generate_sql_node)
workflow.add_node("db_executor", execute_sql_node)
workflow.add_node("response_generator", generate_response_node)

workflow.set_entry_point("sql_generator")
workflow.add_edge("sql_generator", "db_executor")
workflow.add_conditional_edges(
    "db_executor",
    check_for_errors,
    {
        "needs_fix": "sql_generator",
        "all_good": "response_generator"
    }
)
workflow.add_edge("response_generator", END)

shoptalk_app = workflow.compile()

# --- التشغيل ---
if __name__ == "__main__":
    print("🕸️ Starting ShopTalk LangGraph Architecture...\n")
    
    schema = str(get_db_schema())
    
    # 2. إرضاء Pylance بتحديد نوع القاموس صراحة
    inputs: AgentState = {
        "question": "What is the total revenue?", 
        "schema": schema,
        "error": "none"
    }
    
    final_state = shoptalk_app.invoke(inputs)
        
    print("\n✅ Final Output:")
    print(final_state.get('final_answer', 'No answer generated.'))