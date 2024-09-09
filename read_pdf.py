import PyPDF2

pdf_file = input("Where is you're file located?\nProvide the full path:\n")
# print(pdf_file)

# Open the PDF file in read-binary mode

with open(pdf_file, 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Get the number of pages
    num_pages = len(pdf_reader.pages)

    # Extract text from each page
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        print(text)