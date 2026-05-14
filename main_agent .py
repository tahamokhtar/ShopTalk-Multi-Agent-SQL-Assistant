import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from database_utils import get_db_schema

load_dotenv()

def run_sql_query(sql):
    """Function to execute the SQL query on the database."""
    try:
        conn = sqlite3.connect('shoptalk.db')
        # Execute the query and convert it to a pandas DataFrame
        result = pd.read_sql_query(sql, conn)
        conn.close()
        return result
    except Exception as e:
        return f"❌ Execution Error: {e}"

def get_sql_generator_chain():
    # مكتبة LangChain هتقرأ الـ GOOGLE_API_KEY تلقائياً من ملف .env
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0  # درجة حرارة صفر مهمة جداً هنا عشان توليد الـ SQL يكون دقيق ومفيهوش إبداع يكسر الـ Syntax
    )
    
    template = """
    You are an expert SQLite developer. Given the database schema below, 
    write a SQL query that answers the user's question.
    
    Database Schema:
    {schema}
    
    User Question:
    {question}
    
    Return ONLY the SQL query code. No backticks, no explanation.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    return prompt | llm

if __name__ == "__main__":
    print("🤖 ShopTalk Assistant is ready! Type 'exit' to quit.")
    
    schema = get_db_schema()
    chain = get_sql_generator_chain()
    
    while True:
        # أخذ السؤال من المستخدم مباشرة
        user_question = input("\n❓ Ask a question: ")
        
        # شرط لإيقاف البرنامج
        if user_question.lower() in ['exit', 'quit', 'q']:
            print("👋 Goodbye!")
            break
            
        print("⏳ Generating SQL...")
        generated_sql = chain.invoke({"schema": schema, "question": user_question}).content
        
        print(f"✅ Generated Code:\n{generated_sql}")
        
        print("\n📊 Database Result:")
        final_result = run_sql_query(generated_sql)
        
        print("-" * 30)
        print(final_result)
        print("-" * 30)