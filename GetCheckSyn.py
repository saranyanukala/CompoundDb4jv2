import pickle
import sys

infile = str(sys.argv[1])

pickle_in = open("SynId.pickle","rb")
SynId = pickle.load(pickle_in)

pickle_in = open("IdSyns.pickle","rb")
IdSyns = pickle.load(pickle_in)

pickle_in = open("Pat.pickle","rb")
Pat = pickle.load(pickle_in)

pickle_in = open("Pub.pickle","rb")
Pub = pickle.load(pickle_in)


#fhand = open("PubNotFound.txt")
#fhand = open("PatNotFound.txt")
fhand = open(infile)
#file1 = open("PubSynNotFound.txt","w")
#file2 = open("PubSynFound.txt","w")
#file1 = open("PatSynNotFound.txt","w")
#file2 = open("PatSynFound.txt","w")
#foundName = 'Found'+infile.split('.')[0]
#notFoundName = 'Not Found'+infile.split('.')[0]

file1 = open("NotFound1.txt","a")
file2 = open("Found1.txt","a")

for line in fhand:
	flag = 0
	patnum = line.rstrip()
	if (patnum in SynId):
		ids = SynId[patnum]
	else :
		file1.write(patnum+"\n") #No synonym at all
		print("Not Found :",patnum)
		continue
	synonyms = IdSyns[ids]
	#print(synonyms)
	for syn in synonyms:
		syn1 = syn[2:] #syn1 = without US(to check in Patents
		if (syn1 in Pat):
			file2.write(patnum+"|"+syn1+"\n")
			flag = 1
			print(patnum,syn1)
			break

		elif (syn in Pub):
			file2.write(patnum+"|"+syn+"\n")
			flag = 1
			print(patnum,syn)
			break

	if (flag == 0):
		file1.write(patnum+"\t")
		for syn in synonyms:
			file1.write(syn+" ")
		file1.write("\n")

fhand.close()
file1.close()
file2.close()
		
	 
