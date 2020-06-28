import csv
import pandas as pd

def SellDate(Stuff,StartIndex):
		x = StartIndex
		HiPoint = Stuff.Price[x]
		SevPerc = HiPoint*0.1
		while (x+1<1726):
			x = x+1
			if(Stuff.Chg[x] < 0):
				if((HiPoint - Stuff.Price[x]) > SevPerc):
					print("Sell On: " + Stuff.Date[x])
					break
			elif(Stuff.Price[x] > HiPoint):
				HiPoint = Stuff.Price[x]
				SevPerc = HiPoint * 0.1

			# if Stuff.Chg[x] < 0.07:
			# 	print("Sell On: " + Stuff.Date[x])
			# 	break

			
		return x, ( Stuff.Price[x] - Stuff.Price[StartIndex]) #returning next index and profit
	

with open("DataWithEMA.csv", "r") as CSVDataFile:
	DataFile = pd.read_csv(CSVDataFile)
	Data = DataFile[["Date","Price","Chg","SevOverFortyFlag","SixOverTwenOneFlag"]] #The dataframe thingy
	# When to buy
	x,TotProf,TradP,TradL = 0,0,0,0
	while (x<1726):
		if(Data.SevOverFortyFlag[x]):
			print("Buy On: "+Data.Date[x])
			x, prof = SellDate(Data,x+1)
			if(prof > 0):
				TradP = TradP + 1
			else:
				TradL = TradL + 1
			TotProf = TotProf + prof
		if(x<1726 and Data.SevOverFortyFlag[x] and Data.SixOverTwenOneFlag[x] ):
			print("Buy On: "+Data.Date[x])
			x, prof  = SellDate(Data, x+1)
			if(prof > 0):
				TradP = TradP + 1
			else:
				TradL = TradL + 1
			TotProf = TotProf+prof
		else:
			x = x+1
	print("Total Profit Made: " + str(TotProf))
	print("Total Trade With Profit: " + str(TradP))
	print("Total Trade With Loss: " + str(TradL))
	print("Win:Loss: " + str(TradP/TradL))



