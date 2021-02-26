import re, sys, os

input_dict = {}
#print(sys.argv)

input_word = open(sys.argv[1],'r')

output_dict = open(sys.argv[2], 'w+')


words = (input_word.read()).lower()

for i in sorted(re.split("[\W]", words)):
    if len(i) >0: #removes quirk from split of empty strings
        input_dict[i] = input_dict.get(i,0)+1 #key is input[i] data in .get(i,0)


#print(input_dict)
for j in input_dict:
    data = str(j)+" "+str(input_dict.get(j))+"\n"
    output_dict.write((data))

#output_dict.write(str(input_dict))
input_word.close()
output_dict.close()
