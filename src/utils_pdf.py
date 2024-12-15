import math
import re
from io import BytesIO
from statistics import median

import pandas as pd
from bs4 import BeautifulSoup
from langchain.document_loaders import PDFMinerPDFasHTMLLoader
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

deep_strip = lambda text: re.sub(r"\s+", " ", text or "").strip()


def process_pdf(url=None, file=None):
    if url:
        data = PDFMinerPDFasHTMLLoader(url).load()[0].page_content
    elif file:
        output_buffer = BytesIO()
        extract_text_to_fp(file, output_buffer, output_type="html", laparams=LAParams())
        data = output_buffer.getvalue().decode("utf-8")
    else:
        raise ValueError("Either URL or file must be provided")
    content = BeautifulSoup(data, "html.parser").find_all("div")
    snippets = get_pdf_snippets(content)
    filtered_snippets = filter_pdf_snippets(snippets, new_line_threshold_ratio=0.4)
    median_font_size = math.ceil(median([font_size for _, font_size in filtered_snippets]))
    semantic_snippets = get_pdf_semantic_snippets(filtered_snippets, median_font_size)
    document_snippets = [
        {
            "timestamp": pd.Timestamp.now(),
            "title": " ".join(snip[1]["header_text"].split()[:10]),
            "text": deep_strip(snip[1]["header_text"]) + " " + deep_strip(snip[0]),
        }
        for snip in semantic_snippets
    ]
    return document_snippets


def get_pdf_snippets(content):
    current_font_size = None
    current_text = ""
    snippets = []
    for cntnt in content:
        span = cntnt.find("span")
        if not span:
            continue
        style = span.get("style")
        if not style:
            continue
        font_size = re.findall("font-size:(\d+)px", style)
        if not font_size:
            continue
        font_size = int(font_size[0])

        if not current_font_size:
            current_font_size = font_size
        if font_size == current_font_size:
            current_text += cntnt.text
        else:
            snippets.append((current_text, current_font_size))
            current_font_size = font_size
            current_text = cntnt.text
    snippets.append((current_text, current_font_size))
    return snippets


def filter_pdf_snippets(content_list, new_line_threshold_ratio):
    filtered_list = []
    for e, (content, font_size) in enumerate(content_list):
        newline_count = content.count("\n")
        total_chars = len(content)
        ratio = newline_count / total_chars
        if ratio <= new_line_threshold_ratio:
            filtered_list.append((content, font_size))
    return filtered_list


def create_metadata(header, header_font_size, content_font_sizes):
    return {
        "header_font_size": header_font_size,
        "content_font_size": (median(content_font_sizes) if content_font_sizes else None),
        "header_text": header,
    }


def add_snippet(semantic_snippets, header, content, header_font_size, content_font_sizes):
    metadata = create_metadata(header, header_font_size, content_font_sizes)
    semantic_snippets.append((content, metadata))


def get_pdf_semantic_snippets(filtered_snippets, median_font_size):
    semantic_snippets = []
    current_header = None
    current_content = []
    header_font_size = None
    content_font_sizes = []

    for content, font_size in filtered_snippets:
        if font_size > median_font_size:
            if current_header is not None:
                add_snippet(semantic_snippets, current_header, current_content, header_font_size, content_font_sizes)
                current_content = []
                content_font_sizes = []

            current_header = content
            header_font_size = font_size
        else:
            content_font_sizes.append(font_size)
            current_content = f"{current_content} {content}" if current_content else content

    if current_header is not None:
        add_snippet(semantic_snippets, current_header, current_content, header_font_size, content_font_sizes)

    return semantic_snippets
