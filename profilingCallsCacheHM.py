# -*- coding: utf-8 -*-
#!/usr/bin/python
 
import time
import os
import sys

proj = sys.argv[1]
lista = []
lol = []
totais = []

#leitura do arquivo de projeto e atribuição das variáveis
p = open(proj + ".txt", 'r')
linhas = p.readlines()
p.close()

for n in linhas:
	l = n.split(',')
	l.pop()
	lista.append(l)
	
profiles = lista[0]
videos = lista[1]
nFs = lista[2]
QPs = lista[3]
sRanges = lista[4]
size_L1 = lista[5]
size_Ll = lista[6]
ass_L1 = lista[7]
ass_Ll = lista[8]
cache_word = lista[9]
out = "/Results/"
vec = []


## dd/mm/yyyy format
print (time.strftime("%d/%m/%Y"))

class Function:
    def __init__(self, function, Ir, Dr, Dw, I1mr, D1mr, D1mw, ILmr, DLmr, DLmw):
    	self.function = function
    	self.Ir = Ir
    	self.Dr = Dr
    	self.Dw = Dw
    	self.I1mr = I1mr
    	self.D1mr = D1mr
    	self.D1mw = D1mw
    	self.ILmr = ILmr
    	self.DLmr = DLmr
    	self.DLmw = DLmw

Com = Function('Com', 0, 0, 0, 0, 0, 0, 0, 0, 0)
Enc = Function('Enc', 0, 0, 0, 0, 0, 0, 0, 0, 0)
Other = Function('Other', 0, 0, 0, 0, 0, 0, 0, 0, 0)

