import re
from itertools import chain
###############################################################################
#@author Gurin Evgeny
def checkCorr(str):
	match = re.match(r"(\ )*[(|](\w?\d?)+[-+](\w?\d?)+[)|]=(\d)+(\ )*", str)
	if match is None:
		match = re.match(r"(\ )*-?(\d)+<=?[(|](\w?\d?)+[-+](\w?\d?)+[)|]<=?((\d)+)(\ )*", str)
	return match
###############################################################################
#@author Gurin Evgeny
def createVar(varTemp, startN):
	varTempTemp = ["0","0"]
	var = []
	k = 0
	i = startN
	while (i < (len(varTemp))):
		if re.match(r"[-\+\(\)|]", varTemp[i]) is not None:
			break
		elif (varTemp[i] == "x"):
			varTempTemp[0] = "x"
			varTempTemp[1] = varTemp[i+1]
			i += 2
		else:
			varTempTemp[0] = "num"
			varTempTemp[1] = varTemp[i]
			i += 1
		var.extend(varTempTemp)
	return var

###############################################################################
#@author Gurin Evgeny
def simb(str, IO, endFlag = "None"): #endFlag принимает значения "begin", "end",
# указывает искать знак с начала или с конца
	if (IO == "out"):
		if (endFlag == "begin"):
			strTerm = str[0:(re.search(r"[(|]", str).start())]
		elif (endFlag == "end"):
			strTerm = str[(re.search(r"[(|]", str).start())::]
		#__________________________
		match = re.search("<=", strTerm)
		if match is not None:
			simb = "<="
			str = str[0:(match.start())] + str[(match.start()+2)::]
		else:
			match = re.search("<", strTerm)
			simb = "<"
			str = str[0:(match.start())] + str[(match.start() + 1)::]

		return simb, str
	#__________________________
	elif (IO == "in"):
		match = re.search(r"\+", str)
		if match is not None:
			simb = "+"
		else:
			match = re.search(r"-", str)
			if match is not None:
				simb = "-"

		varOne = createVar(str, 1)
		varTwo = createVar(str, match.start()+1)

		return simb, varOne, varTwo
###############################################################################
#@author Gurin Evgeny
def parseOne(str):
	match = re.match(r"(\ )*-?(\d)+<=?[(|](\w?\d?)+[-+](\w?\d?)+[)|]<=?((\d)+)(\ )*", str)
	if match is not None:
		if re.search(r"|", str) is not None:
			absFlag = True
		elif re.search(r"(", str) is not None:
			absFlag = False

		minN = int(str[0:(re.search("<", str).start())])
		str = str[(re.search("<", str).start())::]
		simbOne, str = simb(str, "out", "begin")
		simbIn, varOne, varTwo = simb(str, "in")
		simbTwo, str = simb(str, "out", "end")
		maxN = int(str[(re.search(r"[|\)]", str[1::]).start() + 2)::])
		return minN, simbOne, varOne, simbIn, varTwo, simbTwo, maxN, absFlag
###############################################################################
#@author Gurin Evgeny
def parseTwo(str):
	while True:
		if (str[0] == " "):
			str = str[1::]
		else:
			break
	match = re.match(r"(\ )*[\(|](\w?\d?)+[-+](\w?\d?)+[\)|]=(\d,?)+(\ )*", str)
	if match is not None:
		if re.search(r"|", str) is not None:
			absFlag = True
		elif re.search(r"(", str) is not None:
			absFlag = False
		numEq = int(str[(re.search("=", str).start()+1)::])
		str = str[0:(re.search("=", str).start())]
		simbIn, varOne, varTwo = simb(str, "in")
		print(str)
	return varOne, simbIn, varTwo, numEq, absFlag
###############################################################################
#@author Gurin Evgeny
def parseAll(str):
	for match in chain(
		parseOne(str),
		parseTwo(str),
	):
		return match
###############################################################################
#@author Gurin Evgeny
def createVarTxt(var): #гененрирует текст, который будет названием столбца со значениями переменных
	varTxt = ""
	for simb in var:
		if (simb =="num"):
			continue
		else:
			varTxt += simb
	return varTxt
###############################################################################
#@author Gurin Evgeny
def createVarNumTxt(var, srcNum): #генерирует значение переменной в двоичном виде
	varNumTxt = ""
	isimb = 0
	while (isimb < len(var)):
		if var[isimb] == "x":
			varNumTxt += srcNum[int(var[isimb+1])-1]
			isimb += 2
		elif var[isimb] == "num":
			varNumTxt += var[isimb + 1]
			isimb += 2
		else:
			isimb += 1
	return varNumTxt
