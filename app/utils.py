# import re

# def clean_text(text):
#     # Remove HTML tags
#     text = re.sub(r'<[^>]*?>', '', text)
#     # Remove URLs
#     text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
#     # Remove special characters
#     text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
#     # Replace multiple spaces with a single space
#     text = re.sub(r'\s{2,}', ' ', text)
#     # Trim leading and trailing whitespace
#     text = text.strip()
#     # Remove extra whitespace
#     text = ' '.join(text.split())
#     return text
    



import re
import ipaddress
import socket
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def clean_text(text):
    text = re.sub(r"<[^>]*?>", " ", text or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def validate_public_url(url):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("Only HTTP and HTTPS URLs are allowed.")

    if not parsed.hostname:
        raise ValueError("Please enter a valid job URL.")

    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not allowed.")

    host = parsed.hostname.rstrip(".").lower()

    if (
        host == "localhost"
        or host.endswith(".localhost")
        or host.endswith(".local")
    ):
        raise ValueError("Local URLs are not allowed.")

    try:
        ip = ipaddress.ip_address(host)
        if not ip.is_global:
            raise ValueError("Private IP addresses are not allowed.")
    except ValueError:
        try:
            ipaddress.ip_address(host)
        except ValueError:
            pass
        else:
            raise ValueError("Private IP addresses are not allowed.")

    try:
        addresses = socket.getaddrinfo(
            host,
            parsed.port or (443 if parsed.scheme == "https" else 80)
        )
    except socket.gaierror as exc:
        raise ValueError("Could not resolve the job URL.") from exc

    for address in addresses:
        ip = ipaddress.ip_address(address[4][0].split("%")[0])
        if not ip.is_global:
            raise ValueError("The URL resolves to a private IP address.")

    return url


def fetch_job_page(url):
    current_url = validate_public_url(url)

    for _ in range(4):
        current_url = validate_public_url(current_url)

        try:
            with requests.get(
                current_url,
                headers={"User-Agent": "ColdEmailGenerator/1.0"},
                timeout=(4, 12),
                stream=True,
                allow_redirects=False,
            ) as response:

                if response.is_redirect or response.is_permanent_redirect:
                    location = response.headers.get("Location")

                    if not location:
                        raise ValueError("Invalid redirect.")

                    current_url = urljoin(current_url, location)
                    continue

                response.raise_for_status()

                content_type = response.headers.get(
                    "Content-Type", ""
                ).lower()

                if (
                    "text/html" not in content_type
                    and "text/plain" not in content_type
                ):
                    raise ValueError(
                        "The URL does not contain a readable job page."
                    )

                chunks = []
                total_size = 0

                for chunk in response.iter_content(65536):
                    if not chunk:
                        continue

                    total_size += len(chunk)

                    if total_size > 2_000_000:
                        raise ValueError("Job page is too large.")

                    chunks.append(chunk)

                page = b"".join(chunks).decode(
                    response.encoding or "utf-8",
                    errors="replace"
                )

                if "text/plain" in content_type:
                    text = page
                else:
                    soup = BeautifulSoup(page, "html.parser")

                    for element in soup(
                        ["script", "style", "noscript", "nav", "footer"]
                    ):
                        element.decompose()

                    content = (
                        soup.find("main")
                        or soup.find("article")
                        or soup.body
                        or soup
                    )

                    text = content.get_text(" ", strip=True)

                text = clean_text(text)

                if len(text) < 100:
                    raise ValueError(
                        "Not enough text found. Paste the job description instead."
                    )

                return text[:25000]

        except requests.RequestException as exc:
            raise ValueError(
                "Could not fetch this job page. Paste its description instead."
            ) from exc

    raise ValueError("Too many redirects.")
