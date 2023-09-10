import num2words as num

row="Hello, I'm Peter and me 25 years old. My hooby it's swim on Throughout 8 years"

numList=[]

for i in 10:
    numList.append(i)

for i in range(len(row.strip())):
    for j in range(len(numList)):
        if (row[i]==str(numList[j] and row[i+1]==str(numList[j]))):
            pass


