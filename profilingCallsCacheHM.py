# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import sys
import time
import re

proj = sys.argv[1]
param = []
functionsList = []
out = "Results_" + time.strftime("%d_%m_%y") + "/"

os.system("mkdir --p " + out) #creates results folder, if it insnt there already

#reads project archive and attributes simulation variables
p = open(proj + ".txt", 'r')
lines = p.readlines()
p.close()

for n in lines:
	l = n.split(',')
	l.pop()
	param.append(l)

profiles = param[0]
videos = param[1]
nFs = param[2]
QPs = param[3]
sRanges = param[4]
size_L1 = param[5]
size_Ll = param[6]
ass_L1 = param[7]
ass_Ll = param[8]
cache_word = param[9]

class Function:
	def __init__(self, name, lista):
		self.name = name
		self.Ir = lista[0]
		self.Dr = lista[1]
		self.Dw = lista[2]
		self.I1mr = lista[3]
		self.D1mr = lista[4]
		self.D1mw = lista[5]
		self.ILmr = lista[6]
		self.DLmr = lista[7]
		self.DLmw = lista[8]
		
	def toString(self):
		return self.name + '\t' + str(self.Ir) + '\t' + str(self.Dr) + '\t' + str(self.Dw) + '\t' + str(self.I1mr) + '\t' + str(self.D1mr) + '\t' + str(self.D1mw) + '\t' + str(self.ILmr) + '\t' + str(self.DLmr) + '\t' + str(self.DLmw)
	
	def accumulate(self, name, words):
		self.Ir += int(words[0].replace(',', ''))
		self.Dr += int(words[1].replace(',', ''))
		self.Dw += int(words[2].replace(',', ''))
		self.I1mr += int(words[3].replace(',', ''))
		self.D1mr += int(words[4].replace(',', ''))
		self.D1mw += int(words[5].replace(',', ''))
		self.ILmr += int(words[6].replace(',', ''))
		self.DLmr += int(words[7].replace(',', ''))
		self.DLmw += int(words[8].replace(',', ''))
			
		return Function(self.name, [self.Ir, self.Dr, self.Dw, self.I1mr, self.D1mr, self.D1mw, self.ILmr, self.DLmr, self.DLmw])
	
#initialization of acc variables
Entropy = Function('Entropy', [0, 0, 0, 0, 0, 0, 0, 0, 0])
Filter = Function('Filter', [0, 0, 0, 0, 0, 0, 0, 0, 0])
Inter = Function('Inter', [0, 0, 0, 0, 0, 0, 0, 0, 0])
Intra = Function('Intra', [0, 0, 0, 0, 0, 0, 0, 0, 0])
I = Function('Inter/Intra', [0, 0, 0, 0, 0, 0, 0, 0, 0])
IQ = Function('InvQuant', [0, 0, 0, 0, 0, 0, 0, 0, 0])
Q = Function('Quant', [0, 0, 0, 0, 0, 0, 0, 0, 0])
IT = Function('InvTransf', [0, 0, 0, 0, 0, 0, 0, 0, 0])
T = Function('Transf', [0, 0, 0, 0, 0, 0, 0, 0, 0])
P = Function('Pre/Pos', [0, 0, 0, 0, 0, 0, 0, 0, 0])

classesDic = {'TEncEntropy':Entropy, 'TComInterpolationFilter':Filter, 'TComTrQuant':T, 'TComYuv': P, 'TEncSbac': Entropy, 'TComLoopFilter': Filter, 'TEncBinCABAC':Entropy, 'xTrMxN':T, 'xITrMxN':IT}
PBI = re.compile('partialButterflyInverse(\d+)')
PB = re.compile('partialButterfly(\d+)')
InterList = ['Inter', 'xGetComponentBits', 'xPatternRefinement', 'TZSearch', 'Mv', 'DPCM', 'xGetTemplateCost', 'Motion', 'MVP', 'xMergeEstimation']
IntraList = ['Intra', 'xUpdateCandList']
IList = ['SSE', 'SAD', 'HAD']
ITList = ['xIT']
TList = ['xT', 'Transform']
QList = ['Quant']