###############################################################################
#@author Gurin Evgeny
def checkF_unEq(minN, simbOne, resTemp, simbTwo, maxN):
	f = "0"
	if ((simbOne == "<=") & (resTemp >= minN))|((simbOne == "<") & (resTemp > minN)):
		if ((simbTwo == "<=") & (resTemp <= maxN))|((simbTwo == "<") & (resTemp < maxN)):
			f = "1"
	return f
###############################################################################
#@author Gurin Evgeny
def simbToText(simb: str, absFlag):
	if (absFlag == True):
		simb = "|" + str(simb) + "|"
	else:
		simb = "(" + str(simb) + ")"
	return str(simb)
###############################################################################
#@author Gurin Evgeny
def doTableOne(stringT, stringD):
	minT, simbOne, varOne, simbIn, varTwo, simbTwo, maxT, absFlag = parseOne(stringT)
	varOneD, simbInD, varTwoD, numEq, absFlagD = parseTwo(stringD)
	#print(minN, simbOne, varOne, simbIn, varTwo, simbTwo, maxN, absFlag)
	varsOne = []
	varsTwo = []
	varsOneD = []
	varsTwoD = []
	f = []

	simb = simbToText(simbIn, absFlag)
	simbD = simbToText(simbInD, absFlagD)


	print("%2s|%8s|%8s|%10s|%8s|%10s|%3s|%8s|%10s|%8s|%10s|%3s|f|" %("№", "x(12345)", createVarTxt(varOne), createVarTxt(varOne) + "(10)", createVarTxt(varTwo), createVarTxt(varTwo) + "(10)", simb, createVarTxt(varOneD), createVarTxt(varOneD) + "(10)", createVarTxt(varTwoD), createVarTxt(varTwoD) + "(10)", simbD))
	print("—"*102)
	for i in range(32):
		srcNum = str(bin(i))
		srcNum = "0"*(7-len(srcNum)) + srcNum[2::]
		varsOne.append(createVarNumTxt(varOne, srcNum))
		varsTwo.append(createVarNumTxt(varTwo, srcNum))
		varsOneD.append(createVarNumTxt(varOneD, srcNum))
		varsTwoD.append(createVarNumTxt(varTwoD, srcNum))

		if (simbIn == "+"):
			resTemp = int(varsOne[i], 2) + int(varsTwo[i], 2)
		elif (simbIn == "-"):
			resTemp = int(varsOne[i], 2) - int(varsTwo[i], 2)
		elif (simbIn == "mod"):
			resTemp = int(varsOne[i], 2) % int(varsTwo[i], 2)

		if absFlag:
			resTemp = abs(resTemp)

		if (simbInD == "+"):
			resTempD = int(varsOneD[i], 2) + int(varsTwoD[i], 2)
		elif (simbInD == "-"):
			resTempD = int(varsOneD[i], 2) - int(varsTwoD[i], 2)
		elif (simbInD == "mod"):
			resTempD = int(varsOneD[i], 2) % int(varsTwoD[i], 2)

		if absFlagD:
			resTempD = abs(resTempD)

		f.append(checkF_unEq(minT, simbOne, resTemp, simbTwo, maxT))
		if (resTempD == numEq):
			f[i] = "d"
		print("%2s|%8s|%8s|%10d|%8s|%10s|%3s|%8s|%10d|%8s|%10s|%3s|%s|" %(i, srcNum + " ", varsOne[i], int(varsOne[i], 2), varsTwo[i], int(varsTwoD[i], 2), resTempD, varsOneD[i], int(varsOneD[i], 2), varsTwoD[i], int(varsTwoD[i], 2), resTempD, f[i]))
###############################################################################
#@author Gurin Evgeny
def doTable(stringT, stringD):
	if re.match(r"(\ )*-?(\d)+<=?[(|](\w?\d?)+[-+](\w?\d?)+[)|]<=?((\d)+)(\ )*", string) is not None:
		minT, simbOne, varOne, simbIn, varTwo, simbTwo, maxN, absFlag = parseOne(stringT)
###############################################################################
#@author Gurin Evgeny
if __name__ ==  "__main__":
	cond = ["1", "d"]
	for i in cond:
		while True:
			print("Введите условие для f=%s: " %(i),end = "")
			string = input()
			if checkCorr(string) is None:
				print("Некорректное выражение")
				continue
			if (i == "1"):
				stringT = string
			else:
				stringD = string
			break
	doTableOne(stringT, stringD)