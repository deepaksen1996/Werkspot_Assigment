#!/usr/bin/env python
# coding: utf-8

# In[8]:

import os
import pandas as pd
import datetime
from tqdm import tqdm


# In[2]:


#data preprocessing 
df = pd.read_csv('event_log.csv', sep=';')
df.drop(['meta_data'], axis=1, inplace=True)
df['created_at'] = pd.to_datetime(df['created_at'])
df.head()


# In[4]:


#fucntion for new columns status which shows activity for the entry date
def func(entry):
    if entry in ['proposed', 'became_able_to_propose']:
        return 1
    else:
        return 0
def getdate(x):
    return x.date()
def gettime(x):
    return x.time()


# In[6]:


#new columns creation
df['status'] = list(map(func, df['event_type']))
df['date'] = list(map(getdate, df['created_at']))
df['time'] = list(map(gettime, df['created_at']))


# In[9]:


#list of all dates present in data
list_date = sorted(list(df['date'].unique()))


# In[11]:


#function to retrive active ids on am emtry date
def new(uni_date):
    df_1 = pd.DataFrame()
    df_temp = df[df['date']==uni_date]
    for i in list(df_temp['professional_id_anonymized'].unique()):
        d_tmp = df_temp[df_temp['professional_id_anonymized']==i]
        tt = df_temp[df_temp['professional_id_anonymized']==i]['time'].max()
        df_1 = pd.concat([df_1, d_tmp[d_tmp['time']==tt]])
    return df_1

df_f = []
for i in tqdm(list_date):
    df_result = new(i)
    list_0 = df_result[df_result['status']==0]['professional_id_anonymized']
    list_1 = df_result[df_result['status']==1]['professional_id_anonymized']
    df_f.append([df_result['date'].unique(), list_0, list_1])


# In[15]:


#appending final unique active professionals count on a date
final_list = []
for idx, entry in enumerate(df_f):
    if idx==0:
        final_list.append([df_f[idx][0], len(set(df_f[idx][2]))])
        pass
    else:
        diff = list(set(df_f[idx-1][2])-set(df_f[idx][1])-set(df_f[idx][2]))
#         print('_'*60)
#         print(df_f[idx][0])
#         print()
#         print(sorted(set(df_f[idx][2])))
#         print()
#         print(sorted(set(diff)))
#         print()
#         print(df_f[idx][0], len(set(df_f[idx][2]))+len(set(diff)))
        final_list.append([df_f[idx][0], len(set(df_f[idx][2]))+len(set(diff))])


# In[16]:


#creating a dataframe to save results
df_end = pd.DataFrame(final_list, columns=['date', 'active'])
print(os.listdir())
df_end.to_csv('availability_snapshot.csv', header=True)
while True:
    print('Output file generated copy from container to local and kill the process')

# In[ ]:





# In[ ]:




