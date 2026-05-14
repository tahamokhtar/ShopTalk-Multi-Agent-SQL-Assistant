🛒 ShopTalk Pro - Multi-Agent SQL Assistant
ShopTalk Pro is an advanced AI system designed to enable non-technical users to interact with complex databases using Natural Language. 🗣️ Instead of writing complex SQL queries, the user asks normal questions, and the Multi-Agent System analyzes the intent, extracts the data, and automatically generates natural language insights alongside interactive charts. 📊✨

🚀 Technologies Used
Language: Python 🐍

LLM: Google Gemini 2.5 Flash (for rapid inference and high accuracy) 🧠

Orchestration: LangGraph (Multi-Agent System) 🕸️

Visualization: Plotly Express 📈

Database: SQLite 🗄️

UI: Streamlit 🖥️

🧠 Agent Architecture
The system relies on three specialized intelligent agents working collaboratively: 🤝

SQL Expert Agent: Analyzes the database schema and translates user questions into optimized, executable SQL queries. 🕵️‍♂️

Data Engineer Agent: Executes the queries on the database. It includes built-in Self-Correction capabilities to automatically detect and fix SQL syntax errors before returning results. 🛠️

Data Analyst Agent: Formats the raw database output into a human-readable natural language response and intelligently selects the most appropriate chart type to visualize the data. 📉

⚡ Advanced Features
GitHub Actions Caching: Configured a continuous integration pipeline with package caching, significantly reducing workflow build times and optimizing deployment efficiency. ⏱️

Interactive Visuals: Dynamically generated, transparent-background charts that adapt based on the context of the user's question. 🎨

Clean UI: A modern, responsive interface featuring status trackers and beautiful animations for a premium user experience. ✨

⚙️ How to Run Locally
Clone this repository to your local machine. 📥

Open your main agent Python file and insert your personal API key. 🔑

Install all the required dependencies listed in your requirements text file. 📦

Start the Streamlit application using your terminal to view the interface. 🚀

👨‍💻 Developer
Taha Mokhtar – Data Engineer 💼
Data Science, Badr University in Assiut (BUA) 🎓
