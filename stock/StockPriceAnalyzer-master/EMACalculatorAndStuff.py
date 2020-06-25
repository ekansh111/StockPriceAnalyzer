import pandas as pd
import csv

def EMA_Calculator(Data,Days,Prev):
	# EMA=Price(t)×k+EMA(y)×(1−k)
	# where:
	# t=today
	# y=yesterday
	# N=number of days in EMA
	k=2/(Days+1)	 	
	EMA = (Data*k) + (Prev *(1-k))
	return EMA
def reset_my_index(df):
	res = df[::-1].reset_index(drop=True)
	return(res)	

with open("NotFucked.csv", "r") as CSVDataFile:
	DataFile = pd.read_csv(CSVDataFile)
	ComputeData = DataFile[["Date","Price","Chg"]]
	# ComputeData.reindex(index=ComputeData.index[::-1])
	ComputeData = reset_my_index(ComputeData)
	EMADataFile = open("DataWithEMA.csv", "w", newline="\n")
	EMAWriter = csv.writer(EMADataFile)
	EMAWriter.writerow(["Date","Price","Chg","Av_Sev","Av_OneFrty"])
	# print(ComputeData.Price[0])
	EMAWriter.writerow([ComputeData.Date[0],ComputeData.Price[0],ComputeData.Chg[0],ComputeData.Price[0],ComputeData.Price[0]]) #First Row

	Mean140,Mean7 = 0,0
	for x in range(1,ComputeData.size):
		if (x < 70):
			MeanPrice = ComputeData[:x].mean().Price
			EMAWriter.writerow([ComputeData.Date[x],ComputeData.Price[x],ComputeData.Chg[x],MeanPrice,MeanPrice]) #Date,Price,Chg,Av_Sev,Av_OneFrty
		elif(x<140):
			Mean7 = ComputeData[(x-70):x].mean().Price
			Mean140 = ComputeData[:x].mean().Price
			EMAWriter.writerow([ComputeData.Date[x],ComputeData.Price[x],ComputeData.Chg[x],Mean7,Mean140])
	Old7,Old140,= Mean7,Mean140
	for x in range(140,1726):
		# print(x)
		amt = ComputeData.Price[x]
		Mean7 = EMA_Calculator(amt,70,Old7)
		Old7 = Mean7
		Mean140 = EMA_Calculator(amt,140,Old140)
		Old140 = Mean140
		EMAWriter.writerow([ComputeData.Date[x],ComputeData.Price[x],ComputeData.Chg[x],Mean7,Mean140])





