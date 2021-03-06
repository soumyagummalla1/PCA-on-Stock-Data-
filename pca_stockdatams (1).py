# -*- coding: utf-8 -*-
"""PCA_StockDataMS.ipynb



import pandas as pd
from pandas_datareader import DataReader
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
 
ms = DataReader('MS',  'yahoo', datetime(2019,1,1), datetime(2019,8,31))
returns = pd.DataFrame(np.diff(np.log(ms['Adj Close'].values)))
returns.index = ms.index.values[1:ms.index.values.shape[0]]
returns.columns = ['MS Returns']

spy = DataReader('SPY',  'yahoo', datetime(2019,1,1), datetime(2019,8,31))
returns1 = pd.DataFrame(np.diff(np.log(spy['Adj Close'].values)))
returns1.index = spy.index.values[1:spy.index.values.shape[0]]
returns1.columns = ['SPY Returns']

jpm = DataReader('JPM',  'yahoo', datetime(2019,1,1), datetime(2019,8,31))
returns2 = pd.DataFrame(np.diff(np.log(jpm['Adj Close'].values)))
returns2.index = jpm.index.values[1:jpm.index.values.shape[0]]
returns2.columns = ['JPM Returns']

bac = DataReader('BAC',  'yahoo', datetime(2019,1,1), datetime(2019,8,31))
returns3 = pd.DataFrame(np.diff(np.log(bac['Adj Close'].values)))
returns3.index = bac.index.values[1:bac.index.values.shape[0]]
returns3.columns = ['BAC Returns']

gs = DataReader('GS',  'yahoo', datetime(2019,1,1), datetime(2019,8,31))
returns4 = pd.DataFrame(np.diff(np.log(gs['Adj Close'].values)))
returns4.index = gs.index.values[1:gs.index.values.shape[0]]
returns4.columns = ['GS Returns']

ms1=ms[['Adj Close']]
spy1=spy[['Adj Close']]
jpm1=jpm[['Adj Close']]
bac1=bac[['Adj Close']]
gs1=gs[['Adj Close']]
spy1

from functools import reduce
data_frames = [ms1, spy1,jpm1,bac1,gs1]
df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],
                                            how='outer'), data_frames)
df_merged.columns = ['MS', 'SPY','JPM','BAC','GS']
df_merged

#ms1=ms[['Adj Close']]
rs = df_merged.apply(np.log).diff(1) 
rs.plot(title='Daily Returns of the Stocks')

(rs.cumsum().apply(np.exp)).plot(legend=0, figsize=(10,6), grid=True, title='Cumulative Returns of the Stocks')
plt.tight_layout()

from sklearn.decomposition import PCA
pca = PCA(1).fit(rs.fillna(0))

pc1 = pd.Series(index=rs.columns, data=pca.components_[0])
pc1.plot(grid=True, title='PCA for the 5 competitors')
plt.tight_layout()

pc1

weights = abs(pc1)/sum(abs(pc1))
myrs = (weights*rs).sum(1)
myrs.cumsum().apply(np.exp).plot()

fig, ax = plt.subplots(2,1, figsize=(10,6))
pc1.nsmallest(10).plot.bar(ax=ax[0], color='green', grid=True, title='Stocks with Most Negative PCA Weights')
pc1.nlargest(10).plot.bar(ax=ax[1], color='blue', grid=True, title='Stocks with Least Negative PCA Weights')

plt.tight_layout()

