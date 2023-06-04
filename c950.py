import csv

#2-Create Package and Truck objects and have packageCSV and distanceCSV and addressCSV files ready
#3-Create loadPackageData(HashTable) to 
#- read packages from packageCSV file (see C950 - Webinar-2 - Getting Greedy, who moved my data  webinar) 
#- update Package object
# insert Package object into HashTable with the key=PackageID and Item=Package

class Package:
    def __init__(self, packageID, address, city, state, zip, deadline, mass, notes):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes

    def getAddressNumber(self):
        for entry in Distances.nameTable:
            if self.address == entry[1]: return Distances.nameTable.index(entry)

class ChainingHashTable:
    def __init__(self): 
        self.table = []
        for i in range(10): self.table.append([])

    def insert(self, key, value):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key: 
                kv[1] = value
                return
        
        bucket_list.append([key, value])

    def get(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key: return kv[1]
        
        return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key: bucket_list.remove([kv[0],kv[1]])

class Truck:
    def __init__(self, packages):
        self.packages = packages
        self.speed = 18

    def deliver(self):
        for package in self.packages:
            return

def PackageTable():
    packages = ChainingHashTable()
    with open('./packageTable.csv',mode = 'r', encoding='utf-8-sig') as csvfile:
        packageEntries = list(csv.reader(csvfile))

    for p in packageEntries:
        key = int(p[0])
        value = Package(key, p[1], p[2], p[3], p[4], p[5], p[6], p[7])
        packages.insert(key, value)

    return packages

class DistanceTable():
    def __init__(self):
        self.nameTable = []
        self.distanceTable = []
        with open('./distanceTable.csv',mode = 'r', encoding='utf-8-sig') as csvfile:
            entries = list(csv.reader(csvfile))
        for entry in entries:
            self.nameTable.append([entry[0], entry [1], entry[2]])
            for i in range(3): entry.remove(entry[0])
            self.distanceTable.append(entry)

    def getDistance(self, a, b):
        if a > 26: return None
        if a == b: return 0.0, None, None
        distance = self.distanceTable[a][b]

        if distance == '': return float(self.distanceTable[b][a]), self.nameTable[a], self.nameTable[b]
        return float(distance), self.nameTable[a], self.nameTable[b]
    
Packages = PackageTable()
Distances = DistanceTable()