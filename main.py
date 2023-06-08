#C1: Create an identifying comment within the first line of a file named “main.py” that includes your first name, last name, and student ID.
#first name: Adam
#last name: Byra
#student ID: 010450534

import csv

Messages = []

def m2h(minutes):
    hours = str(int(minutes//60))
    mins = str(int(minutes%60))
    if len(mins)== 1: mins = '0' + mins
    return hours + ':' + mins

#D1  Identify a self-adjusting data structure, such as a hash table, that can be used with the algorithm identified in part A to store the package data.
#Explain how your data structure accounts for the relationship between the data points you are storing.

#The following hash table implementation is used with the nearest neighbor algorithm to store package data.
#Every package is stored here, regardless of its delivery status or location, so that the user can look up the status of any package at any time by referencing the hash table. 

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
        return round(float(distance),2)
    
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
    StatusHub = "Hub"
    StatusTruck = "En Route"
    StatusDelivered = "Delivered"
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
        self.status = Package.StatusHub
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
                package.timeDelivered = int(self.time)
                package.isDelivered = True
                package.status = Package.StatusDelivered

                Hub.snapshot(package.ID, package.timeDelivered)

                #report
                report = 'Package ' + str(package.ID) + ', on Truck ' + str(self.name) + ' DELIVERED ' + ', at ' +toLocation
                #', travel distance: ' + travelDistance + ' miles']
                
                #Messages.append([package.ID, package.timeDelivered, report])
                
                if package.timeDelivered > package.deadline:
                    error = '*** Error: package '
                    error += str(package.ID) + ' with deadline: ' + str(m2h(package.deadline))
                    error += ' delivered at ' + str(m2h(package.timeDelivered))
                    Messages.append([package.ID, package.timeDelivered, error])
        #all deliverable packages delivered; return to hub
        self.travel(Truck.Hub)

        #return undelivered packages to hub
        undeliveredPackages = []
        for package in self.packages:
            if not package.isDelivered: undeliveredPackages.append(package)

        #unload truck
        self.packages = []

        #report
        time = str(m2h(int(self.time)))
        miles = str(round(self.miles, 1))
        message = 'Truck ' + self.name + ' returned to hub at ' + time + ' with ' + miles + ' miles, '
        numUndelivered = len(undeliveredPackages)
        if numUndelivered == 0:
            message += ' with no undelivered packages'
        else:
            message += ' with ' + str(numUndelivered)+ ' undelivered packages: '
            for package in undeliveredPackages: message += (package + '\n')

        Messages.append([0,int(self.time), message])

class Hub:
    PackagesHashTable = PackageTable() #all packages

    def __init__(self):
        self.Packages = [] #packages remaining at hub
        for i in range(1,41):
            package = Hub.PackagesHashTable.get(i)
            package.status = Package.StatusHub
            self.Packages.append(package)
            self.Truck1 = Truck(1)
            self.Truck2 = Truck(2)
            self.Truck3 = Truck(3)

    def getPackage(self):
        package = self.Packages[0]
        self.Packages.remove(package)
        return(package)

    def returnPackage(self, package): self.Packages.append(package)

    #F  Develop a look-up function that takes the following components as input and returns the corresponding data elements: package ID number, delivery address, delivery deadline, delivery city, delivery zip code, package weight, delivery status (i.e., “at the hub,” “en route,” or “delivered”), including the delivery time

    def snapshot(packageID, time):
        p = None
        for i in range(1,41):
            package = Hub.PackagesHashTable.get(i)
            if package.ID == packageID: p = package

        if p == None: 
            print ('no package')
            return    
        
        report = 'Package ID: ' + str(p.ID) + ', Status: ' + p.status +', Deadline: ' + str(m2h(p.deadline)) + ', Address: ' + p.address + ', City: ' + p.city + ', Zip: ' + p.zip + ', Weight: ' + str(p.mass)
        if p.status == Package.StatusDelivered:
            report += ', Delivered: ' + m2h(p.timeDelivered)

        #id, time, report
        Messages.extend([[packageID, int(time), report]])

    def loadTrucks(self):
        noteDelayed ='Delayed on flight---will not arrive to depot until 9:05 am'
        noteWrongAddress = 'Wrong address listed'
        noteTruck2 = 'Can only be on truck 2'

        for i in range(len(self.Packages)):
            package = self.getPackage()
            if package == None: return

            package.status = Package.StatusTruck

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
                Hub.snapshot(package.ID, int(self.Truck2.time))

                continue

            #load low priority packages on truck 3
            if package.deadline == 24*60 and t3NumPackages < Truck.MaxPackages:
                self.Truck3.load(package)
                Hub.snapshot(package.ID, self.Truck3.time)
                continue

            #is package available? noteDelayed
            if truck.time >= package.timeAvailable:
                truck.load(package)
                Hub.snapshot(package.ID, truck.time)
                continue

            #package not loaded onto any truck, return to hub
            self.returnPackage(package)
            Hub.snapshot(package.ID, 8 * 60)
    
    def loadTruck(self, Truck):
        for package in hub.Packages: 
            package.status = Package.StatusTruck
            Truck.load(package)
            Hub.snapshot(package.ID, Truck.time)
        hub.Packages = []

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
    hub.loadTruck(hub.Truck1)
    hub.Truck1.deliverPackages()
    hub.Truck3.time = hub.Truck2.time
    hub.Truck3.deliverPackages()
else:
    hub.loadTruck(hub.Truck1)
    hub.Truck2.deliverPackages()
    hub.Truck3.time = hub.Truck1.time
    hub.Truck3.deliverPackages()

#packageStatus()


print(' - - - ')

def getPackageInfo(packageID, time):

    hours, minutes = map(int, time.split(':'))
    timeMinutes = minutes + (hours * 60)
    report = None

    for message in Messages:
        messageTime = message[1]
        id = message[0]
        if (messageTime < timeMinutes) and packageID == id:
            report = message
    
    if report != None:
        print(m2h(report[1]), report[2])
    

getPackageInfo(1,'9:00')

#todo: 
    #truck mileage
    #p9 wrong address listed