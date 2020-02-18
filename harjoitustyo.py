######################################################################
# CT60A0202 Ohjelmoinnin ja data-analytiikan perusteet
# Tekijä: Jan Saariniemi
# Opiskelijanumero: 0443233
# Päivämäärä: 21.11.2018
# Yhteistyö ja lähteet, nimi ja yhteistyön muoto: luentomateriaali, ohjelmointiopas,
#https://snakify.org/en/lessons/two_dimensional_lists_arrays/
#https://stackoverflow.com/questions/625083/python-init-and-self-what-do-they-do
#https://stackoverflow.com/questions/39402795/how-to-pad-a-string-with-leading-zeros-in-python-3/39402910
# HUOM! KAIKKI KURSSIN TEHTÄVÄT OVAT HENKILÖKOHTAISIA!
######################################################################
import sys
import datetime

class dailydata: # CREATES THE OBJECTS WHICH ARE USED TO ANALYSE THE DATA
    time = ""
    power = ""
    def __init__(self, time, power):
        self.time = time
        self.power = power
    def printtime(self):
        return self.time.strftime("%d.%m.%Y %H:%M")

def panel():
    print("Anna haluamasi toiminnon numero seuraavasta valikosta:")
    print("1) Lue sähköntuotantotiedot")
    print("2) Analysoi päivätuotanto")
    print("3) Tallenna päivätuotanto")
    print("4) Analysoi kuukausituotanto")
    print("5) Analysoi tuntituotanto")
    print("6) Tallenna kuukausituotanto")
    print("7) Tallenna tuntituotanto")
    print("0) Lopeta")
    choice = int(input("Valintasi: "))
    return choice

#READ

def readcvs(): # READS THE CSV FILE, MAKES SOME MODIFICATIONS AND SAVE THE DATA IN TO A LIST
    dataset = []
    name = "HTViope2016.csv"
    #name = input("Anna luettavan tiedoston nimi: ")
    year = int(input("Anna analysoitava vuosi: "))
    try:
        file = open(name,"r",encoding="utf-8")
    except:
        print("Tiedoston '"+name+"' lukeminen epäonnistui, ei löydy, lopetetaan.")
        sys.exit()
        
    line = file.readline()
    while True:
        line = file.readline()
        if line =="":
            break
        temp = line.split(";")
        time = temp[0]; power = 0
        for i in temp[1:8]:
            i = float(i); power = power +i    
        if power <0: # CLEANING THE DATA FROM NEGTIVE LINES 
            power = 0
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        data = dailydata(time, power)
        dataset.append(data)
    file.close()
    print("Tiedosto '"+name+"' luettu, "+str(len(dataset)+1)+" riviä, "+str(len(dataset))+" otettu analysoitavaksi.")
    print("Analysoidaan "+dataset[0].printtime() +" ja "+dataset[len(dataset)-1].printtime()+" välistä dataa."); print("")
    time = time + datetime.timedelta(days=1); power = 0; data = dailydata(time, power); dataset.append(data)# ADDING A NEW DAY FOR THE FUTURE LOOPING
    return dataset, year

#ANALYSE

def analysedaily(dataset, year): #FUNCTION'S PURPOSE IS TO ANALYSE DAILY DATA: USING A LOOP AND IF-CONDITIONS TO ALLOCATE THE RIGHT POWERS PER DAY
    temp = []
    for j in dataset:
        if j == dataset[0]: # REFERENCE POINT
            compare = j.time
            power = j.power
        elif compare.day != j.time.day:#SAVING AND FORMATING
            data = dailydata(compare, power)
            temp.append(data)
            compare = j.time 
            power = j.power
        else:
            power += j.power
    processed = temp
    print("Päivätuotanto analysoitu."); print("")
    return processed, year

def analysemontly(dataset,year): #FUNCTION'S PURPOSE IS TO ANALYSE MONTHLY DATA: USING A LOOP AND IF-CONDITIONS TO ALLOCATE THE RIGHT POWERS PER MONTH
    temp = []
    for j in dataset:
        if j == dataset[0]: # REFERENCE POINT
            compare = j.time
            power = j.power
        elif compare.month != j.time.month:#SAVING AND FORMATING
            compare = compare.month
            data = dailydata(compare, power)
            temp.append(data)
            compare = j.time 
            power = j.power
        else: # ADDING 
            power += j.power
    processed = temp
    print("Kuukausituotanto analysoitu.");print("")
    return processed,year

def analysehourly(data,year):#FUNCTION'S PURPOSE IS TO ANALYSE HOURLY DATA: USING A LOOP AND IF-CONDITIONS TO ALLOCATE THE RIGHT POWERS PER HOURS. REQUIRED MAKING A "MATRIX"
    temp = [[0 for j in range(24)] for i in range(12)] #MAKING THE "DF" WITH ZEROS
    for i in data:
            month = i.time.month-1
            hour = i.time.hour
            temp[month][hour] += (i.power)
    processed = temp
    print("Tuntituotanto analysoitu.");print("")
    return processed,year

#SAVE 

