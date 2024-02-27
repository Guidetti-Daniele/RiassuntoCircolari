from pdf_parsing import parse_pdf

input_file_path = "file.pdf"  # path to the PDF file to parse
table_name = "Tabella"  # name to tell the cat that there is a table

output_file = "parsedPDF.txt"  # path to the file to save

text_parsed = parse_pdf(input_file_path, table_name)  # Save the parsed PDF in a string

with open(output_file, "w", encoding='utf-8') as file_to_save:
    file_to_save.write(text_parsed)
