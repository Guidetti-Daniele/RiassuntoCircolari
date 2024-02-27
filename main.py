from pdf_parsing import parse_pdf

text_parsed = parse_pdf("file2.pdf", "Tabella")  # Save the parsed PDF in a string
output_file = "parsedPDF.txt"

with open(output_file, "w", encoding='utf-8') as file_to_save:
    file_to_save.write(text_parsed)
