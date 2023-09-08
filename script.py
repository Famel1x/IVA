def readAndUploadFile(filepath,exitValue):
    output=""
    with open(filepath,"r") as file:
            for line in file.readline():
                  if (exitValue in line):
                        break
                  output+=line
    
    print(output)

readAndUploadFile("C:\Users\User\Desktop\IVA-main\ test.txt","1")
                
#C:\Users\User\Desktop\IVA-main\Перечень-неисправностей.txt