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
def upload_to_anonfiles(file_path):
    upload_url = "https://api.anonfiles.com/upload"

    with open(file_path, "rb") as file:
        files = {"file": (file_path, file)}

        response = requests.post(upload_url, files=files)
        if response.status_code == 200:
            data = response.json()
            if data["status"]:
                return data["data"]["file"]["url"]["short"]
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
        # Save the rendered HTML to a file
        output_html_path = "invoice.html"
        with open(output_html_path, "w") as f:
            f.write(rendered_invoice)
        pdfkit.from_file('invoice.html', 'invoice.pdf')
        if os.path.exists("invoice.html"):
            os.remove("invoice.html")
        st.success("Invoice HTML generated and saved.")
        short_url = upload_to_anonfiles("invoice.pdf")
        if short_url:
            st.write("File uploaded successfully.")
            st.write("Short URL:", short_url)
            if os.path.exists("invoice.pdf"):
                os.remove("invoice.pdf")
        else:
            print("Failed to upload file.")
if __name__ == "__main__":
    main()
