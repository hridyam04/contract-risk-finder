# Contract Risk Finder

A web app that lets users upload legal contracts (PDF) and automatically detects potentially risky clauses like indemnity, termination, penalties, non-compete, and more.

## 🔍 Features
- Upload contract PDFs
- Auto-highlight clauses with legal risks
- Explain each flagged clause in plain English

## 🚀 Built With
- Streamlit (Frontend)
- Python + PyMuPDF (PDF parser)
- Rule-based NLP for clause classification

## 📄 Try It Online

## 👩‍⚖️ Sample Input
_"The Employee shall indemnify the Company from all liabilities."_  
🛑 Flagged as: `indemnity`
