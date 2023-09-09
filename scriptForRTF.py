# Открываем RTF файл
with open('Перечень неисправностей.rtf', 'r') as rtf_file:
    doc = rtf_file.read(rtf_file)

# Поиск и обработка таблиц
for element in doc.va:
    if isinstance(element, TextReader.Table):
        table = element
        # table содержит данные о таблице, вы можете обработать ее здесь

        # Получите количество строк и столбцов в таблице
        num_rows = len(table.rows)
        num_cols = len(table.rows[0].cells)

        # Обход строк и столбцов
        for row in table.rows:
            for cell in row.cells:
                # Извлеките текст из каждой ячейки
                cell_text = ''.join(cell.content)
                print(cell_text)

