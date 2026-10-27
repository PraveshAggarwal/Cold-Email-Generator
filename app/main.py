# import streamlit as st
# import streamlit.components.v1 as components
# from langchain_community.document_loaders import WebBaseLoader

# from chains import Chain
# from portfolio import Portfolio
# from utils import clean_text

# CUSTOM_CSS = """
# <style>
# [data-testid="stAppViewContainer"] {
#     background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
#     color: #f0f0f0;
# }
# [data-testid="stHeader"] { background: transparent; }

# [data-testid="stMainBlockContainer"] {
#     padding-top: 1rem !important;
# }

# .card {
#     background: rgba(255,255,255,0.06);
#     border: 1px solid rgba(255,255,255,0.12);
#     border-radius: 16px;
#     padding: 2rem;
#     backdrop-filter: blur(10px);
# }

# div.stButton > button {
#     width: 100%;
#     background: linear-gradient(90deg, #6a11cb, #2575fc);
#     color: white;
#     border: none;
#     border-radius: 10px;
#     padding: 0.65rem 1.5rem;
#     font-size: 1rem;
#     font-weight: 600;
#     cursor: pointer;
#     transition: opacity 0.2s;
# }
# div.stButton > button:hover { opacity: 0.85; }

# .email-box {
#     background: rgba(0,0,0,0.35);
#     border: 1px solid rgba(255,255,255,0.1);
#     border-radius: 12px;
#     padding: 1.4rem 1.6rem;
#     white-space: pre-wrap;
#     font-family: 'Courier New', monospace;
#     font-size: 0.88rem;
#     line-height: 1.7;
#     color: #e8e8e8;
# }

# .tag {
#     display: inline-block;
#     background: rgba(101,78,163,0.55);
#     border: 1px solid rgba(101,78,163,0.8);
#     border-radius: 20px;
#     padding: 2px 12px;
#     margin: 3px 4px 3px 0;
#     font-size: 0.78rem;
#     color: #ddd;
# }

# .section-label {
#     font-size: 0.75rem;
#     text-transform: uppercase;
#     letter-spacing: 0.1em;
#     color: #aaa;
#     margin-bottom: 0.3rem;
# }
# </style>
# """


# def copy_button(text: str):
#     escaped = text.replace("\\", "\\\\").replace("`", "\\`")
#     components.html(
#         f"""
#         <button onclick="navigator.clipboard.writeText(`{escaped}`)
#             .then(()=>this.innerText='✅ Copied!')
#             .catch(()=>this.innerText='❌ Failed')"
#             style="margin-top:0.8rem;padding:0.4rem 1.1rem;background:#2575fc;
#                    color:white;border:none;border-radius:8px;font-size:0.82rem;cursor:pointer;">
#              Copy Email
#         </button>
#         """,
#         height=50,
#     )


# def create_streamlit_app(llm, portfolio, clean_text):
#     st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

#     st.markdown(
#         "<h1 style='text-align:center;font-size:2.4rem;margin-top:0;margin-bottom:0.2rem;'>"
#         "📧 Cold Email Generator</h1>"
#         "<p style='text-align:center;color:#bbb;margin-bottom:1.2rem;'>"
#         "Paste a job posting URL and get a personalised cold email in seconds.</p>",
#         unsafe_allow_html=True,
#     )

#     left, right = st.columns([1, 1], gap="large")

#     # ── left: input + skills ──
#     with left:
#         st.markdown("<p class='section-label'>Job Posting URL</p>", unsafe_allow_html=True)
#         url_input = st.text_input(
#             label="url", label_visibility="collapsed",
#             placeholder="https://careers.example.com/job/12345",
#         )
#         generate = st.button("⚡ Generate Email")

#         if generate and url_input.strip():
#             try:
#                 with st.spinner("🔍 Scraping job page…"):
#                     loader = WebBaseLoader([url_input])
#                     data = clean_text(loader.load().pop().page_content)

#                 with st.spinner("📄 Reading your resume…"):
#                     portfolio.load_portfolio()
#                     resume_text = portfolio.get_resume_text()

#                 with st.spinner("🤖 Extracting job details…"):
#                     jobs = llm.extract_jobs(data)

#                 # store results in session state so right column can read them
#                 emails = []
#                 for i, job in enumerate(jobs, 1):
#                     with st.spinner(f"✍️ Writing email {i}/{len(jobs)}…"):
#                         email = llm.write_mail(job, resume_text)
#                     emails.append((job, email))
#                 st.session_state["results"] = emails

