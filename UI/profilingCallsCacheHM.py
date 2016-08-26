# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import sys
import time
import re

functionsList = []
out = "Results/"

os.system("mkdir --p " + out) #creates results folder, if it insnt there already


profile		= sys.argv[1]
video		= sys.argv[2]
nf			= sys.argv[3]
qp			= sys.argv[4]
sRange		= sys.argv[5]
cSizeL1		= sys.argv[6]
cSizeLL		= sys.argv[7]
cAssL1		= sys.argv[8]
cAssLL		= sys.argv[9]
cWord		= sys.argv[10]
time 		= sys.argv[11]

class Function:
	def __init__(self, name, lista):
		self.name = name
		self.Ir		= int(str(lista[0]).replace(',', ''))
		self.Dr		= int(str(lista[1]).replace(',', ''))
		self.Dw		= int(str(lista[2]).replace(',', ''))
		self.I1mr	= int(str(lista[3]).replace(',', ''))
		self.D1mr	= int(str(lista[4]).replace(',', ''))
		self.D1mw	= int(str(lista[5]).replace(',', ''))
		self.ILmr	= int(str(lista[6]).replace(',', ''))
		self.DLmr	= int(str(lista[7]).replace(',', ''))
		self.DLmw	= int(str(lista[8]).replace(',', ''))
		self.Dmw	= self.D1mw + self.DLmw
		self.Dwh	= self.Dw - self.Dmw		#data write hits only
		self.Dmr	= self.D1mr + self.DLmr	#total data read misses
		self.Drh	= self.Dr - self.Dmr		#data read hits only
		self.Imr	= self.I1mr + self.ILmr	#total instruction read misses
		self.Irh	= self.Ir - self.Imr		#instruction read hits only
		self.L1Rate	= 0.0
		self.I1Rate	= 0.0
		self.D1Rate	= 0.0
		self.LLRate	= 0.0
		self.ILRate	= 0.0
		self.DLRate	= 0.0
			
	def __add__(self, other):
		return Function(self.name, [self.Ir + other.Ir, self.Dr + other.Dr, self.Dw + other.Dw, self.I1mr + other.I1mr, self.D1mr + other.D1mr, self.D1mw + other.D1mw, self.ILmr + other.ILmr, self.DLmr + other.DLmr, self.DLmw + other.DLmw])   	

	def toString(self):
		return self.name + '\t' + str(self.Ir) + '\t' + str(self.Dr) + '\t' + str(self.Dw) + '\t' + str(self.I1mr) + '\t' + str(self.D1mr) + '\t' + str(self.D1mw) + '\t' + str(self.ILmr) + '\t' + str(self.DLmr) + '\t' + str(self.DLmw) + '\t' + str(self.Irh) + '\t' + str(self.Drh) + '\t' + str(self.Dwh) + '\t' + str(self.L1Rate) + ' %\t' + str(self.I1Rate) + ' %\t' + str(self.D1Rate) + ' %\t' + str(self.LLRate) + ' %\t' + str(self.ILRate) + ' %\t' + str(self.DLRate) + ' %'
	
	def accumulate(self, name, words):
		self.Ir += int(words[0])
		self.Dr += int(words[1])
		self.Dw += int(words[2])
		self.I1mr += int(words[3])
		self.D1mr += int(words[4])
		self.D1mw += int(words[5])
		self.ILmr += int(words[6])
		self.DLmr += int(words[7])
		self.DLmw += int(words[8])
		self.Dmw += self.D1mw + self.DLmw
		self.Dwh += self.Dw - self.Dmw		#data write hits only
		self.Dmr += self.D1mr + self.DLmr	#total data read misses
		self.Drh += self.Dr - self.Dmr		#data read hits only
		self.Imr += self.I1mr + self.ILmr	#total instruction read misses
		self.Irh += self.Ir - self.Imr		#instruction read hits only
		
	def calcRates(self):
		if (self.Ir == 0 or self.Dr == 0 or self.Dw == 0):
			self.L1Rate	= 0
			self.I1Rate	= 0
			self.D1Rate	= 0
			self.LLRate	= 0
			self.ILRate	= 0
			self.DLRate	= 0
		else:
			self.L1Rate	= (self.I1mr + self.D1mr + self.D1mw) / ((self.Ir + self.Dr + self.Dw) * 0.01)
			self.I1Rate	= (self.I1mr) / ((self.Ir)* 0.01)
			self.D1Rate	= (self.D1mr + self.D1mw) / ((self.Dr + self.Dw)* 0.01)
			self.LLRate	= (self.ILmr + self.DLmr + self.DLmw) / ((self.Ir + self.Dr + self.Dw)* 0.01)
			self.ILRate	= (self.ILmr) / ((self.Ir) *0.01)
			self.DLRate	= (self.DLmr + self.DLmw) / ((self.Dr + self.Dw)* 0.01)		
		
nullList = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
#initialization of acc variables
Entropy =	Function('Entropy',		nullList)
Filter =	Function('Filter',		nullList)
IQ =		Function('InvQuant',	nullList)
Q =			Function('Quant',		nullList)
IT =		Function('InvTransf',	nullList)
T =			Function('Transf',		nullList)
P =			Function('Misc',		nullList)
Pred =		Function('Pred',		nullList)
Inter =		Function('Inter',		nullList)
Intra =		Function('Intra',		nullList)
I =			Function('Inter/Intra',	nullList)

