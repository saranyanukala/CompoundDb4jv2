import pickle

pickle_in = open("Pat.pickle","rb")
Pat = pickle.load(pickle_in)

pickle_in = open("Pub.pickle","rb")
Pub = pickle.load(pickle_in)

fhand1 = open("AllPatPubNumbersUSPubchem.txt")
#fhand1 = open("AllPubNumbersUSPubchem.txt")
file1 = open("Found.txt","w")
file2 = open("NotFound.txt","w")
#file1 = open("PubFound.txt","w")
#file2 = open("PubNotFound.txt","w")
count = 1

for patnum in fhand1:
	patnum = patnum.rstrip()
	patn = patnum[2:]  #removing US for patentNumbers 
	print("Record",count,":",patnum)
	if (patn in Pat):
	#if (patnum in Pub):
		print("Found :",patnum)
		file1.write(patnum+"|"+patn+"\n")
		#file1.write(patnum+"|"+patnum+"\n")
	elif(patnum in Pub):
		file1.write(patnum+"|"+patnum+"\n")
	else:
		print("Not Found :",patnum)
		file2.write(patnum+"\n")
	count += 1

#fhand.close()
fhand1.close()
file1.close()
file2.close()

