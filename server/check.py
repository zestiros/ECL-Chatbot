import re

regex= re.compile('^[0-9]*$')

def check():
    reqFile=open('requierments.txt')
    script=open('chatbot_ecl.py')
    found=-1

    
    for line in reqFile:
        a=''
        for i in line:
            if i != '=' and i !='.' and not regex.match(i):
                a+=i
        print(a)
        if found==2:
            print()
            break
        elif found > 0:
            found+=1
        else:
            for line2 in script:
                # print (line2)
                if a in line2:
                    print(line2)
                    found=1

check()
