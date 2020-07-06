import pandas as pd
import csv


#Smoothed DMI = sum[1:14](DM) - (sum[1:14](DM)/14) + Current_DM

def SmoothAf(Data,x,atr):
	SerP = pd.Series(Data[x-14:x+1].DM_P).sum()
	SerN = pd.Series(Data[x-14:x+1].DM_N).sum()

	SmP = SerP - (SerP/14) + Data.DM_P[x]
	SmN = SerN - (SerN/14) + Data.DM_N[x]

	DI_P = ((SmP + Data.DM_P[x])/atr) * 100
	DI_N = ((SmN + Data.DM_N[x])/atr) * 100

	DX = (abs(DI_P - DI_N)/abs(DI_P+DI_N)) * 100

	return DX

with open("DataWithEMA.csv", "r") as CSVDataFile:
	DataFile = pd.read_csv(CSVDataFile)

	ComputeData = DataFile[["Date","Price","Chg","Av_Sev","Av_OneFrty","SevOverFortyFlag","Av_Six","Av_TwenOne","SixOverTwenOneFlag","DM_P","DM_N","TR"]] #All the fuckin data
	EMADataFile = open("DataFiles\\ADXandATRData.csv", "w", newline="\n")#File we are writing data to; This command won't work if the directory doesn't exist already. You will have to make a directory before you flush data here.I feel like this looks more organised
	
	EMAWriter = csv.writer(EMADataFile)
	EMAWriter.writerow(["Date","Price","Chg","Av_Sev","Av_OneFrty","SevOverFortyFlag","Av_Six","Av_TwenOne","SixOverTwenOneFlag","DM_P","DM_N","ATR","ADX"])#Header for our write file
	EMAWriter.writerow([ComputeData.Date[0],ComputeData.Price[0],ComputeData.Chg[0],ComputeData.Av_Sev[0],ComputeData.Av_OneFrty[0],ComputeData.SevOverFortyFlag[0],ComputeData.Av_Six[0],ComputeData.Av_TwenOne[0],ComputeData.SixOverTwenOneFlag[0],ComputeData.DM_P[0],ComputeData.DM_N[0],ComputeData.TR[0],0]) #Date,Price,Chg,Av_Sev,Av_OneFrty,FlagFor70>140,six,twentyone,FlagFor6>21,DI_P,DI_N,TR,ADX

	DX_Vals = [] #Will be our Queue FIFO with 15 values to give us our average
	for x in range(1,1726):
		#Calculate ADX and ATR in 14 day intervals
		ADX = 0
		ATR = 0
		if(x<14):
			ADX = (abs(ComputeData.DM_P[x] - ComputeData.DM_N[x])/abs(ComputeData.DM_P[x] + ComputeData.DM_N[x])) * 100
			ATR  = pd.Series(ComputeData[:x+1].TR).mean()
			DX_Vals.append(ADX)
		else:
			ATR = pd.Series(ComputeData[x-14:x+1].TR).mean()
			DX = SmoothAf(ComputeData,x,ATR)
			DX_Vals.pop(0) #Remove old value
			DX_Vals.append(DX) #Add new value
			ADX = sum(DX_Vals)/15 #Find Average of added value



		EMAWriter.writerow([ComputeData.Date[x],ComputeData.Price[x],ComputeData.Chg[x],ComputeData.Av_Sev[x],ComputeData.Av_OneFrty[x],ComputeData.SevOverFortyFlag[x],ComputeData.Av_Six[x],ComputeData.Av_TwenOne[x],ComputeData.SixOverTwenOneFlag[x],ComputeData.DM_P[x],ComputeData.DM_N[x],ATR,ADX]) #Date,Price,Chg,Av_Sev,Av_OneFrty,FlagFor70>140,six,twentyone,FlagFor6>21,DI_P,DI_N,TR,ADX


