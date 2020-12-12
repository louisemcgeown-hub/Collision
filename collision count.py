import sqlite3
import time
import zlib

conn = sqlite3.connect('new collisions ALL.sqlite')
cur = conn.cursor()

count = 10

types = {'22350': 'Unsafe Speed',
         '22107' : 'Unsafe Turn or Lane Change',
         '21453A' : 'Red Signal Violation',
         '23152A' : 'Driving Under the Influence',
         '22106' : 'Unsafe Starting or Backing on Highway',
         '' : 'No Cause Given',
         '21801A' : 'Violation of Right-of-Way–Left Turn',
         '21804A' : 'Entering Highway From Alley or Driveway',
         '21950A' : 'Failure to Yield at Crosswalk',
         '21658A' : 'Lane Straddling/Failure to Use Specified Lanes'
         }


cur.execute('SELECT violation FROM Indicents')
pcause = dict()

for data_row in cur :
    # store a dictionary entry if not already there, increment entry count
    pcause[data_row[0]] = pcause.get(data_row[0], 0) + 1

print("Top", count, "Accident Types")
# This one line replaces the above code
# We make a list of reversed tuples and then store it. DYNAMICALLY!
lst = sorted([(v, k) for k, v in pcause.items()], reverse = True)

# lst is (val, key)
for val, key in lst[:count] :
    print(key, types[key], val)

fhand = open('collision count.js','w')
fhand.write("collision = [ ['Violation'")
# lst is (val, key)
for val, key in lst[:count] :
    fhand.write(",'"+types[key]+"'")
fhand.write("],")

fhand.write("\n['Count'")
# lst is (val, key)
for val, key in lst[:count] :
    fhand.write(",")
    fhand.write(str(val))

fhand.write("]");

fhand.write("\n];\n")
fhand.close()

cur.close() # close the connection to the database

print("Output written to collisionCount.js")
print("Open collision count.htm to visualize the data")
