import csv
import itertools
import re

configdata = {}
itemset = {}
transactions = []
rules = {}
frequentItems = {}

def getConfidence(newitems):
	for item in newitems:
		eachitem = re.split(" ", item)
		itemlen = len(eachitem)
		setel = set(eachitem)
		for i in range(1, itemlen):
			lhs = list(itertools.combinations(setel, i))
			for i in lhs:
				rhs = setel.difference(i)
				i = " ".join(list(i))
				rhs = " ".join(list(rhs))
				if i in frequentItems.keys() and rhs in frequentItems.keys():
					conf = float(frequentItems[item])/float(frequentItems[i])
					if conf >= float(configdata["confidence"]):
						rules[i + "=>" + rhs] = conf


with open("config.csv", "r") as csvfile:
	configfile = csv.reader(csvfile, delimiter=',')
	for row in configfile:
		configdata[row[0]] = row[1]
	csvfile.close()

with open(configdata["input"], "r") as inpfile:
	inpdata = csv.reader(inpfile, delimiter=",")
	for row in inpdata:
		temp = []
		for element in row:
			temp.append(element)
			if element not in itemset.keys():
				itemset[element] = 1
			else:
				itemset[element] += 1
		transactions.append(temp)
	inpfile.close()
#for single elements
newitemset = {}
for key in itemset.keys():
	if itemset[key] >= float(configdata['support'])*len(transactions):
		newitemset[key] = itemset[key]
		frequentItems[key] = newitemset[key]

itemset = dict(newitemset)

#for double elements
if len(itemset.keys()) > 0:
	newitemset = {}
	for key in sorted(itemset.keys()):
		for key1 in sorted(itemset.keys()):
			for itemlist in transactions:
				if key < key1 and set([key, key1]).issubset(set(itemlist)):
					if key + " " + key1 not in newitemset.keys():
						newitemset[key+" "+key1] = 1
					else:
						newitemset[key+" "+key1] += 1

	for key in sorted(newitemset.keys()):
		if newitemset[key] >= float(configdata['support'])*len(transactions):
			frequentItems[key] = newitemset[key]
		else:
			newitemset.pop(key, None)
	
	if configdata["flag"] == "1":
		getConfidence(newitemset)

	itemset = dict(newitemset)

while len(itemset.keys()) > 0:
	newitemset = {}
	for key in itemset.keys():
		allkey = re.split(" ", key)
		sizekey = len(allkey)
		for key1 in itemset.keys():
			allkey1 = re.split(" ", key1)
			sizekey1 = len(allkey1)
			if " ".join(allkey[0:sizekey-1]) == " ".join(allkey1[0:sizekey1-1]) and allkey[-1] < allkey1[-1]:
				newkey = " ".join(allkey[0:sizekey-1]) + " " + allkey[-1] + " " + allkey1[-1]
				newkeylist = allkey + [allkey1[-1]]
				newitemset[newkey] = 0
				for itemlist in transactions:
					if set(newkeylist).issubset(set(itemlist)):
						newitemset[newkey] += 1
	for item in newitemset.keys():
		if newitemset[item] < float(configdata['support'])*len(transactions):
			newitemset.pop(item, None)
		else:
			frequentItems[item] = newitemset[item]

	
	if configdata["flag"] == "1":
		getConfidence(newitemset)	
	itemset = dict(newitemset)

with open(configdata["output"], "w") as outfile:
	outfile.write(str(len(frequentItems)) + "\n")
	for i in frequentItems.keys():
		outfile.write(re.sub(" ", ",", i) + "\n")
	outfile.write(str(len(rules)) + "\n")
	for i in rules.keys():
		outfile.write(re.sub(" ", ",", i) + "\n")
	outfile.close()
