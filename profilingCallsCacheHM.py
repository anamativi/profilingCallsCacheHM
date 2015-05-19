# -*- coding: utf-8 -*-
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
out = "Results/"
vec = []

size_L1 = ["8192"]
size_Ll = [str(x*1024) for x in [4096, 8192]] #4M,8M
ass_L1 = ["1",]
ass_Ll = ["1", ]
cache_word = ["32"]

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

def parse_annotate(out, hm_config, memory_config):
	f = open(out + "annotate_" + hm_config + memory_config + ".txt")
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
	print attrs
	print >> csv, '\t'.join("%s: %s" % item for item in attrs.items())

	for i, line in enumerate(lines[25:]): #begin function data
		word = line.split()

		if not word: #empty word, expected if there are any error reports in the end
			break
		else:
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
			writeOutput(lol, i)
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
											memory_config = "_MSize_L1_" + str(cSizeL1) +  "_AssL1_" + str(cAssL1) + "_MSize_LL" + str(cSizeLL)+ "_AssLL_" + str(cAssLL) + "_Word_" + str(cWord)

											call_valgrind = "valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes" + " --D1=" + str(cSizeL1) + "," + str(cAssL1) + "," + str(cWord) + " --LL=" + str(cSizeLL) + "," + str(cAssLL) + "," + str(cWord) + " --callgrind-out-file=valgrind_" + hm_config + memory_config + ".txt " + "../../HM-16.2/bin/./TAppEncoderStatic -c " + profile + " -c " + video + " --QP=" + qp + " --SearchRange=" + sRange + " --FramesToBeEncoded=" + nf
											os.system(call_valgrind)
									
											call_annotate = "callgrind_annotate --auto=yes valgrind_" + hm_config + memory_config + ".txt >" + out + "annotate_" + hm_config + memory_config + ".txt"
											os.system(call_annotate)
											header = hm_config + memory_config 
											print >> csv, header  #print header
											parse_annotate(out, hm_config, memory_config)
				
#initialization of the csv
csv = open ("results_parse.csv", 'w')

codifica()

csv.close()
