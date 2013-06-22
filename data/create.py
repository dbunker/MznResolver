
print 'start'

boardsDat = open('rubik-data.txt','r').read()
boards = boardsDat.split('start cube')

topDat = open('top.txt','r').read()
botDat = open('bot.txt','r').read()

boards = boards[1:]

i = 1
for board in boards:
	
	board = board.strip()
	outName = '../sabr/' + str(i) + '-solve.tb'
	
	outData = topDat + '\n\t\t' + board + '\n' + botDat
	
	outFile = open(outName,'w')
	outFile.write(outData)
	
	print 'out: ' + outName
	i += 1
	if i > 20:
		break