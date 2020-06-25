import csv
import pandas as pd

s=0 
net=0 
b=0


def SellDate(Stuff,StartIndex):
		global net
		x = StartIndex
		while (x<1726):
			if(Stuff.Chg[x] <= -0.7):
				print("Sell On: "+Stuff.Date[x])
				s=Stuff.Price[x]

				if b!=0:
					net=s-b+net
					print(net)
				
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
			b=Data.Price[x]
			'''if b!=0:
				net=s-b
			print(net)'''
			x = SellDate(Data,x+1)
		else:
			x = x+1


