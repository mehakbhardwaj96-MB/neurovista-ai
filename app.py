
import streamlit as st
import pandas as pd
import requests
import random
from datetime import date, datetime
from xml.etree import ElementTree as ET

st.set_page_config(
    page_title="NeuroVista AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 NeuroVista AI")
st.subheader("Cognitive Research & Brain-Imaging Support")

st.write(
    "A research prototype that organises questionnaire responses, "
    "relevant history and published Alzheimer's research."
)

st.warning(
    "RESEARCH PROTOTYPE ONLY. This app does not diagnose Alzheimer's, "
    "determine dementia status, assign a disease stage, or analyse MRI/PET."
)
st.info(
    "Use fictional data only. Do not enter real patient identifiers "
    "or upload identifiable medical records."
)

# -------------------- PATIENT PROFILE --------------------

st.header("1. Participant Profile")

c1, c2 = st.columns(2)

with c1:
    pid = st.text_input("Demo participant ID", "NV-001")
    dob = st.date_input(
        "Date of birth (optional)",
        value=None,
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )
    if dob:
        age = date.today().year - dob.year - (
            (date.today().month, date.today().day) < (dob.month, dob.day)
        )
        st.write(f"Calculated age: {age}")
    else:
        age = st.number_input("Age", min_value=18, max_value=120, value=60)

with c2:
    sex = st.selectbox(
        "Sex (optional)",
        ["Prefer not to say", "Female", "Male", "Intersex", "Other"]
    )
    education = st.selectbox(
        "Education",
        ["Prefer not to say", "Primary", "Secondary",
         "College/university", "Postgraduate", "No formal education"]
    )
    reporter = st.selectbox(
        "Information provided by",
        ["Participant", "Family/care partner",
         "Healthcare professional", "Fictional demo"]
    )

st.caption("This is a demo profile, not a secure medical record.")

# -------------------- QUESTIONNAIRE --------------------

st.header("2. Cognitive and Daily-Life Questionnaire")
st.caption(
    "These original demonstration questions are not a validated "
    "clinical instrument."
)

questions = {
    "Memory": [
        "Forgetting recent conversations or events",
        "Repeating questions or stories",
        "Forgetting recently learned information"
    ],
    "Language and orientation": [
        "Difficulty finding familiar words",
        "Difficulty following conversations",
        "Confusion about dates or familiar places"
    ],
    "Planning and attention": [
        "Difficulty planning or solving everyday problems",
        "Difficulty completing familiar multi-step tasks",
        "Difficulty concentrating on familiar activities"
    ],
    "Daily function and behaviour": [
        "Noticeable changes in mood, behaviour or motivation",
        "Difficulty managing familiar daily activities",
        "Difficulty managing appointments or money"
    ]
}

frequency = ["Never", "Rarely", "Sometimes", "Often", "Unsure"]
answers = {}

for section, items in questions.items():
    with st.expander(section, expanded=True):
        for q in items:
            answers[q] = st.select_slider(
                q, options=frequency, value="Never", key=q
            )

onset = st.selectbox(
    "When were concerns first noticed?",
    ["No concerns reported", "Within the last month",
     "Several months ago", "More than a year ago", "Unsure"]
)

change = st.selectbox(
    "Change over time",
    ["No concerns reported", "No noticeable change",
     "Gradually increased", "Changed suddenly",
     "Fluctuates", "Unsure"]
)

impact = st.selectbox(
    "Reported impact on daily activities",
    ["No reported impact", "Mild", "Moderate", "Major", "Unsure"]
)

# -------------------- MEMORY DEMONSTRATION --------------------

st.header("3. Mini Memory Activity")
st.write(
    "An informal demonstration, not the MMSE, MoCA or another "
    "validated cognitive test."
)

if "memory_words" not in st.session_state:
    st.session_state.memory_words = random.sample(
        ["APPLE", "RIVER", "KEY", "GARDEN", "LAMP", "TRAIN"], 3
    )
