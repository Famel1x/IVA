import openpyxl

wb = openpyxl.load_workbook('VLAD/20.xlsx')

sheet = wb.get_sheet_by_name('Лист1')

with open("VLAD/20.yml", "w", encoding = "UTF-8") as file:
    i = 1

    while sheet[f'B{i}'].value != "end":
        if sheet[f'A{i}'].value != None:
            
            k = i + 1
            while sheet[f'A{k}'].value == None:
                k += 1
            
            if i != k - 1:
                if sheet[f"C{i + 1}"].value == None:
                    file.write(f"--{sheet[f'B{i}'].value}" + " " + f"{sheet[f'C{i}'].value}\n")

                    for j in range(i, k):
                        file.write(f" -{sheet[f'D{j}'].value}" + "\n")
                        
                else:
                    file.write(f"--{sheet[f'B{i}'].value}")

                    for j in range(i, k):
                        if sheet[f'C{i}'].value != None:  
                            file.write(f" -{sheet[f'C{j}'].value}" + "\n")

                    for j in range(i, k):
                        file.write(f" -{sheet[f'D{j}'].value}" + "\n")

            else:
                file.write(f"--{sheet[f'B{i}'].value}" + " " + f"{sheet[f'C{i}'].value}\n")
                file.write(f" -{sheet[f'D{i}'].value}" + "\n")

        print(f"{i} {k}")
        i = k
        if i == 3000: exit(0)