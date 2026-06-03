from pypdf import PdfReader


def extract_text_by_page(file_path: str):

    reader = PdfReader(file_path)

    pages = []

    for index, page in enumerate(reader.pages):

        text = page.extract_text()

        if text:

            pages.append({
                "page_number": index + 1,
                "text": text
            })

    return pages
