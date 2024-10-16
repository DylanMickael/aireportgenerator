import os
from fpdf import FPDF

class Document:
    def __init__(self):
        self.pdf = FPDF()
        self.pdf.add_page()

    def add_title(self, title):
        self.pdf.set_font('Arial', 'B', 16)
        self.pdf.cell(0, 10, title, ln=True, align='C')
        self.pdf.ln(10)

    def add_subtitle(self, subtitle):
        self.pdf.set_font('Arial', 'I', 12)
        self.pdf.cell(0, 10, subtitle, ln=True, align='L')
        self.pdf.ln(5)

    def add_text(self, text):
        self.pdf.set_font('Arial', '', 12)
        self.pdf.multi_cell(0, 10, text)
        self.pdf.ln(5)

    def add_image(self, image_data):
        temp_file_path = 'temp_image.png'
        with open(temp_file_path, 'wb') as f:
            f.write(image_data.getvalue())

        self.pdf.image(temp_file_path, x=10, y=self.pdf.get_y(), w=180)

        os.remove(temp_file_path)
        self.pdf.ln(5)

    def add_table(self, data):
        self.pdf.set_font('Arial', 'B', 12)
        col_widths = []

        for row in data:
            for i, item in enumerate(row):
                item_width = self.pdf.get_string_width(str(item)) + 10
                if i >= len(col_widths):
                    col_widths.append(item_width)
                else:
                    col_widths[i] = max(col_widths[i], item_width)

        total_width = sum(col_widths)
        if total_width > 180:
            scale_factor = 180 / total_width
            col_widths = [w * scale_factor for w in col_widths]

        for row in data:
            for i, item in enumerate(row):
                self.pdf.cell(col_widths[i], 10, str(item), border=1)
            self.pdf.ln()

        self.pdf.ln(5)

    def generate(self):
        pdf_output = self.pdf.output(dest='S').encode('latin1')
        return pdf_output