def parseAnnotate(hmConfig, memoryConfig):
	header = hmConfig + memoryConfig + "\tIr\tDr\tDw\tI1mr\tD1mr\tD1mw\tILmr\tDLmr\tDLmw"
	print >> csv, header  #print header

	f = open(out + "annotate_" + hmConfig + memoryConfig + ".txt")
	lines = f.readlines()
	words = lines[20].split() #PROGRAM TOTALS line
	total = Function('PROGRAM TOTALS', words)

	for i, line in enumerate(lines[25:]): #begin functions data
		words = line.split()

		if not words: #empty words, expected if there are any error reports in the end
			break
		else:
			for x in range(0,9): #treatment for '.' cases, when there's no value
				if words[x] == ".":
					words[x] = "0"
		#BEGIN NOJEIRA
			name = words[9]
			name = name.strip("?:")
			name = name.split("(")
			name = name[0]
		#END NOJEIRA
			x = Function(name, words)
			functionsList.append(x)
			writeOutput(functionsList, i)
			nameList = name.split(':')
			fClass = nameList[0]
			
			if len(nameList) == 3: #functions with names class::method
				fMethod = nameList[2]
			else: #functions with short names
				fMethod = ''
				
			if fClass in classesDic: #checks if the function can be sorted by its class
				myInstance = classesDic.get(fClass)
				if myInstance is not None:
					if myInstance == T:
						if 'DeQuant' in fMethod: #case inside TComTrQuant
							IQ.accumulate(fClass, words)
						else:
							if any(x in fMethod for x in QList):
								Q.accumulate(fClass, words)
							else:
								if any(x in fMethod for x in ITList):
									IT.accumulate(fClass, words)
								else:
									myInstance.accumulate(fClass, words)
					else:
						myInstance.accumulate(fClass, words)
			else: #for functions that need method evaluation
				if PBI.match(fClass):
					IT.accumulate(fClass, words)
				else:	
					if PB.match(fClass):
						T.accumulate(fClass, words)
			if 'init' in fMethod:
				P.accumulate(fClass, words)
			else:
				if 'QT' in fMethod: #QuadTree
					T.accumulate(fClass, words)
				else:
					if any(x in fMethod for x in IList): #methods used both in Intra and Inter pred modes
						I.accumulate(fClass, words)
					else:
						if any(x in fMethod for x in InterList):
							Inter.accumulate(fClass, words)
						else:
							if any(x in fMethod for x in IntraList):
								Intra.accumulate(fClass, words)
	#printing final results to csv
	print >>csv, "\nRESULTS"
	print >> csv, Entropy.toString()
	print >> csv, Filter.toString()
	print >> csv, Intra.toString()
	print >> csv, Inter.toString()
	print >> csv, I.toString()
	print >> csv, IQ.toString()
	print >> csv, Q.toString()
	print >> csv, IT.toString()
	print >> csv, T.toString()
	print >> csv, P.toString()
	print >> csv, total.toString()
	f.close
    			
def writeOutput(functionsList, i):
	print >> csv, functionsList[i].toString() #print line: each line is an object

def codifica():
#runs valgrind + HM
	for video in videos:
		for profile in profiles:
			for sRange in sRanges:
				for qp in QPs:
					for nf in nFs:
						for cSizeL1 in size_L1:
							for cAssL1 in ass_L1:
								for cSizeLL in size_Ll:
									for cAssLL in ass_Ll:
										for cWord in cache_word:
										
											name = video.split("/")
											name = name[5].split(".")
											name = name[0]

											hmConfig = name + "_" + "_QP_" + qp + "_nF_" + nf
											memoryConfig = "_MSizeL1_" + str(cSizeL1) +  "_AssL1_" + str(cAssL1) + "_MSizeLL_" + str(cSizeLL)+ "_AssLL_" + str(cAssLL) + "_Word_" + str(cWord)
											hmSetup = "../../HM-16.2/bin/./TAppEncoderStatic -c " + profile + " -c " + video + " --QP=" + qp + " --SearchRange=" + sRange + " --FramesToBeEncoded=" + nf
											
											callValgrind = "valgrind --tool=callgrind --simulate-cache=yes" + " --D1=" + str(cSizeL1) + "," + str(cAssL1) + "," + str(cWord) + " --LL=" + str(cSizeLL) + "," + str(cAssLL) + "," + str(cWord) + " --callgrind-out-file=" + out + "valgrind_" + hmConfig + memoryConfig + ".txt " + hmSetup

											os.system(callValgrind)

											callAnnotate = "callgrind_annotate --auto=yes "+ out + "valgrind_" + hmConfig + memoryConfig + ".txt >" + out + "annotate_" + hmConfig + memoryConfig + ".txt"
											os.system(callAnnotate)
											parseAnnotate(hmConfig, memoryConfig)
				

csv = open (out + "parsedResults.csv", 'w')

codifica()

csv.close()
