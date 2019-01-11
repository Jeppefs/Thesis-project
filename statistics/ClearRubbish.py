import os 
import pandas 

for directory in os.listdir("data"):
    if os.path.exists("data/"+ directory + "/dataEnd.csv") == True:
        dataEnd = pandas.read_csv("data/"+ directory +"/dataEnd.csv")
        if "Unnamed: 0" in dataEnd.keys():
            dataEnd = dataEnd.set_index("Unnamed: 0")
        if "halfMean" in dataEnd.keys():
            dataEnd.loc[:, "mean"] = dataEnd.loc[:, "halfMean"]
            dataEnd.loc[:, "variance"] = dataEnd.loc[:, "variance"]
            dataEnd.drop(labels = ["halfMean", "halfVariance"], axis = 'columns', inplace=True) 
    
            dataEnd.to_csv("data/" +  directory + "/dataEnd.csv", index=False)
            
            print(directory)
        else:
            dataEnd.to_csv("data/" + directory + "/dataEnd.csv",index=False)