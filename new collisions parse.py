import csv
import sqlite3

print ("Parse Collision Data")

def parsestreet(intersection):
    # returns the two separate streets from the intersection given
    ampersand = intersection.find(" - ")
    st1 = intersection[:(ampersand)]
    st2 = intersection[(ampersand + 3):]
    return(st1.title(), st2.title())

def parsestring(inputdata):
    # returns the value input string '# Inj: #' or '# Killed: '
    colon = inputdata.find(": ")
    return(inputdata[(colon + 1):])

conn = sqlite3.connect('new collisions ALL.sqlite')
cur = conn.cursor()


cur.execute('DROP TABLE IF EXISTS Indicents')

cur.execute('''CREATE TABLE IF NOT EXISTS Indicents
    (id TEXT UNIQUE, date TEXT, time TEXT, day TEXT, intersection TEXT,
     street1 TEXT, street2 TEXT, distance TEXT, lighting TEXT, weather TEXT, atfault TEXT,
     category TEXT, sobriety TEXT, gender TEXT, age INTEGER,
     violation TEXT, injcount INTEGER, deathcount INTEGER)''')
## injured and killed being stored as text for now; need to extract the number from the string

#with open('new collisions.csv', newline='') as csvfile:
with open('../new collisions long.csv', newline='') as csvfile:
    rawdata = csv.reader(csvfile, delimiter= ',')
    count = 0
    writetodatabase = False
    for row in rawdata:
        count = count + 1
        if count < 3 : continue # ignore first two rows
        if len(row[2]) > 2:
            # new incident
            writetodatabase = False
            id = row[2]
            date = row[3]
            time = row[4]
            day = row[5]
            intersection = row[6].title()
            street1, street2 = parsestreet(row[6])
            distance = row[7]
            #stdistance = row[5]
            #stdirection = row[6]
            lighting = row[9]
            weather = row[10]
            atfault = row[11]
            category = row[12]
            violation = row[15]
            if len(row[18]) > 7:
                injured = int(parsestring(row[18]))
            else:
                injured = 0
            if len(row[19]) > 10:
                killed = int(parsestring(row[19]))
            else:
                killed = 0
            #print(id, date, time, street1, street2, primarycause)

        if row[20].startswith("Party 1") and writetodatabase == False:
            # driver information. Only store the first driver for now
            if len(row[25]) > 5:
                age = int(parsestring(row[25]))
            else:
                age = 0 # not defined
            sobriety = parsestring(row[32])
            writetodatabase = True



        if writetodatabase == True:
            writetodatabase = False
            cur.execute('''INSERT INTO Indicents (id, date, time, day, intersection, street1, street2, distance,
                lighting, weather, atfault, category, sobriety, violation, injcount, deathcount)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (id, date, time, day, intersection,
                street1, street2, distance, lighting, weather, atfault, category, sobriety, violation, injured, killed))

        if count % 50 == 0 :
            conn.commit()
            print(".")

# one final conn.commit() at the end
conn.commit()
print('finished parsing csv file')
