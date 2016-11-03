import pandas as pd

df=pd.DataFrame([[1,2,3],[1,2,3],[4,5,6]],columns=['a','b','c'])
print(df)
df2=df.drop_duplicates()
print('-'*20)
df3=pd.concat([df,df2],axis=0,ignore_index=True)
print(df3)