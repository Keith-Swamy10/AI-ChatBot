import os
from bs4 import BeautifulSoup
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_html_pages(base_url, output_dir):
    visited_urls = set()

    def crawl_and_save(url):
        if url in visited_urls:
            return
        visited_urls.add(url)

        response = requests.get(url)
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Save the HTML content to a file
        page_name = url.replace(base_url, '').replace('/', '_') or 'index'
        file_path = os.path.join(output_dir, f"{page_name}.html")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        # Recursively crawl other pages within the same domain
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/') or href.startswith(base_url):
                next_url = href if href.startswith('http') else base_url + href
                print(next_url)
                crawl_and_save(next_url)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    crawl_and_save(base_url)

def convert_html_to_pdf_with_reportlab(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".html"):
            file_path = os.path.join(input_dir, filename)

            # Extract text content from the HTML file
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                page_text = soup.get_text(separator='\n', strip=True)

            # Create a PDF for the extracted text
            pdf_filename = filename.replace(".html", ".pdf")
            pdf_output_path = os.path.join(output_dir, pdf_filename)

            # Use reportlab to generate the PDF
            c = canvas.Canvas(pdf_output_path, pagesize=letter)
            width, height = letter
            c.setFont("Helvetica", 10)

            # Write text to the PDF, handling line breaks
            y_position = height - 50
            for line in page_text.split('\n'):
                if y_position < 50:  # Start a new page if the current page is full
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y_position = height - 50
                c.drawString(50, y_position, line)
                y_position -= 12

            c.save()

# Example usage
# input_dir = "app/index_pages_dir"
# output_dir = "app/index_pages_dir_pdfs"
# convert_html_to_pdf_with_reportlab(input_dir, output_dir)

# For storing html pages
website_link = "Enter website link here"
output_dir = "data/index_pages_dir"
save_html_pages(website_link, output_dir)