if "memory_hidden" not in st.session_state:
    st.session_state.memory_hidden = False

if not st.session_state.memory_hidden:
    st.write("Try to remember these words:")
    st.subheader(" · ".join(st.session_state.memory_words))
    if st.button("Hide words and start recall"):
        st.session_state.memory_hidden = True
        st.rerun()
else:
    recall = st.text_input(
        "Type the words you remember, separated by commas"
    )
    if st.button("Check demo recall"):
        entered = {
            word.strip().upper()
            for word in recall.split(",") if word.strip()
        }
        correct = len(entered.intersection(st.session_state.memory_words))
        st.write(f"Words matched: {correct} out of 3")
        st.caption(
            "This unstandardised activity is for demonstrating software "
            "functionality only. It cannot assess cognitive health."
        )
        if st.button("Try a new word set"):
            st.session_state.memory_words = random.sample(
                ["APPLE", "RIVER", "KEY", "GARDEN", "LAMP", "TRAIN"], 3
            )
            st.session_state.memory_hidden = False
            st.rerun()

# -------------------- MEDICAL HISTORY --------------------

st.header("4. Relevant History")

conditions = st.multiselect(
    "Relevant health history (optional)",
    ["High blood pressure", "Diabetes", "Previous stroke",
     "Thyroid condition", "Vitamin deficiency", "Sleep disorder",
     "Depression/anxiety", "Neurological condition", "Other", "Unknown"]
)

medications = st.text_area(
    "Medication notes (optional; fictional information only)"
)

family = st.selectbox(
    "Family history of dementia",
    ["Unknown", "No known family history",
     "Reported family history", "Prefer not to say"]
)

sleep = st.selectbox(
    "Sleep concerns",
    ["Unknown", "None reported", "Difficulty sleeping",
     "Daytime sleepiness", "Other"]
)

mood = st.selectbox(
    "Mood concerns",
    ["Unknown", "None reported", "Low mood", "Anxiety/stress", "Other"]
)

history_notes = st.text_area("Other context (optional)")

# -------------------- MRI/PET FILE INFORMATION --------------------

st.header("5. Optional Imaging Information")

scan_type = st.selectbox(
    "Imaging type",
    ["None", "MRI", "PET", "MRI and PET", "Existing scan report"]
)

scan_file = st.file_uploader(
    "Select a demo image or file (optional)",
    type=["png", "jpg", "jpeg", "csv", "pdf"]
)

if scan_file:
    st.write("Selected file:", scan_file.name)
    st.write("File size:", f"{scan_file.size / 1024:.1f} KB")
    if scan_file.type.startswith("image/"):
        st.image(scan_file, caption="Uploaded image — not AI-analysed")
    elif scan_file.type == "text/csv":
        try:
            st.dataframe(pd.read_csv(scan_file).head(10))
        except Exception:
            st.info("Could not preview this CSV.")
    else:
        st.info("File selected. This prototype does not interpret PDFs.")

# -------------------- EDUCATIONAL STAGES --------------------

st.header("6. Educational Information")

st.write(
    "The descriptions below are educational only. This app does not "
    "assign any participant to a stage."
)

st.markdown("""
- **Preclinical changes:** Biological changes may precede noticeable symptoms.
- **Mild / early stage:** Memory or other thinking difficulties may emerge.
- **Moderate stage:** Cognitive difficulties may increasingly affect daily life.
- **Severe / late stage:** Extensive support with everyday care may be needed.

People differ in symptoms and progression. Clinical assessment is required.
""")

st.markdown(
    "[How Alzheimer's is diagnosed — National Institute on Aging]"
    "(https://www.nia.nih.gov/health/alzheimers-symptoms-and-diagnosis/"
    "how-alzheimers-disease-diagnosed)"
)
st.markdown(
    "[Official ADNI data and access information]"
    "(https://adni.loni.usc.edu/data-samples/adni-data/)"
)

# -------------------- LIVE PUBMED SEARCH --------------------