#                 # skills below the button
#                 for job, _ in emails:
#                     skills = job.get("skills", [])
#                     if skills:
#                         st.markdown(
#                             f"<p class='section-label' style='margin-top:1.2rem;'>🛠 Required Skills — {job.get('role','')}</p>",
#                             unsafe_allow_html=True,
#                         )
#                         tags = "".join(f"<span class='tag'>{s}</span>" for s in skills)
#                         st.markdown(tags, unsafe_allow_html=True)

#             except Exception as e:
#                 st.error(f"An Error Occurred: {e}")
#         elif generate and not url_input.strip():
#             st.warning("Please enter a job URL first.")

#     # ── right: email output only ──
#     with right:
#         results = st.session_state.get("results", [])
#         if results:
#             for i, (job, email) in enumerate(results, 1):
#                 st.markdown(
#                     f"<p class='section-label'>📧 Generated Email — {job.get('role', f'Job {i}')}</p>",
#                     unsafe_allow_html=True,
#                 )
#                 st.markdown(f"<div class='email-box'>{email}</div>", unsafe_allow_html=True)
#                 copy_button(email)
#         else:
#             st.markdown(
#                 "<div style='padding-top:4rem;text-align:center;color:#666;font-size:0.95rem;'>"
#                 "Your generated email will appear here.</div>",
#                 unsafe_allow_html=True,
#             )


# if __name__ == "__main__":
#     chain = Chain()
#     portfolio = Portfolio()
#     st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
#     create_streamlit_app(chain, portfolio, clean_text)




import streamlit as st
import streamlit.components.v1 as components

from chains import Chain
from portfolio import extract_resume_text
from utils import clean_text, fetch_job_page


MAX_RESUME_SIZE = 5 * 1024 * 1024

CSS = """
<style>
[data-testid="stHeader"] { display: none; }

[data-testid="stMainBlockContainer"] {
    padding: 1.2rem 2rem 0 !important;
}

/* section labels above inputs */
.lbl {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #888;
    margin: 0.9rem 0 0.25rem;
}

/* skill pill badges */
.skill {
    display: inline-block;
    background: #1a2f4a;
    border: 1px solid #2e6da4;
    border-radius: 20px;
    padding: 3px 13px;
    margin: 3px 4px 3px 0;
    font-size: 0.78rem;
    color: #90caf9;
}

/* email read-only display box */
.email-box {
    background: #0e1117;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    white-space: pre-wrap;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    line-height: 1.75;
    color: #e0e0e0;
    margin-top: 0.4rem;
}

/* right panel placeholder */
.placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 60vh;
    color: #444;
    font-size: 0.95rem;
    text-align: center;
}

/* vertical divider between columns */
[data-testid="stVerticalBlockBorderWrapper"] { border: none !important; }
</style>
"""


def clear_previous_results():
    """Clear old generated emails when the resume or job input changes."""
    st.session_state.pop("results", None)

    # Clear old email editor values.
    for key in list(st.session_state.keys()):
        if key.startswith("email_"):
            st.session_state.pop(key, None)


@st.cache_resource
def get_chain():
    """Cache the LLM client, never the user's resume or generated email."""
    return Chain()


def _copy_button(text: str, idx: int):
    safe = text.replace("\\", "\\\\").replace("`", "\\`").replace("\r", "")
    components.html(
        f"""
        <button
          onclick="navigator.clipboard.writeText(`{safe}`)
            .then(()=>{{this.textContent='\u2705 Copied!';
                        setTimeout(()=>this.textContent='\U0001f4cb Copy Email',2000)}})
            .catch(()=>this.textContent='\u274c Failed')"
          style="padding:6px 20px;background:#2575fc;color:#fff;border:none;
                 border-radius:7px;font-size:0.82rem;cursor:pointer;font-weight:600;">
          \U0001f4cb Copy Email
        </button>""",
        height=42,
    )


