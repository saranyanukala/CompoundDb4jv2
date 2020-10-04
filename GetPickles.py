fhand = open("USSyn.txt")
SynId = {}
IdSyns = {}

count = 1

for line in fhand:
	#print("Count :",count)
	ID,pid = line.rstrip().split("\t")
	SynId[pid] = ID
	if (ID not in IdSyns):
		IdSyns[ID] = []
	IdSyns[ID].append(pid)
	count+=1

pickle_out = open("SynId.pickle","wb")
pickle.dump(SynId,pickle_out)
pickle_out.close()

pickle_out = open("IdSyns.pickle","wb")
pickle.dump(IdSyns,pickle_out)
pickle_out.close()

fhand.close()

fhand = open("PubPatAppUSPTO.csv")
Pat = {}
Pub = {}

count = 1

for line in fhand:
	#print("Count1 :",count)
	l = line.rstrip().split(",")
	Pat[l[1]] = Pat.get(l[1],0)+0
	Pub[l[0]] = Pub.get(l[0],0)+0
	count+=1

pickle_out = open("Pat.pickle","wb")
pickle.dump(Pat,pickle_out)
pickle_out.close()

pickle_out = open("Pub.pickle","wb")
pickle.dump(Pub,pickle_out)
pickle_out.close()

fhand.close()
