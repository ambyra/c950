import csv, pprint

#A) Package data steps:
#1-Create HashTable data structure (See C950 - Webinar-1 - Let’s Go Hashing webinar)


#2-Create Package and Truck objects and have packageCSV and distanceCSV and addressCSV files ready
#3-Create loadPackageData(HashTable) to 
#- read packages from packageCSV file (see C950 - Webinar-2 - Getting Greedy, who moved my data  webinar) 
#- update Package object
# insert Package object into HashTable with the key=PackageID and Item=Package

class Package:
    #Package ID, Address, City , State, Zip, Delivery Deadline , Mass KILO , Special Notes,
    def __init__(self, packageID, address, city, state, zip, deadline, mass, notes):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes

        def __str__(self):
            return self.packageID

    #def print(self):
     #   print(self.packageID, self.address, self.city, self.state, se)

#From C950 webinar 1 "lets go hashing"
class ChainingHashTable:
    def __init__(self, initial_capacity=10):
        self.table = []
        self.currentIndex = 0
        for i in range(initial_capacity):
            self.table.append([])
      
    def insert(self, key, value):
        bucket = hash(key) % len(self.table)
        print(bucket)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = value
        
        kv = [key, value]
        bucket_list.append(kv)

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            print (kv[0], kv[1])
            if kv[0] == key:
                return kv[1]
        
        return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0],kv[1]])
                return True
        
        return False

with open('./distanceTable.csv',mode = 'r', encoding='utf-8-sig') as csvfile:
    distanceTable = list(csv.reader(csvfile))

with open('./packageTable.csv',mode = 'r', encoding='utf-8-sig') as csvfile:
    packageTable = list(csv.reader(csvfile))

Packages = ChainingHashTable()
for package in packageTable:
    key = int(package[0])
    value = Package(key, package[1], package[2], package[3], package[4], package[5], package[6], package[7])
    Packages.insert(key, value)
    
print(Packages.search(1))