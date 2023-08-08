import streamlit as st
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import pdfkit
import requests
# Load Jinja environment with the template folder
template_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(['html', 'xml'])
)
def generate_invoice(data):
    # Load the Jinja template for the invoice
    template = template_env.get_template("invoice_template.html")
    # Render the template with the provided data
    rendered_html = template.render(data=data)
    return rendered_html
def generate_pdf(html_content):
    pdfkit_options = {
        "page-size": "Letter",
        "encoding": "UTF-8",
    }
    pdf_content = pdfkit.from_string(html_content, False, options=pdfkit_options)
    return pdf_content
def upload_to_anonfiles(file_content):
    upload_url = "https://api.anonfiles.com/upload"
    files = {"file": ("invoice.pdf", file_content)}
    response = requests.post(upload_url, files=files)
    if response.status_code == 200:
        data = response.json()
        if data["status"]:
            return data["data"]["file"]["url"]["short"]
    return None
def main():
    st.title("Invoice Generator")
    # User input for invoice data
    customer_name = st.text_input("Customer Name:")
    invoice_date = st.date_input("Invoice Date:")
    amount = st.number_input("Invoice Amount:", min_value=0.01, step=0.01)
    data = {
        "customer_name": customer_name,
        "invoice_date": invoice_date.strftime('%B %d, %Y'),
        "amount": amount
    }
    # Generate and display the invoice HTML
    if st.button("Generate Invoice"):
        rendered_invoice = generate_invoice(data)
        st.subheader("Generated Invoice:")
        pdf_content = generate_pdf(rendered_invoice)
        if pdf_content:
            # Save PDF locally
            pdf_filename = "invoice.pdf"
            with open(pdf_filename, "wb") as pdf_file:
                pdf_file.write(pdf_content)
            st.success("PDF generated and saved successfully!")
            # Upload PDF to AnonFiles
            short_url = upload_to_anonfiles(pdf_content)
            if short_url:
                st.write("PDF uploaded successfully.")
                st.write("PDF Short URL:", short_url)
                os.remove(pdf_filename)  # Remove the locally saved PDF
            else:
                st.error("Failed to upload PDF.")
if __name__ == "__main__":
    main()
