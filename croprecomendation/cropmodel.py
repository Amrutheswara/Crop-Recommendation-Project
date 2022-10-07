import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pickle


dataset=pd.read_csv('cpdata.csv')

x=dataset.iloc[:,[0,1]].values

y=dataset.iloc[:,[4]].values

xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=110)

ytrain=np.ravel(ytrain)

classifier=KNeighborsClassifier(n_neighbors=3)
classifier.fit(xtrain,ytrain)

file=open('knncrop.pkl','wb')
pickle.dump(classifier,file)
file.close()



