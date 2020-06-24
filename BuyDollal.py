import csv
import pandas as pd

def SellDate(Stuff,StartIndex):
		x = StartIndex
		while (x<1726):
			if(Stuff.Chg[x] <= -0.7):
				print("Sell On: "+Stuff.Date[x])
				break
			x = x+1
		return x
	

with open("DataWithEMA.csv", "r") as CSVDataFile:
	DataFile = pd.read_csv(CSVDataFile)
	Data = DataFile[["Date","Price","Chg","Av_Sev","Av_OneFrty"]] #The dataframe thingy
	# When to buy
	x = 0
	while (x<1726):
		if(Data.Av_Sev[x]>Data.Av_OneFrty[x]):
			print("Buy On: "+Data.Date[x])
			x = SellDate(Data,x+1)
		else:
			x = x+1


