import csv

def m2h(minutes):
    hours = str(int(minutes//60))
    mins = str(int(minutes%60))
    if len(mins)== 1: mins = '0' + mins
    return hours + ':' + mins

class ChainingHashTable:
    #1-Create HashTable data structure (See C950 - Webinar-1 - Let’s Go Hashing webinar)
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

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key: bucket_list.remove([kv[0],kv[1]])

class DistanceTable():
    #2-Create Package and Truck objects and have packageCSV and distanceCSV and addressCSV files ready
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
        if a == b: return 0.0
        distance = self.distanceTable[a][b]

        if distance == '': return float(self.distanceTable[b][a])
        return float(distance)
    
    def getName(self, index): return str(self.nameTable[index][0])
    
def PackageTable():
    #2-Create Package and Truck objects and have packageCSV and distanceCSV and addressCSV files ready
    packages = ChainingHashTable()
    #- read packages from packageCSV file (see C950 - Webinar-2 - Getting Greedy, who moved my data  webinar) 
    with open('./packageTable.csv',mode = 'r', encoding='utf-8-sig') as csvfile:
        packageEntries = list(csv.reader(csvfile))

    #3-Create loadPackageData(HashTable) to 
    #- update Package object
    for p in packageEntries:
        key = int(p[0])

        #parse deadline into minutes after 0000
        deadlineText = p[5]
        deadline = 24 * 60
        if deadlineText == '10:30 AM': deadline = (10*60 ) + 30
        if deadlineText == '9:00 AM': deadline = 9 * 60
        
        value = Package(key, p[1], p[2], p[3], p[4], deadline, p[6], p[7])
        # insert Package object into HashTable with the key=PackageID and Item=Package
        packages.insert(key, value)

    return packages

class Package:
    #2-Create Package and Truck objects and have packageCSV and distanceCSV and addressCSV files ready
    Distances = DistanceTable()
    def __init__(self, ID, address, city, state, zip, deadline, mass, notes):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        self.addressIndex = self.getAddressIndex()
        self.timeDelivered = None
        self.isDelivered = False

    def __str__(self): return 'Package: ' + str(self.ID)

    def getAddressIndex(self):
        for entry in Package.Distances.nameTable:
            if self.address == entry[1]: return Package.Distances.nameTable.index(entry)

class Truck:
    #2-Create Package and Truck objects and have packageCSV and distanceCSV and addressCSV files ready
    Distances = DistanceTable()
    Speed = 18 / 60
    StartTime = 8 * 60
    MaxPackages = 16
    MaxMileage = 140.0
    Hub = 0
    def __init__(self, truckName):
        self.name = str(truckName)
        self.packages = []
        self.currentTime = Truck.StartTime
        self.milesTraveled = 0
        self.addressIndex = 0

    def travel(self, destinationIndex):
        distance = Truck.Distances.getDistance(self.addressIndex, destinationIndex)
        
        self.currentTime += distance / self.Speed
        self.milesTraveled += distance
        self.addressIndex = destinationIndex

        if self.milesTraveled > self.MaxMileage:
            print('*** ERROR: Truck ' + str(self.truckName) + ' exceeded max mileage')

    def load(self, package):
        if len(self.packages) > self.MaxPackages:
            print('*** ERROR: Truck ' + str(self.truckName) + ' exceeded max packages')
            return
        self.packages.append(package)

    def getClosestPackage(self):
        lowestDistance = 100
        currentPackage = None

        for package in self.packages:
            if package.isDelivered: continue

            #determine if truck has enough miles to deliver package and return to hub
            distanceToDeliveryAddress = Truck.Distances.getDistance(self.addressIndex, package.addressIndex)
            distanceToHubFromDeliveryAddress = Truck.Distances.getDistance(package.addressIndex, Truck.Hub)
            travelDistance = self.milesTraveled + distanceToDeliveryAddress + distanceToHubFromDeliveryAddress
            if travelDistance > Truck.MaxMileage: continue

            #determine if package is closest package to current location
            if distanceToDeliveryAddress < lowestDistance: 
                currentPackage = package
                lowestDistance = distanceToDeliveryAddress
        return currentPackage
    
    def deliverPackages(self):
        for i in range(len(self.packages)):
            package = self.getClosestPackage()
            if package:
                #optimal package found

                fromLocation = str(self.Distances.getName(self.addressIndex))
                toLocation = str(self.Distances.getName(package.addressIndex))
                travelDistance = str(self.Distances.getDistance(self.addressIndex, package.addressIndex))

                #move truck to delivery address; deliver package
                self.travel(package.addressIndex)
                package.timeDelivered = self.currentTime
                package.isDelivered = True

                #report
                print('Package ' + str(package.ID) +
                      ', on Truck ' + str(self.name) +
                      ', delivered at ' + m2h(package.timeDelivered) + 
                      ', from ' + fromLocation + 
                      ', to ' + toLocation +
                      ', travel distance: ' + travelDistance + ' miles'
                )
                
                if package.timeDelivered > package.deadline:
                    print('*** Error: package ' + str(package.ID) + 
                          ' with deadline: ' + str(m2h(package.deadline)) +
                          ' delivered at ' + str(m2h(package.timeDelivered)))

        #all deliverable packages delivered; return to hub
        self.travel(Truck.Hub)

        #return undelivered packages to hub
        undeliveredPackages = []
        for package in self.packages:
            if not package.isDelivered: undeliveredPackages.append(package)
        Hub.extend(undeliveredPackages)

        #unload truck
        self.packages = []

        #report 
        time = str(m2h(self.currentTime))
        message = 'Truck ' + self.name + ' returned to hub at ' + time + ' with ' + str(self.milesTraveled) + ' miles, '
        if len(undeliveredPackages) == 0:
            print (message + ' with no undelivered packages')
        else:
            print (message + ' with following undelivered packages: ' + str(undeliveredPackages))

#make trucks
Truck1 = Truck(1)
Truck2 = Truck(2)
Truck3 = Truck(3)

#make hub
Hub = []

#load trucks
Packages = PackageTable()
for i in range(1,41):
    currentPackage = Packages.get(i)
    if currentPackage.notes == 'Can only be on truck 2': Truck2.load(currentPackage)

Truck2.deliverPackages()