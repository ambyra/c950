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
        value = Package(key, p[1], p[2], p[3], p[4], p[5], p[6], p[7])

        #parse deadline into minutes after 0000
        if value.deadline == 'EOD':
            value.deadline = 24 * 60
        if value.deadline == '10:30 AM':
            value.deadline = (10*60 ) + 30
        if value.deadline == '9:00 AM': 
            value.deadline = 9 * 60

        #set availability time
        value.timeAvailable = 8 * 60
        delayed ='Delayed on flight---will not arrive to depot until 9:05 am'
        if value.note == delayed: value.timeAvailable = (9 * 60) + 5

        # insert Package object into HashTable with the key=PackageID and Item=Package
        packages.insert(key, value)

    return packages

class Package:
    #2-Create Package and Truck objects and have packageCSV and distanceCSV and addressCSV files ready
    Distances = DistanceTable()
    def __init__(self, ID, address, city, state, zip, deadline, mass, note):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.note = note

        self.addressIndex = self.getAddressIndex()
        self.timeAvailable = 8 * 60
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
        self.time = Truck.StartTime
        self.miles = 0
        self.addressIndex = 0

        self.driver = None

    def travel(self, destinationIndex):
        distance = Truck.Distances.getDistance(self.addressIndex, destinationIndex)
        
        self.time += distance / self.Speed
        self.miles += distance
        self.addressIndex = destinationIndex

        if self.miles > self.MaxMileage:
            print('*** ERROR: Truck ' + str(self.name) + ' exceeded max mileage')

    def load(self, package):
        self.packages.append(package)
        if len(self.packages) > Truck.MaxPackages:
            print('*** ERROR: Truck ' + str(self.name) + ' exceeded max packages')
            return

    def getClosestPackage(self):
        lowestDistance = 100
        currentPackage = None

        for package in self.packages:
            if package.isDelivered: continue

            #determine if truck has enough miles to deliver package and return to hub
            distanceToDeliveryAddress = Truck.Distances.getDistance(self.addressIndex, package.addressIndex)
            distanceToHubFromDeliveryAddress = Truck.Distances.getDistance(package.addressIndex, Truck.Hub)
            travelDistance = self.miles + distanceToDeliveryAddress + distanceToHubFromDeliveryAddress
            if travelDistance > Truck.MaxMileage: continue

            #determine if package is closest package to current location
            if distanceToDeliveryAddress < lowestDistance: 
                currentPackage = package
                lowestDistance = distanceToDeliveryAddress

            #determine if package will arrive late if not delivered next
            deliveryTime = self.time + distanceToDeliveryAddress/Truck.Speed
            if deliveryTime + 45 > package.deadline:
                return package
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
                package.timeDelivered = self.time
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

        #unload truck
        self.packages = []

        #report 
        time = str(m2h(self.time))
        message = 'Truck ' + self.name + ' returned to hub at ' + time + ' with ' + str(self.miles) + ' miles, '
        numUndelivered = len(undeliveredPackages)
        if numUndelivered == 0:
            print (message + ' with no undelivered packages')
        else:
            print (message + ' with ' + str(numUndelivered)+ ' undelivered packages: ')
            for package in undeliveredPackages: print(package)

class Driver:
    def __init__(self, name):
        self.name = str(name)
        self.truck = None
        self.addressIndex = self.getLocation()

    def getLocation(self):
        if(self.truck == None): return 0
        return self.truck.addressIndex

class Hub:
    PackagesHashTable = PackageTable() #all packages

    def __init__(self):
        self.Packages = [] #packages remaining at hub
        for i in range(1,41):
            package = Hub.PackagesHashTable.get(i)
            self.Packages.append(package)

            self.Truck1 = Truck(1)
            self.Truck2 = Truck(2)
            self.Truck3 = Truck(3)

    def getPackage(self):
        package = self.Packages[0]
        self.Packages.remove(package)
        return(package)

    def returnPackage(self, package): self.Packages.append(package)

    def loadTrucks(self):
        noteDelayed ='Delayed on flight---will not arrive to depot until 9:05 am'
        noteWrongAddress = 'Wrong address listed'
        noteTruck2 = 'Can only be on truck 2'

        for i in range(len(self.Packages)):
            package = self.getPackage()
            if package == None: return

            t1NumPackages = len(self.Truck1.packages)
            t2NumPackages = len(self.Truck2.packages)
            t3NumPackages = len(self.Truck3.packages)

            #load truck 1 and truck 2 evenly
            truck = self.Truck1
            if t2NumPackages < t1NumPackages: 
                truck = self.Truck2

            #is package for truck 2?
            if package.note == noteTruck2:
                self.Truck2.load(package)
                continue

            #load low priority packages on truck 3
            if package.deadline == 24*60 and t3NumPackages < Truck.MaxPackages:
                self.Truck3.load(package)
                continue

            #is package available? noteDelayed
            if truck.time >= package.timeAvailable:
                truck.load(package)
                continue

            #package not loaded onto any truck, return to hub
            self.returnPackage(package)

def packageStatus():
    print('--- hub ---')
    for package in hub.Packages: print(package)
    print('--- t1 ---')
    for package in hub.Truck1.packages: print(package)
    print('--- t2 ---')
    for package in hub.Truck2.packages: print(package)
    print('--- t3 ---')
    for package in hub.Truck3.packages: print(package)

hub = Hub()
hub.loadTrucks()

#packageStatus()
#driver 1 deliver packages and return to hub
hub.Truck1.deliverPackages()

#driver 2 deliver packages and return to hub
hub.Truck2.deliverPackages()

#driver returning first delivers delayed packages
#driver returning last delivers low priority packages on truck 3
if hub.Truck1.time < hub.Truck2.time:
    for package in hub.Packages: hub.Truck1.load(package)
    hub.Packages = []
    hub.Truck1.deliverPackages()
    hub.Truck3.time = hub.Truck2.time
    hub.Truck3.deliverPackages()
else:
    for package in hub.Packages: hub.Truck2.load(package)
    hub.Packages = []
    hub.Truck2.deliverPackages()
    hub.Truck3.time = hub.Truck1.time
    hub.Truck3.deliverPackages()

packageStatus()

#todo round miles
#p9 wrong address listed