def savedaily(processed, year): #FUNCTION'S PURPOSE IS TO SAVE DAILY DATA: USES 2 LOOPS , HANDLES ALL POSSIBLE ERRORS WHILE HANDLING FILE, WRITING IS DONE IN 2 PARTS
    name= "tulosPaivajee"+str(year)+".csv"
    twoemptylines = "\n"+"\n"
    title = "Päivittäinen sähköntuotanto:\n"
    title2 = "Kumulatiivinen päivittäinen sähköntuotanto:\n"
    date = ";"+str(year)+"\n"
    
    try:
        #WRITING DAILY
        file = open(name,"w",encoding="utf-8")
        file.write(title)
        file.write(date)
        for i in processed:
            dayf =  i.time.strftime("%d.%m.%Y")
            power = int(i.power)
            line = (dayf+";"+str(power)+"\n") # CREATING THE ACTUAL DATA LINE
            file.write(line)
        file.write(twoemptylines)
        file.close()
    except:
        print("Tallennus epäonnistui, palataan valikkoon.")
        return
    
    try:
        file = open(name,"a",encoding="utf-8") 
        file.write(title2)
        file.write(date)
        power = 0
        for i in processed:
            dayf =  i.time.strftime("%d.%m.%Y")
            power = power +i.power
            line = (dayf+";"+str(int(power))+"\n")# CREATING THE ACTUAL DATA LINE
            file.write(line)
        file.write(twoemptylines)
        file.close()
    #ENDING WRITING
    except:
        print("Tallennus epäonnistui, palataan valikkoon.")
        return
    
    print("Päivätuotanto tallennettu tiedostoon '"+str(name)+"'.");print("")
    return

def savemonthly(processed,year): #FUNCTION'S PURPOSE IS TO SAVE DAILY DATA: USES 1 LOOP , HANDLES ALL POSSIBLE ERRORS WHILE HANDLING FILE
    name= "tulosKuukausi"+str(year)+".csv"
    twoemptylines = "\n"+"\n"
    title = "Kuukausittainen sähköntuotanto:\n"
    share = ";"+str(year)+";%-osuus\n"
    total = 0
    
    for i in processed: #SUMMING UP THE POWERS
        total = total+i.power
        
    try:
        #WRITING MONTHS 
        file = open(name,"w",encoding="utf-8")  
        file.write (title)
        file.write(share)
        for i in processed:
            time = str(i.time); time = time.zfill(2) # FILLING NUMBERS WITH ZERO (purkkaratkaisu, en ollut suunnittelut tätä, vaan jouduin etsimään keinon jolla Viope hyväksisi koodini)
            month = ((time)+"/"+str(year)+";")
            line = (" "+month+str(int(i.power))+";"+str(int((i.power/total)*100))+"%\n") # CREATING THE ACTUAL DATA LINE
            file.write(line) 
        overall = ("Yhteensä;"+str(int(total))+"\n")
        file.write(overall)
        file.write(twoemptylines)
        file.close()
        #ENDING WRITING
    except:
        print("Tallennus epäonnistui, palataan valikkoon.")
        return
    
    print("Kuukausituotanto tallennettu tiedostoon '"+str(name)+"'.")
    print("")
    return

def savehourly(processed, year): #FUNCTION'S PURPOSE IS TO SAVE DAILY HOURS: USES 2 LOOPS , HANDLES ALL POSSIBLE ERRORS WHILE HANDLING FILE, WRITING IS DONE IN 2 PARTS
    name= "tulosTunti"+str(year)+".csv"
    title = "Tuntipohjainen sähköntuotanto: "+"\n"
    twoemptylines = "\n"+"\n"
    changemonth = 0
    numhours = ""
    for i in range(0,24):
        numhours+=";"+str(i)
    numhours += "\n"   
    total = [0]*24
    try:
        #WRITING HOURS
        file = open(name,"w",encoding="utf-8")
        file.write(title)
        file.write(numhours)
        for month in processed: #MONTHS IN NUMERICAL FORM FOR WRITING
            changemonth +=1
            whathour = 0
            changemonthC = str(changemonth); changemonthC = changemonthC.zfill(2) # FILLING NUMBERS WITH ZERO (purkkaratkaisu, en ollut suunnittelut tätä, vaan jouduin etsimään keinon jolla Viope hyväksisi koodini)
            front = (" "+(changemonthC)+"/"+str(year))
            line=("")
            for hour in month:
                line = (line+";"+str(int(hour)))
                total[whathour]+=hour
                whathour +=1
            line= (front+line+"\n") # CREATING THE ACTUAL DATA LINE
            file.write(line)
        line=""
        for i in total:
            line=line+";"+str(int(i))# CREATING THE ACTUAL DATA LINE FOR TOTAL POWER PER HOURS
        line = "Yhteensä"+line+"\n"
        file.write(line);
        file.write(twoemptylines)
        file.close()
        #ENDING WRITING  
    except:
        print("Tallennus epäonnistui, palataan valikkoon.")
        return

    title="Yksittäisen tunnin osuus vuosittaisesta sähköntuotannosta:\n"
    powerH = [0]*24
    for month in processed:
        whathour = 0
        for i in month:
            powerH[whathour]+=i #COUNTING THE PORTIONS
            whathour +=1
    totalpower = sum(powerH)
    try:
        #WRITING THE HOURS            
        file = open(name,"a",encoding="utf-8")
        file.write(title)
        file.write(numhours)
        line=("")
        for i in powerH:
            line =(line+";"+str(int((i/totalpower)*100))+"%") # PORTIONS2PERCENTAGES
        line = "%-osuus"+line+"\n"
        file.write(line)
        file.write(twoemptylines) 
        file.close()
        #ENDING WRITING
    except:
        print("Tallennus epäonnistui, palataan valikkoon.")
        return
        
    print("Tuntituotanto tallennettu tiedostoon '"+str(name)+"'."); print("")  
    return


def main():
    while True:
        choice = panel()
        if choice == 1:
            data,year = readcvs()
        elif choice == 2:
            prosessedD,year = analysedaily(data,year)
        elif choice == 3:
            savedaily(prosessedD,year)
        elif choice == 4:
            prosessedM,year = analysemontly(data,year)
        elif choice == 5:
            prosessedH,year = analysehourly(data,year)
        elif choice == 6:
            savemonthly(prosessedM,year)
        elif choice == 7:
            savehourly(prosessedH,year)
        elif choice == 0:
            print("Kiitos ohjelman käytöstä.")
            break
main()
