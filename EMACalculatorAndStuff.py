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
	EMAWriter.writerow(["Date","Price","Chg","Av_Sev","Av_OneFrty","SevOverFortyFlag","Av_Six","Av_TwenOne","SixOverTwenOneFlag"])
	# print(ComputeData.Price[0])
	EMAWriter.writerow([ComputeData.Date[0],ComputeData.Price[0],ComputeData.Chg[0],ComputeData.Price[0],ComputeData.Price[0],False,ComputeData.Price[0],ComputeData.Price[0], False]) #First Row

	Mean140,Mean7,Old7,Old06,Old21,Old140 = 0,0,0,0,0,0
	FlagSev, FlagSix = False, False
	for x in range(1,1726):
		if(x < 6):
			MeanPrice = ComputeData[:x].mean().Price
			Mean06,Mean21,Mean140,Mean7 = MeanPrice,MeanPrice,MeanPrice,MeanPrice
			FlagSev,FlagSix = False, False
			Old6 = MeanPrice
			
		elif (x < 21): #EMA For 6 save old 21 day value
			amt = ComputeData.Price[x]
			MeanPrice = ComputeData[:x].mean().Price
			Mean06 = EMA_Calculator(amt,6,Old06)
			Mean21,Mean140,Mean7 = MeanPrice,MeanPrice,MeanPrice
			FlagSev,FlagSix = False, False
			Old06 = Mean06
			Old21 = MeanPrice
		elif(x<70): #EMA for 6,21, save old 70 day value
			amt = ComputeData.Price[x]
			Mean06 = EMA_Calculator(amt,6,Old06) #6DayEMA
			Mean21 = EMA_Calculator(amt,21,Old21)#21 day EMA
			Old06, Old21 = Mean06, Mean21 
			FlagSix = Mean06 > Mean21
			MeanPrice = ComputeData[:x].mean().Price #Mean for 70 and 140
			Old7 = MeanPrice
			Mean140,Mean7 = MeanPrice,MeanPrice
			FlagSev = False
		elif(x<140):#EMA fro 6,21,70, save old value for 140
			amt = ComputeData.Price[x]
			Mean06 = EMA_Calculator(amt,6,Old06) #6DayEMA
			Mean21 = EMA_Calculator(amt,21,Old21)#21 day EMA
			Mean7  = EMA_Calculator(amt,70,Old7) #70 day EMA
			Old6, Old21, Old7 = Mean06, Mean21, Mean21
			MeanPrice = ComputeData[:x].mean().Price #Mean for 140
			Mean140 = MeanPrice
			FlagSix = Mean06 > Mean21
			FlagSev = Mean7>Mean140
			Old140 = MeanPrice
		else: #Calculate everything boiiiii
			amt = ComputeData.Price[x]
			Mean06 = EMA_Calculator(amt,6,Old06) #6DayEMA
			Mean21 = EMA_Calculator(amt,21,Old21)#21 day EMA
			Mean7  = EMA_Calculator(amt,70,Old7) #70 day EMA
			Mean140 = EMA_Calculator(amt,140,Old140) #140 day EMA
			Old6, Old21, Old7,Old140 = Mean06, Mean21, Mean21, Mean140
			FlagSix = Mean06 > Mean21
			FlagSev = Mean7>Mean140


		
		#We now write and flush the calculated Values.
		EMAWriter.writerow([ComputeData.Date[x],ComputeData.Price[x],ComputeData.Chg[x],Mean7,Mean140,FlagSev,Mean06,Mean21,FlagSix]) #Date,Price,Chg,Av_Sev,Av_OneFrty,FlagFor70>140,six,twentyone,FlagFor6>21
	





	# Old7,Old140,= Mean7,Mean140


	# for x in range(140,1726):
	# 	# print(x)
	# 	amt = ComputeData.Price[x]
	# 	Mean7 = EMA_Calculator(amt,70,Old7)
	# 	Old7 = Mean7
	# 	Mean140 = EMA_Calculator(amt,140,Old140)
	# 	Old140 = Mean140
	# 	EMAWriter.writerow([ComputeData.Date[x],ComputeData.Price[x],ComputeData.Chg[x],Mean7,Mean140])





