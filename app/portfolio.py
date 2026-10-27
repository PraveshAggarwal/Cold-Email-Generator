# import os
# from pypdf import PdfReader


# class Portfolio:
#     """Reads the resume PDF and gives its text to the email writer.

#     (Replaces the old ChromaDB portfolio: the resume is now the only source of facts.)
#     """

#     def __init__(self, resume_path=None):
#         base_dir = os.path.dirname(os.path.abspath(__file__))
#         self.resume_path = resume_path or os.path.join(base_dir, "Pravesh_Resume(0).pdf")
#         self.resume_text = ""

#     def load_portfolio(self):
#         """Extract the text from the resume once and cache it."""
#         if self.resume_text:
#             return
#         if not os.path.exists(self.resume_path):
#             raise FileNotFoundError(f"Resume not found at: {self.resume_path}")

#         reader = PdfReader(self.resume_path)
#         self.resume_text = "\n".join(page.extract_text() or "" for page in reader.pages)

#         if not self.resume_text.strip():
#             raise ValueError("No text found in the resume PDF (it may be a scanned image).")

#     def get_resume_text(self):
#         return self.resume_text




from io import BytesIO
from pypdf import PdfReader


def extract_resume_text(pdf_bytes: bytes) -> str:
    """Extract resume text without saving the uploaded PDF to disk."""

    if not pdf_bytes:
        raise ValueError("The uploaded resume is empty.")

    try:
        reader = PdfReader(BytesIO(pdf_bytes), strict=True)

        if reader.is_encrypted:
            raise ValueError(
                "Password-protected PDFs are not supported."
            )

        if len(reader.pages) == 0:
            raise ValueError("The PDF contains no pages.")

        if len(reader.pages) > 20:
            raise ValueError(
                "Please upload a resume with no more than 20 pages."
            )

        resume_text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(
            "Could not read the PDF. Please upload a valid resume."
        ) from exc

    if not resume_text.strip():
        raise ValueError(
            "No readable text found. Please upload a text-based PDF."
        )

    return resume_text.strip()