def parse_annotate(out, name, qp, nf, hm_config, memory_config):
	f = open("annotate_" + hm_config + memory_config + ".txt")
	lines = f.readlines()
	words = lines[20].split() #PROGRAM TOTALS line
	Ir = words[0]
	Dr = words[1]
	Dw = words[2]
	I1mr = words[3]
	D1mr = words[4]
	D1mw = words[5]
	ILmr = words[6]
	DLmr = words[7]
	DLmw = words[8]
	function = words[9] + " " + words [10]
	total = Function(function, Ir, Dr, Dw, I1mr, D1mr, D1mw, ILmr, DLmr, DLmw)
	attrs = vars(total)
	print >> csv, '\t'.join("%s: %s" % item for item in attrs.items())

	for i, line in enumerate(lines[25:]): #begin function data
		word = line.split()

		if not word: #empty word, expected if there are any error reports in the end
			break
		else:
			for x in range(0,9):
				if word[x] == ".":
					word[x] = "0"
		#BEGIN NOJEIRA
			function = word[9]
			function = function.strip("?:")
			function = function.split("(")
			function = function[0]
			function = function.split("/")
			function = function[0]
		#END NOJEIRA
			x = Function(function, Ir, Dr, Dw, I1mr, D1mr, D1mw, ILmr, DLmr, DLmw)
			x.Ir = word[0]
			x.Dr = word[1]
			x.Dw = word[2]
			x.I1mr = word[3]
			x.D1mr = word[4]
			x.D1mw = word[5]
			x.ILmr = word[6]
			x.DLmr = word[7]
			x.DLmw = word[8]

			lol.append(x)



			if "TCom" in function:
				Com.Ir += int(word[0].replace(',', ''))
				Com.Dr += int(word[1].replace(',', ''))
				Com.Dw += int(word[2].replace(',', ''))
				Com.I1mr += int(word[3].replace(',', ''))
				Com.D1mr += int(word[4].replace(',', ''))
				Com.D1mw += int(word[5].replace(',', ''))
				Com.ILmr += int(word[6].replace(',', ''))
				Com.DLmr += int(word[7].replace(',', ''))
				Com.DLmw += int(word[8].replace(',', ''))
			
			else:
				if "TEnc" in function:
					Enc.Ir += int(word[0].replace(',', ''))
					Enc.Dr += int(word[1].replace(',', ''))
					Enc.Dw += int(word[2].replace(',', ''))
					Enc.I1mr += int(word[3].replace(',', ''))
					Enc.D1mr += int(word[4].replace(',', ''))
					Enc.D1mw += int(word[5].replace(',', ''))
					Enc.ILmr += int(word[6].replace(',', ''))
					Enc.DLmr += int(word[7].replace(',', ''))
					Enc.DLmw += int(word[8].replace(',', ''))
				else:
					Other.Ir += int(word[0].replace(',', ''))
					Other.Dr += int(word[1].replace(',', ''))
					Other.Dw += int(word[2].replace(',', ''))
					Other.I1mr += int(word[3].replace(',', ''))
					Other.D1mr += int(word[4].replace(',', ''))
					Other.D1mw += int(word[5].replace(',', ''))
					Other.ILmr += int(word[6].replace(',', ''))
					Other.DLmr += int(word[7].replace(',', ''))
					Other.DLmw += int(word[8].replace(',', ''))
							
			writeOutput(lol, i)
		
	Com.Ir = str(Com.Ir)
	Com.Dr = str(Com.Dr)
	Com.Dw = str(Com.Dw)
	Com.I1mr = str(Com.I1mr)
	Com.D1mr = str(Com.D1mr)
	Com.D1mw = str(Com.D1mw)
	Com.ILmr = str(Com.ILmr)
	Com.DLmr = str(Com.DLmr)
	Com.DLmw = str(Com.DLmw)

	Enc.Ir = str(Enc.Ir)
	Enc.Dr = str(Enc.Dr)
	Enc.Dw = str(Enc.Dw)
	Enc.I1mr = str(Enc.I1mr)
	Enc.D1mr = str(Enc.D1mr)
	Enc.D1mw = str(Enc.D1mw)
	Enc.ILmr = str(Enc.ILmr)
	Enc.DLmr = str(Enc.DLmr)
	Enc.DLmw = str(Enc.DLmw)

	Other.Ir = str(Other.Ir)
	Other.Dr = str(Other.Dr)
	Other.Dw = str(Other.Dw)
	Other.I1mr = str(Other.I1mr)
	Other.D1mr = str(Other.D1mr)
	Other.D1mw = str(Other.D1mw)
	Other.ILmr = str(Other.ILmr)
	Other.DLmr = str(Other.DLmr)
	Other.DLmw = str(Other.DLmw)
			

	attrs = vars(Com)
	print >> csv, '\t'.join("%s: %s" % item for item in attrs.items())
	attrs = vars(Enc)
	print >> csv, '\t'.join("%s: %s" % item for item in attrs.items())
	attrs = vars(Other)
	print >> csv, '\t'.join("%s: %s" % item for item in attrs.items())
		
	f.close
    			
def writeOutput(lol, ind):
	attrs = vars(lol[ind])
	print >> csv, '\t'.join("%s: %s" % item for item in attrs.items())#print line: each line is an object

def codifica():

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
											name = name[3].split(".")
											name = name[0]

											hm_config = name + "_" + "_QP_" + qp + "_nF_" + nf
											memory_config = "_MSizeL1_" + str(cSizeL1) +  "_AssL1_" + str(cAssL1) + "_MSizeLL_" + str(cSizeLL)+ "_AssLL_" + str(cAssLL) + "_Word_" + str(cWord)

											call_valgrind = "valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes" + " --D1=" + str(cSizeL1) + "," + str(cAssL1) + "," + str(cWord) + " --LL=" + str(cSizeLL) + "," + str(cAssLL) + "," + str(cWord) + " --callgrind-out-file=valgrind_" + hm_config + memory_config + ".txt " + "../../HM-16.2/bin/./TAppEncoderStatic -c " + profile + " -c " + video + " --QP=" + qp + " --SearchRange=" + sRange + " --FramesToBeEncoded=" + nf

											os.system(call_valgrind)
									
											call_annotate = "callgrind_annotate --auto=yes valgrind_" + hm_config + memory_config + ".txt >" + "annotate_" + hm_config + memory_config + ".txt"
											os.system(call_annotate)
											header = hm_config + memory_config 
											print >> csv, header  #print header
											parse_annotate(out, name, qp, nf, hm_config, memory_config)
				
#initialization of the csv
csv = open ("results_parse.csv", 'w')

codifica()

csv.close()
