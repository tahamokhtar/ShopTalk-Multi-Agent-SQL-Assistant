# ShopTalk-Multi-Agent-SQL-Assistant
ShopTalk is an advanced AI system designed to enable non-technical users to interact with complex databases using Natural Language. Instead of writing complex SQL queries, the user asks normal questions, and the Multi-Agent System analyzes the question, extracts the data, and automatically generates reports and charts
# 🛒 ShopTalk - Multi-Agent SQL Assistant

ShopTalk is an intelligent SQL assistant built with a Multi-Agent architecture. It translates natural language questions into executable SQL queries, runs them against a database, and returns human-readable insights.

## 🚀 Technologies Used
* **Language:** Python
* **LLM:** Groq (Llama-3.3-70b-versatile) for rapid inference
* **Architecture:** LangGraph (Multi-Agent System)
* **Database:** SQLite
* **UI:** Streamlit

## 🧠 Agent Architecture
1. **SQL Generator:** Translates user questions into SQL.
2. **Execution Agent:** Runs the query on SQLite. Includes self-correction capabilities if a SQL error occurs.
3. **Response Agent:** Formats raw database output into a natural language response.

## ⚙️ How to Run Locally
1. Clone this repository.
2. Create a `.env` file and add your `GROQ_API_KEY`.
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `python -m streamlit run app.py`
