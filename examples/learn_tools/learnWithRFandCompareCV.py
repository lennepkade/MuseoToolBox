# -*- coding: utf-8 -*-
"""
Learn with Random-Forest and compare Cross-Validation methods
===============================================================

This example shows how to make a classification with different cross-validation methods.

"""

##############################################################################
# Import librairies
# -------------------------------------------

from museotoolbox.learn_tools import learnAndPredict
from museotoolbox import cross_validation
from museotoolbox import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold

##############################################################################
# Load HistoricalMap dataset
# -------------------------------------------

raster,vector = datasets.historicalMap(low_res=True)
field = 'Class'
group = 'uniquefid'

##############################################################################
# Initialize Random-Forest
# ---------------------------

classifier = RandomForestClassifier(random_state=12,n_jobs=1)

##############################################################################
# Create list of different CV
# ---------------------------

CVs = [cross_validation.RandomStratifiedKFold(n_splits=2),
       cross_validation.LeavePSubGroupOut(valid_size=0.5),
       cross_validation.LeaveOneSubGroupOut(),
       StratifiedKFold(n_splits=2,shuffle=True) #from sklearn
       ]

kappas=[]

LAP = learnAndPredict(n_jobs=1)

for cv in CVs : 
        
    LAP.learnFromRaster(raster,vector,inField=field,group=group,cv=cv,
                        classifier=classifier,param_grid=dict(n_estimators=[50,100]))
    print('Kappa for '+str(type(cv).__name__))
    cvKappa = []
    
    for stats in LAP.getStatsFromCV(confusionMatrix=False,kappa=True):
        print(stats['kappa'])
        cvKappa.append(stats['kappa'])
    
    kappas.append(cvKappa)
    
    print(20*'=')

##########################
# Plot example


from matplotlib import pyplot as plt
plt.title('Kappa according to Cross-validation methods')
plt.boxplot(kappas,labels=[str(type(i).__name__) for i in CVs], patch_artist=True)
plt.grid()
plt.ylabel('Kappa')
plt.xticks(rotation=15)
plt.show()
