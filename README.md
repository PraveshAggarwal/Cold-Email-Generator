# 📧 Cold Email Generator

A Streamlit web app that generates personalized cold emails for job applications. Upload your resume (PDF), provide a job posting URL or paste the description, and get a tailored cold email in seconds — powered by Groq's LLM API.

---

## How It Works

1. You upload your resume as a PDF.
2. You paste a job URL or the job description text.
3. The app scrapes and cleans the job page (if a URL is given).
4. The LLM extracts structured job details (role, skills, experience).
5. A second LLM call writes a short, honest cold email using only facts from your resume.

---

## Features

- Resume-grounded emails — the LLM is strictly instructed to use only facts from your resume, no hallucinations.
- URL scraping with SSRF protection — private IPs, localhost, and credential-embedded URLs are blocked.
- Paste fallback — if the job page can't be scraped, paste the description directly.
- Copy-to-clipboard button on every generated email.
- Skill badges extracted from the job posting shown alongside the email.
- Session-isolated — resume text is never cached; it lives only in the current request.

---

## Project Structure

```
coldEmail(LLM)/
├── app/
│   ├── main.py          # Streamlit UI — inputs, layout, session state
│   ├── chains.py        # LLM logic — job extraction and email writing (LangChain + Groq)
│   ├── portfolio.py     # PDF resume parser (pypdf, in-memory, no disk writes)
│   └── utils.py         # URL validation, SSRF guard, page fetcher, text cleaner
├── .env                 # Your API keys (never commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd "coldEmail(LLM)"
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=<your_groq_api_key>
```

Get your free API key at [console.groq.com](https://console.groq.com).

### 5. Run the app

```bash
cd app
streamlit run main.py
```

The app opens at `http://localhost:8501`.

---

## Usage

| Step | Action |
|------|--------|
| 1 | Click **Browse files** and upload your resume as a PDF (max 5 MB, max 20 pages, text-based). |
| 2 | Paste the job posting URL **or** paste the full job description in the text area. |
| 3 | Click **⚡ Generate Cold Email**. |
| 4 | The right panel shows the required skills and your generated email. |
| 5 | Click **📋 Copy Email** to copy it to your clipboard. |

---

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for LLM inference | ✅ Yes |

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI |
| `langchain` + `langchain-groq` | LLM orchestration and Groq integration |
| `langchain-core` | Prompt templates and output parsers |
| `pypdf` | In-memory PDF text extraction |
| `beautifulsoup4` | HTML parsing for job page scraping |
| `requests` | HTTP client for fetching job pages |
| `python-dotenv` | Loading `.env` variables |

---

## Security Notes

- The URL fetcher blocks private IPs, loopback addresses, and `.local` hostnames to prevent SSRF attacks.
- Uploaded PDFs are read into memory only — never written to disk.
- Resume text is deleted from memory after the email is generated; it is never stored in Streamlit's cache.
- The `.env` file is listed in `.gitignore` — never commit your API keys.

---

## Limitations

- Only text-based PDFs are supported. Scanned/image PDFs will return an error.
- Some job pages block automated scraping. Use the paste option as a fallback.
- The LLM model used is `openai/gpt-oss-120b` via Groq. Swap the model name in `chains.py` if needed.

---

## License

MIT
