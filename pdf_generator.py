from datetime import date
from fpdf import FPDF
from file_path import PATH_TO_GENERATED_CONTENT, PATH_TO_PDF
import streamlit as st

SUCCESSFUL_MSG = "PDF successfully exported. You can find it here doc/pdf within this project"
UNSUCCESSFUL_MSG = "Error while generating the pdf file. Please, try again"


def generate_pdf(topic):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    today = str(date.today())
    title = today + ": A brief overview of " + topic
    try:
        with open(PATH_TO_GENERATED_CONTENT + today + "_" + topic + ".txt", "r") as file:
            for line in file:
                # Split line into words
                words = line.split()
                chunk = ""
                for word in words:
                    # Check if adding word exceeds max line length
                    if len(chunk) + len(word) + 1 > 95:
                        pdf.cell(200, 10, txt=chunk.strip(), ln=True, align='L')
                        chunk = word + " "
                    else:
                        chunk += word + " "

                # Add remaining chunk to PDF
                if chunk:
                    pdf.cell(200, 10, txt=chunk.strip(), ln=True, align='L')

        # Save the PDF with filename
        pdf.output(PATH_TO_PDF + title + ".pdf")
        st.write(":green[" + SUCCESSFUL_MSG + "]")
    except Exception as ex:
        print("Error while getting the summary", ex)
        st.write(":red[" + UNSUCCESSFUL_MSG + "]")