modules = [Entropy, IQ, Q, IT, T, P, I, Inter, Intra, Filter]

classesDic = {'TEncEntropy':Entropy, 'TComInterpolationFilter':Inter, 'TComTrQuant':T, 'TComYuv': P, 'TEncSbac': Entropy, 'TComLoopFilter': Filter, 'TEncBinCABAC':Entropy, 'xTrMxN':T, 'xITrMxN':IT, 'fastFowardDst':T, 'FastInverseDst':IT, 'void':Inter}
PBI = re.compile('partialButterflyInverse(\d+)')
PB = re.compile('partialButterfly(\d+)')
InterList = ['Inter', 'xGetComponentBits', 'xPatternRefinement', 'TZSearch', 'Mv', 'DPCM', 'xGetTemplateCost', 'Motion', 'MVP', 'xMergeEstimation', 'xGetSAD12', 'xGetSAD24', 'xGetSAD48']
IntraList = ['Intra', 'Available', 'ReferenceSamples', 'xUpdateCandList']
ITList = ['xIT']
TList = ['xT', 'Transform', 'Dst']
QList = ['Quant']

labels = "\tInstruction Read\tData Read\tData Write\t L1 Instruction Misses (Read)\tL1 Data Misses (Read)\tL1 Data Misses (Write)\tLL Instruction Misses (Read)\tLL Data Misses (Read)\tLL Data Misses (Write)\tIntruction Hits (Read)\tData Hits (Read)\tData Hits(Write)\tL1 Miss Rate\tL1 Instruction Miss Rate\tL1 Data Miss Rate\tLL Miss Rate\tLL Instruction Miss Rate\tLL Data Miss Rate"

def parseAnnotate(csv, hmConfig, memoryConfig):
	header = hmConfig + memoryConfig + labels
	print >> csv, header  #print header

	f = open(annotateFile)
	lines = f.readlines()
	words = lines[20].split() #PROGRAM TOTALS line
	total = Function('PROGRAM TOTALS', words)

	for i, line in enumerate(lines[25:]): #begin functions data
		words = line.split()

		if not words: #empty words, expected if there are any error reports in the end
			break
		else:
			for x in range(0,9): #treatment for '.' cases, when there's no value
				words[x] = words[x].replace(',' , '')
				if words[x] == ".":
					words[x] = '0'
		#BEGIN NOJEIRA
			name = words[9]
			name = name.strip("?:")
			name = name.split("(")
			name = name[0]
		#END NOJEIRA
			
			x = Function(name, words)
			functionsList.append(x)
			writeOutput(csv, functionsList, i)
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
						if any(x in fMethod for x in InterList):
							Inter.accumulate(fClass, words)
						else:
							if any(x in fMethod for x in IntraList):
								Intra.accumulate(fClass, words)
	Pred = I + Intra + Inter
	#printing final results to csv
	print "Fazendo resumo..."
	resumo = open (out + time + "_resumo" + ".csv", 'w')
	i = 0
	print >> resumo, "\nRESULTS" + labels
	for module in modules:
		writeOutput(resumo, modules, i)
		i = i + 1
	f.close
	resumo.close
    			
def writeOutput(csv, functionsList, i):
	functionsList[i].calcRates()
	print >> csv, functionsList[i].toString() #print line: each line is an object

def codifica():
#runs valgrind + HM

	name = video.split("/")
	name = name[6].split(".")
	name = name[0]
	
	hmConfig = time + "__" + name + "_" + "_QP_" + qp + "_nF_" + nf + "_SR_" + sRange
	memoryConfig = "_MSizeL1_" + str(cSizeL1) +  "_AssL1_" + str(cAssL1) + "_MSizeLL_" + str(cSizeLL)+ "_AssLL_" + str(cAssLL) + "_Word_" + str(cWord)
	hmSetup = "~/HM-16.2_callfunc/bin/./TAppEncoderStatic -c " + profile + " -c " + video + " --QP=" + qp + " --SearchRange=" + sRange + " --FramesToBeEncoded=" + nf

	csv = open (out + hmConfig + memoryConfig + ".csv", 'w')
	callValgrind = "valgrind --tool=callgrind --simulate-cache=yes" + " --D1=" + str(cSizeL1) + "," + str(cAssL1) + "," + str(cWord) + " --LL=" + str(cSizeLL) + "," + str(cAssLL) + "," + str(cWord) + " --callgrind-out-file=" + out + "valgrind_" + hmConfig + memoryConfig + ".txt " + hmSetup
	

	os.system(callValgrind)
	annotateFile = out + hmConfig + memoryConfig + "_annotate" + ".txt"
	callAnnotate = "callgrind_annotate --auto=yes --threshold=100 "+ out + "valgrind_" + hmConfig + memoryConfig + ".txt >" + annotateFile
	os.system(callAnnotate)
	parseAnnotate(csv, hmConfig, memoryConfig)
	
	csv.close()

codifica()
