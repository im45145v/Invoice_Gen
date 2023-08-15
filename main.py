import streamlit as st
from jinja2 import Environment, FileSystemLoader, select_autoescape
import base64
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
        # Generate a unique URL for the HTML content
        url = f"data:text/html;charset=UTF-8;base64,{base64.b64encode(rendered_invoice.encode()).decode()}"
        # Display link for manual opening
        st.markdown('### Generated Invoice')
        st.markdown(f'Click [here](%s) to open Invoice.' % url, unsafe_allow_html=True)
        st.markdown('Right click and open it')
if __name__ == "__main__":
    main()