def main():
    st.set_page_config(
        page_title="Cold Email Generator",
        page_icon="\U0001f4e7",
        layout="wide",
    )

    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>\U0001f4e7 Cold Email Generator</h3>", unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    # ── LEFT: inputs ──────────────────────────────────────────────────────────
    with left:

        # --------------------------------------------------
        # 1. Resume upload
        # --------------------------------------------------
        st.markdown("<p class='lbl'>Resume (PDF)</p>", unsafe_allow_html=True)
        uploaded_resume = st.file_uploader(
            "resume",
            type=["pdf"],
            accept_multiple_files=False,
            key="resume_uploader",
            label_visibility="collapsed",
            on_change=clear_previous_results,
        )

        # --------------------------------------------------
        # 2. Job details
        # --------------------------------------------------
        st.markdown("<p class='lbl'>Job Posting URL</p>", unsafe_allow_html=True)
        job_url = st.text_input(
            "url",
            placeholder="https://company.com/careers/job/123",
            key="job_url",
            label_visibility="collapsed",
            on_change=clear_previous_results,
        )

        st.markdown("<p class='lbl'>Or Paste Job Description</p>", unsafe_allow_html=True)
        job_description = st.text_area(
            "desc",
            height=160,
            placeholder="Paste the complete job description here...",
            key="job_description",
            label_visibility="collapsed",
            on_change=clear_previous_results,
        )

        # --------------------------------------------------
        # 3. Submit button
        # --------------------------------------------------
        generate = st.button(
            "\u26a1 Generate Cold Email",
            type="primary",
            use_container_width=True,
        )

    # ── RIGHT: output ─────────────────────────────────────────────────────────
    with right:

        if generate:
            # Always remove the previous result before starting.
            clear_previous_results()

            if uploaded_resume is None:
                st.error("Please upload your resume.")
                st.stop()

            if uploaded_resume.size > MAX_RESUME_SIZE:
                st.error("Resume size must not exceed 5 MB.")
                st.stop()

            pdf_bytes = uploaded_resume.getvalue()

            if not pdf_bytes.startswith(b"%PDF-"):
                st.error("Please upload a valid PDF file.")
                st.stop()

            try:
                # Extract text from the current uploaded resume.
                with st.spinner("Reading your resume..."):
                    resume_text = extract_resume_text(pdf_bytes)

                del pdf_bytes

                if not resume_text.strip():
                    st.error(
                        "No readable text was found in the resume. "
                        "Please upload a text-based PDF."
                    )
                    st.stop()

                # Use pasted job description first, if provided.
                job_text = job_description.strip()

                if not job_text and job_url.strip():
                    with st.spinner("Reading job posting..."):
                        job_text = fetch_job_page(job_url.strip())

                if not job_text:
                    st.error(
                        "Please enter a job URL or paste the job description."
                    )
                    st.stop()

                # Limit input size before sending it to the model.
                job_text = clean_text(job_text)[:25000]
                resume_text = resume_text[:18000]

                chain = get_chain()

                with st.spinner("Extracting job requirements..."):
                    jobs = chain.extract_jobs(job_text)

                if not jobs:
                    st.error(
                        "Could not extract job details. "
                        "Try pasting the job description directly."
                    )
                    st.stop()

                results = []

                with st.spinner("Generating your personalized email..."):
                    for job in jobs[:3]:
                        email = chain.write_mail(job, resume_text)
                        results.append((job, email))

                # Store results only in this user's Streamlit session.
                st.session_state["results"] = results

                # Remove our local reference to the extracted resume text.
                del resume_text

            except Exception as exc:
                # Avoid displaying sensitive server details to public users.
                st.error(
                    f"Email generation failed ({type(exc).__name__}). "
                    "Try pasting the job description or uploading another PDF."
                )

        # --------------------------------------------------
        # 4. Display generated emails
        # --------------------------------------------------
        results = st.session_state.get("results", [])

        if results:
            for index, (job, email) in enumerate(results, start=1):
                role = job.get("role") or f"Job {index}"

                if len(results) > 1:
                    st.markdown(f"**{role}**")

                # Skills section
                skills = job.get("skills", [])
                if isinstance(skills, list) and skills:
                    st.markdown("<p class='lbl'>\U0001f6e0 Required Skills</p>", unsafe_allow_html=True)
                    badges = "".join(f"<span class='skill'>{s}</span>" for s in skills)
                    st.markdown(badges, unsafe_allow_html=True)

                # Email section
                st.markdown("<p class='lbl'>\U0001f4e7 Cold Email</p>", unsafe_allow_html=True)

                # Copy button at the top of the email
                _copy_button(email, index)

                st.markdown(f"<div class='email-box'>{email}</div>", unsafe_allow_html=True)

                if index < len(results):
                    st.divider()

        else:
            st.markdown(
                "<div class='placeholder'>\U0001f4ec Results will appear here after you submit.</div>",
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
