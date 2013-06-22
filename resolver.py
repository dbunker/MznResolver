
import os

print 'start'

def sabr2cnf(sabrCmd,num,sabrName):
	
	# ../SABR/sabr 2 sabr/1-solve.tb
	cmd = sabrCmd + ' --cnf ' + str(num+1) + ' ' + sabrName
	os.system(cmd)

def cnf2mzn(cnfName,mznName):

	cnfFile = open(cnfName,'r')
	mznFile = open(mznName,'w')

	line = cnfFile.readline()
	data = line.split()

	numVars = int(data[2])

	##############################
	# initialize variables
	for i in range(1,numVars+1):
		outStr = 'var bool: v' + str(i) + ';\n'
		mznFile.write(outStr)

	# output
	mznFile.write('output [\n')
	
	for i in range(1,numVars+1):
		outStr = 'show(v' + str(i) + ')," ",\n'
		mznFile.write(outStr)
	
	mznFile.write('];\n')
	
	##############################
	# create clauses

	line = cnfFile.readline()
	while line != '':
	
		data = line.strip().split()
	
		outStr = 'constraint '
		for elem in data:
			
			if elem != '0':
				if elem[0] == '-':
					outStr += 'not '
					elem = elem[1:]
				outStr += 'v' + elem + ' \/ '
	
		outStr = outStr[:-4] + ';\n'
		mznFile.write(outStr)
		
		line = cnfFile.readline()

	outStr = 'solve satisfy;\n\n'
	mznFile.write(outStr)
	
	mznFile.close()

def mzn2mznvars(mznName,mvnvarsName):
	
	cmd = 'mzn-gecode ' + mznName + ' > ' + mvnvarsName
	os.system(cmd)
	
def mznvars2sabrvars(mznvarsName,sabrvarsName):
	
	sabrvarsFile = open(sabrvarsName,'w')
	mznvarsData = open(mznvarsName,'r').read()
	
	data = mznvarsData.strip().split()
	
	sabrvarsFile.write('SAT\n')
	
	i = 1
	outStr = ''
	
	data = data[:-1]
	
	for elem in data:
		
		if elem == 'true':
			outStr += str(i)
		elif elem == 'false':
			outStr += '-'+str(i)
		else:
			print elem
			assert(False)
		
		outStr += ' '
		i += 1
	
	outStr = outStr + '0\n'
	sabrvarsFile.write(outStr)
	sabrvarsFile.close()
	
def sabrvars2out(sabrCmd,num,sabrName,outName):
	
	# ../SABR/sabr 2 sabr/1-solve.tb
	cmd = sabrCmd + ' --result ' + str(num+1) + ' ' + sabrName
	os.system(cmd)
	
	cmd = 'cp result.txt ' + outName 
	os.system(cmd)
	
def solve(sabrCmd,num,fullResolve=False):

	sabrName = 'sabr/' + str(num) + '-solve.tb'
	sabr2cnf(sabrCmd,num,sabrName)
	print 'sabr ' + sabrName
	print 'to cnf cnf.txt'

	mznName = str(num) + '-cube.mzn'
	cnf2mzn('cnf.txt',mznName)
	
	cmd = 'cp ' + mznName + ' out/mzn'
	os.system(cmd)
	print 'to mzn ' + mznName
	
	if fullResolve:
		mzn2mznvars(mznName,'mznvars.txt')
		print 'to mznvars mznvars.txt'
	
		mznvars2sabrvars('mznvars.txt','vars.txt')
		print 'to sabrvars vars.txt'
	
		outName = 'out/result/cube-' + str(num) + '-result.txt'
		sabrvars2out(sabrCmd,num,sabrName,outName)
		print 'to output ' + outName

def buildAll():
	for i in range(1,21):
		solve('../SABR/sabr',i,False)

def runSome():
	for i in range(1,5):
		solve('../SABR/sabr',i,True)

runSome()
