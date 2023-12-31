import openpyxl
import os

def parser(file):
    wb = openpyxl.load_workbook(f'VLAD/ЕБУЧИЕ ВАГОНЫ/{file}')

    sheet = wb.get_sheet_by_name('Лист1')

    print(file)

    with open(f"VLAD/ЕБУЧИЕ ВАГОНЫ YML/{file[:-5]}.yml", "w", encoding = "UTF-8") as file:
        i = 1

        while sheet[f'B{i}'].value != "end":
            if sheet[f'A{i}'].value != None:
                
                k = i + 1
                while sheet[f'A{k}'].value == None:
                    k += 1
                    if k == 10485: return 0
                
                if i != k - 1:
                    if sheet[f"C{i + 1}"].value == None: 
                            
                        string = f"{sheet[f'B{i}'].value}".replace(".", "").strip() + " " + f"{sheet[f'C{i}'].value}".replace(".", "").strip()

                        file.write("- - " + string + "?\n")

                        for j in range(i, k):
                            string = f"{sheet[f'D{j}'].value}".replace(".", "").strip()

                            file.write("  - " + string + ".\n")
                            
                    else:
                        string = f"{sheet[f'B{i}'].value}".replace(".", "").strip()

                        file.write("- - " + string + "?\n")

                        for j in range(i, k):
                            if sheet[f'C{i}'].value != None:  
                                
                                string = f"  - {sheet[f'C{j}'].value}".replace(".", "").strip()
                                file.write("  - " + string + ".\n")

                        for j in range(i, k):
                            string = f"{sheet[f'D{j}'].value}".replace(".", "").strip()
                            file.write("  - " + string + ".\n")

                else:
                    string = f"{sheet[f'B{i}'].value}".replace(".", "").strip() + " " + f"{sheet[f'C{i}'].value}".replace(".", "").strip()

                    file.write("- - " + string + "?\n")
                    
                    string = f"{sheet[f'D{i}'].value}".replace(".", "").strip()

                    file.write("  - " + string + ".\n")

            print(f"{i} {k}")
            i = k

for file in os.listdir("./VLAD/ЕБУЧИЕ ВАГОНЫ"):
            if file.endswith(".xlsx"):
                parser(file)