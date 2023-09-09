import openpyxl

wb = openpyxl.load_workbook('VLAD/20.xlsx')

sheet = wb.get_sheet_by_name('Лист1')

with open("VLAD/20.txt", "w", encoding = "UTF-8") as file:
    i = 1

    while sheet[f'B{i}'].value != "end":
        if sheet[f'A{i}'].value != None:
            
            k = i + 1
            while sheet[f'A{k}'].value == None:
                k += 1
            
            if i != k - 1:
                if sheet[f"C{i + 1}"].value == None:
                    file.write(f"--{sheet[f'B{i}'].value}" + " " + f"{sheet[f'C{i}'].value}\n")

                    for j in range(i, k - 1):
                        file.write(f"-{sheet[f'D{i}'].value}" + "\n")
                        
                else:
                    file.write(f"--{sheet[f'B{i}'].value}")

                    for j in range(i, k - 1):
                        if sheet[f'C{i}'].value != None:  
                            file.write(f"-{sheet[f'C{i}'].value}" + "\n")

                    for j in range(i, k - 1):
                        file.write(f"-{sheet[f'D{i}'].value}" + "\n")

            else:
                file.write(f"--{sheet[f'B{i}'].value}" + " " + f"{sheet[f'C{i}'].value}\n")
                file.write(f"-{sheet[f'D{i}'].value}" + "\n")

        i = i + 1
        print(i)
        if i == 900: exit(0)