st.header("7. Published Research Search")
st.write(
    "Search PubMed for published biomedical literature. "
    "Results are references, not patient records or an ADNI download."
)

term = st.text_input(
    "Research topic",
    value="Alzheimer disease MRI cognitive assessment"
)
max_results = st.selectbox("Number of references", [5, 10, 15, 20], index=1)

if st.button("Search Published Research"):
    try:
        base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = base + "esearch.fcgi"
        search_response = requests.get(
            search_url,
            params={
                "db": "pubmed",
                "term": term,
                "retmax": max_results,
                "sort": "relevance",
                "retmode": "json"
            },
            timeout=20
        )
        search_response.raise_for_status()
        ids = search_response.json()["esearchresult"]["idlist"]

        if not ids:
            st.info("No references found for this search.")
        else:
            fetch_response = requests.get(
                base + "esummary.fcgi",
                params={
                    "db": "pubmed",
                    "id": ",".join(ids),
                    "retmode": "json"
                },
                timeout=20
            )
            fetch_response.raise_for_status()
            result = fetch_response.json()["result"]

            references = []
            for article_id in ids:
                item = result.get(article_id, {})
                title = item.get("title", "Title unavailable")
                pubdate = item.get("pubdate", "Date unavailable")
                source = item.get("fulljournalname", "Journal unavailable")
                references.append({
                    "Title": title,
                    "Date": pubdate,
                    "Journal": source,
                    "PubMed URL": f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"
                })

            st.session_state.research_results = references
            st.success(f"Retrieved {len(references)} references.")

    except Exception as e:
        st.error(
            "Research search could not be completed. Check the connection "
            "and try again. Details: " + str(e)
        )

if "research_results" in st.session_state:
    for i, item in enumerate(st.session_state.research_results, start=1):
        st.markdown(f"**{i}. [{item['Title']}]({item['PubMed URL']})**")
        st.caption(f"{item['Journal']} · {item['Date']}")

# -------------------- REPORT GENERATOR --------------------

st.header("8. Generate Research Demonstration Report")

consent = st.checkbox(
    "I understand this is a demonstration, not a diagnosis, "
    "and I am using fictional information."
)

if st.button("Generate Full Report", type="primary"):
    if not pid.strip():
        st.error("Enter a demo participant ID.")
    elif not consent:
        st.error("Confirm the demo disclaimer first.")
    else:
        record = {
            "Demo ID": pid,
            "Age": age,
            "DOB": str(dob) if dob else "Not entered",
            "Sex": sex,
            "Education": education,
            "Reporter": reporter,
            "Concern onset": onset,
            "Change over time": change,
            "Daily-life impact": impact,
            "Medical history": ", ".join(conditions),
            "Medication notes": medications,
            "Family history": family,
            "Sleep": sleep,
            "Mood": mood,
            "Other history": history_notes,
            "Imaging type": scan_type,
            "Uploaded filename": scan_file.name if scan_file else "None",
            **answers
        }

        st.success("Report generated.")
        st.subheader("Participant and questionnaire summary")
        st.dataframe(
            pd.DataFrame(
                list(record.items()),
                columns=["Field", "Entered information"]
            ),
            use_container_width=True
        )

        if "research_results" in st.session_state:
            st.subheader("Research references")
            for item in st.session_state.research_results:
                st.markdown(f"- [{item['Title']}]({item['PubMed URL']})")

        st.caption(
            "This report organises supplied information. It does not "
            "diagnose dementia, calculate a validated clinical score, "
            "assign a disease stage or interpret brain scans."
        )

        report_df = pd.DataFrame(
            list(record.items()),
            columns=["Field", "Entered information"]
        )
        st.download_button(
            "Download Report (CSV)",
            data=report_df.to_csv(index=False).encode("utf-8"),
            file_name=f"{pid}_research_report.csv",
            mime="text/csv"
        )

st.divider()
st.caption(
    "NeuroVista AI · Research prototype · Not for clinical decisions"
)
