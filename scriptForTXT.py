import os
import codecs
import 

def readFile(filepath,fileName,exitValue):
    output=""
    newFileName=1
    with codecs.open(filepath+fileName,encoding='utf-8',mode="r") as file:
        lines = file.readlines()
        for line in lines:
            if (line.startswith(exitValue)):
                        if (len(line.strip()) == 1):
                            with codecs.open(f"{filepath}\{str(newFileName)}.txt",encoding='utf-8',mode="w") as new_file:
                                new_file.write(output)
                            print(f"Was created {str(newFileName)}.txt in {filepath}")
                            newFileName=newFileName+1
                            output=""
                            continue
            
            output+=line
        # print(output)

def changeFileForDataSet(filepath,fileName):
    pass

readFile(r"C:\Users\User\Desktop\IVA-main","\\noser2.txt","1")
                
#C:\Users\User\Desktop\IVA-main\Перечень-неисправностей.txt
# if not os.path.isfile(f"{filepath}/{fileName}"):