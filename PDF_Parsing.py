import tabula
from PyPDF2 import PdfReader


def find_no_spaces(main, object_string):  # find index of object_sting in the main string ignoring spaces
    current_index = 0
    object_index = 0
    object_len = len(object_string)

    when_started = -1
    has_started = False

    for char in main:
        if char == ' ':  # ignore the space
            current_index += 1
        else:
            if char == object_string[object_index]:
                if not has_started:
                    has_started = True
                    when_started = current_index  # save the start index of the string
                if object_index == object_len - 1:
                    return when_started, current_index  # return start and end index of object_sting in the main string
                object_index += 1
            else:  # if string not found reset index
                object_index = 0
                has_started = False
                when_started = -1
            current_index += 1

    return -1, -1


def replace_text(text_to_replace):  # replace \n \r \t with space
    return str(text_to_replace).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')


def remove_spaces(text_to_replace):  # remove all spaces and \n \r \t
    return str(text_to_replace).replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')


def replace_from_index(string, start_index, end_index, replaced):  # replace a part of the string between two indexes
    return string[:start_index] + replaced + string[end_index + 1:]


def parse_pdf(file_path, table_name):  # table_name is used to tell the cat when there is a table
    tables = tabula.read_pdf(file_path, pages="all")  # read only the tables

    tables_text = ['' for _ in range(len(tables))]
    tables_clean_text = ['' for _ in range(len(tables))]

    for dataIndex, dataframe in enumerate(tables):  # read tables and save them in variables
        tables_text[dataIndex] = table_name + '{\n'

        columns_parsed = dataframe.columns.to_numpy()
        data_parsed = dataframe.to_numpy()

        tables_text[dataIndex] += '['

        for indexText in columns_parsed:
            text_replaced = replace_text(indexText)
            tables_text[dataIndex] += f'({text_replaced})'
            tables_clean_text[dataIndex] += text_replaced + ' '

        tables_text[dataIndex] += ']\n'

        for row in data_parsed:
            tables_text[dataIndex] += '['
            for rowText in row:
                text_replaced = replace_text(rowText)
                tables_text[dataIndex] += f'({text_replaced})'
                tables_clean_text[dataIndex] += text_replaced + ' '

            tables_text[dataIndex] += ']\n'
        tables_text[dataIndex] += '}\n'
        tables_clean_text[dataIndex] = remove_spaces(tables_clean_text[dataIndex][:-1])

    reader = PdfReader(file_path)  # open PDF and read all

    all_text = ''

    for page in reader.pages:
        all_text += page.extract_text()

    all_text_formatted = replace_text(all_text)

    indexes = [[0, 0] for _ in range(len(tables))]
    for num, raw in enumerate(tables_clean_text):
        indexes[num][0], indexes[num][1] = find_no_spaces(all_text_formatted,
                                                          raw)  # get indexes of tables in the main text

    num_len = len(indexes) - 1

    for num, index in enumerate(reversed(indexes)):
        all_text = replace_from_index(all_text, index[0], index[1],
                                      tables_text[num_len - num])  # replace not formatted tables with formatted ones

    return all_text
