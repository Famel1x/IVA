from num2words import num2words
input_str = "I5 have5 apples and 10 oranges"
#istr2 = ""
def convert_numbers_to_words(istr2):
    result = []
    words = istr2.split()

    for word in words:
        if word.isdigit():
            number = int(word)
            word_in_words = num2words(number)
            result.append(word_in_words)
        else:
            result.append(word)

    return ' '.join(result)





for i in range(0, len(input_str)):
    start=0
    end=0
    for j in range(0, len(input_str)):
        if input_str[j].isdigit():
            start=j
            end=j
            for e in range(0, len(input_str)):
                if input_str[j+1].isdigit():
                    end=j+1
                else:break
                istr2=""
                for s in range(start, end):
                    istr2=istr2+input_str[s]
input_str=input_str[:start] + " " + convert_numbers_to_words(istr2) + " " + input_str[end:]
print(input_str)
       
       

    
