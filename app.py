import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd
import io


# Risk rules and explanations
risky_keywords = {
    "termination": ["terminate", "termination", "notice period"],
    "indemnity": ["indemnify", "hold harmless", "liabilities"],
    "penalty": ["penalty", "damages", "compensation"],
    "non-compete": ["non-compete", "restrict", "competition"],
    "confidentiality": ["confidential", "non-disclosure", "disclose"]
}

explanations = {
    "termination": " May allow early contract ending.",
    "indemnity": " Could make you responsible for damages.",
    "penalty": " Might impose extra charges for violations.",
    "non-compete": " Can limit your future job options.",
    "confidentiality": " Restricts sharing of information."
}

# PDF extractor
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

# Detect risky phrases
def detect_risks(clause):
    found = []
    for tag, keywords in risky_keywords.items():
        if any(kw in clause.lower() for kw in keywords):
            found.append(tag)
    return found



# --- Streamlit App ---
st.set_page_config(page_title="Contract Risk Finder", layout="centered")
st.title("📜 Contract Risk Finder")
st.caption("Upload a contract PDF to auto-detect risky legal clauses.")

uploaded = st.file_uploader("📂 Upload your contract (.pdf)", type="pdf")

if uploaded:
    text = extract_text_from_pdf(uploaded)
    clauses = re.split(r'(?<=\.)\s+(?=[A-Z])', text)

    st.markdown("---")
  
    flagged_data=[]
    for clause in clauses:
        risks = detect_risks(clause)
        if risks:
            with st.container():
                st.markdown("### ⚠️ Risky Clause Detected")
                st.markdown(f"""
                    <div style="background-color:#f9f9f9; border-left: 4px solid #ff4b4b; padding: 1em; margin: 1em 0;">
                        <blockquote style="margin: 0; font-style: italic; color:#A20D0D;">"{clause.strip()}"</blockquote>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
    <div style="background-color:#ADADC3; border: 1px solid #ffeeba; 
                padding: 0.75em; border-radius: 8px; margin-bottom: 1em;
                color: #000000;">
        <b>Risks Detected:</b> {', '.join(risks)}<br><br>
        {"<br>".join(f"⚠️ {explanations[r]}" for r in risks)}
    </div>
""", unsafe_allow_html=True)
        flagged_data.append({
            "Clause": clause.strip(),
            "Risks Detected": ", ".join(risks),
            "Explanations": " | ".join(explanations[r] for r in risks)
               
           })
    if flagged_data:
        df = pd.DataFrame(flagged_data)

        st.markdown("### 📥 Download Flagged Clauses")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="flagged_clauses.csv",
            mime="text/csv"
        )

