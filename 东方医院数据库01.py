# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import pandas as pd
from datetime import datetime
import numpy as np
__author__ = 'Administrator'

#gcp报告结果导出
def gen_df_from_gcp():
    #ok.xlsx
    df3=pd.read_excel('data/GCP报告结果导出.xlsx')
    df3_sample=df3[['病人姓名','标本日期','项目名称','检验结果']]
    df4=pd.read_excel('data/科研报告结果导出.xls')
    df4_sample=df4[['病人姓名','标本日期','项目名称','检验结果']]
    df=pd.concat([df3_sample,df4_sample],axis=0,ignore_index=True)
    #df3=df3.ix[df3['病人姓名']=='蔡卫国']
    headers=list(set(df['项目名称']))
    d={}
    date_name_df=df[['病人姓名','标本日期']]
    date_name_df.drop_duplicates(inplace=True)
    for index,item in date_name_df.iterrows():
        name=item['病人姓名']
        if name in d:
            d[name].append(item['标本日期'])
        else:
            d[name]=[item['标本日期']]
    result_l=[]
    for key,values in d.items():
        for value in values:
            df_tmp=df.ix[(df['病人姓名']==key)&(df['标本日期']==value)]
            tmp_dict={'病人姓名':key,'标本日期':value}
            new_keys=list(df_tmp['项目名称'])
            new_values=list(df_tmp['检验结果'])
            for k,v in zip(new_keys,new_values):
                tmp_dict[k]=v
            result_l.append(tmp_dict)
    headers.insert(0,'病人姓名')
    headers.insert(1,'标本日期')
    df=pd.DataFrame(result_l,columns=headers)
    return(df)



#病人的姓名、年龄、性别
def get_info():
    df=pd.read_excel('data/GCP报告结果导出.xlsx')
    df_sample=df[['病人姓名','性别','年龄']]
    df2=pd.read_excel('data/科研报告结果导出.xls')
    df2_sample=df2[['病人姓名','性别','年龄']]
    df=pd.concat([df_sample,df2_sample],axis=0,ignore_index=True)
    names=list(set(df['病人姓名']))
    info_list=[]
    for name in names:
        tmp_dict={}
        tmp_dict['病人姓名']=name
        tmp_df=df.ix[df['病人姓名']==name]
        if len(list(set(tmp_df['性别'])))==0:
            continue
        tmp_dict['性别']=list(set(tmp_df['性别']))[0]
        tmp_dict['年龄']=list(set(tmp_df['年龄']))[0]
        info_list.append(tmp_dict)
    #return pd.DataFrame(info_list)
    df=pd.DataFrame(info_list)
    #df.dropna(inplace=True)
    return df

#心衰(1).xls表中的数据日期规整
def order():
    df2=pd.read_excel('data/心衰(1).xls')
    in_time=list(df2['入院时间'])
    times=[i.strftime('%Y-%m-%d') for i in in_time]
    out_time=list(df2['出院时间'])
    times2=[i.strftime('%Y-%m-%d') for i in out_time]
    df2['入院时间']=times
    df2['出院时间']=times2
    return df2
def f(x):
    if isinstance(x,str):
        return x.replace('.','-')
    return x

#中西医治疗组.xls数据简化
def east_west():
    df_first=pd.read_excel('data/中西医治疗组心超基线及随访数据新建.xls',header=2,sheetname='first')
    df_second=pd.read_excel('data/中西医治疗组心超基线及随访数据新建.xls',header=2,sheetname='second')
    df_1=pd.concat([df_first,df_second],axis=0,ignore_index=True)
    df_third=pd.read_excel('data/中西医治疗组心超基线及随访数据新建.xls',header=2,sheetname='third')
    df_2=pd.concat([df_1,df_third],axis=0,ignore_index=True)
    df_2.dropna(axis=0,inplace=True)
    df_2.drop_duplicates(inplace=True)
    dates=[f(i) for i in list(df_2['日期'])]
    df_2['日期']=dates
    df_2.to_excel('new中西医治疗组心超基线及随访数据新建.xls')

#融合心衰与查检验不带分组.xlsx
def get_it():
    df=order()
    #print(df.ix[df['病人姓名']=='蔡卫国'])
    df2=pd.read_excel('data/检查检验不带分组.xlsx')
    in_times=list(map(f,list(df2['入院时间'])))
    out_times=list(map(f,list(df2['出院时间'])))
    df2['入院时间']=in_times
    df2['出院时间']=out_times
    del df2['住院号']
    df_result=pd.merge(df2,df,how='left',on=['病人姓名','入院时间','出院时间'])
    #df_result.to_excel('蔡卫国.xlsx')
    #print('end')
    return df_result

#使gcp-科研报告.xlsx的标本日期变成统一格式
#16.08.25
#2016-01-04 00:00:00

def format_date(x):
    if isinstance(x,datetime):
        return x.strftime('%Y-%m-%d')
    if isinstance(x,str) and '.' in x:
        ss=x.split('.')
        return '20{}-{}-{}'.format(ss[0],ss[1],ss[2])
    return x
def final(df):
    #df=pd.read_excel('蔡卫国.xlsx')
    df2=pd.read_excel('new中西医治疗组心超基线及随访数据新建.xls')
    add_list=[]
    for index,sereis in df.iterrows():
        name=sereis['病人姓名']
        start_time=sereis['入院时间']
        end_time=sereis['出院时间']
        tmp=df2.ix[(df2['病人姓名']==name)&(df2['日期']<=end_time)&(df2['日期']>=start_time)]
        del tmp['病人姓名']
        if len(tmp)!=0:
            add_list.append(list(tmp.loc[tmp.index[0]]))
        else:
            add_list.append([None]*5)
    num_1,num_2,num_3,num_4,num_5=zip(*add_list)
    df['日期']=list(num_1)
    df['左房内径']=list(num_2)
    df['舒张末期']=list(num_3)
    df['收缩期']=list(num_4)
    df['EF']=list(num_5)
    return df



def true_final():
    df=pd.read_excel('最终结果.xlsx')
    #df_tmp=df[:2]
    df_result=df.ix[(df['入院症状:乏力']==0)|(df['入院症状:乏力']==1)]
    df_result.to_excel('最终结果.xlsx')
    print('end')
#重新生成检查检验不带分组.xlsx
def new_xlsx():
    df2=pd.read_excel('data/检查检验不带分组.xlsx')
    in_times=[f(i) for i in list(df2['入院时间'])]
    out_times=[f(i) for i in list(df2['出院时间'])]
    df2['入院时间']=in_times
    df2['出院时间']=out_times
    del df2['住院号']
    df2.to_excel('new检查检验不带分组.xlsx')
    print('end')
if __name__=='__main__':
    '''
    df=pd.read_excel('second_to_last.xlsx')
    df2=pd.read_excel('gcp-科研报告_new.xlsx')
    df3=pd.merge(df,df2,how='left',on='病人姓名')
    df_result=df3.ix[(df3['入院时间']<=df3['标本日期'])&(df3['出院时间']>=df3['标本日期'])]
    df_result_2=df3[['病人姓名','入院时间','出院时间','标本日期']]
    print(df_result)
    print('-'*30)
    print(df_result_2.head(10))
    print('end')
    #print(df_tmp['入院症状:心悸'][0]!=0 and df_tmp['入院症状:心悸'][0]!=1)
    #print(len(set(list(df3['病人姓名']))))
    #dff=pd.read_excel('second_to_last.xlsx')
    #numbers=len(set(list(dff['病人姓名'])))
    #print(numbers)
    df=pd.read_excel('data/检查检验不带分组.xlsx')
    numbers=len(set(list(df['病人姓名'])))
    print(numbers)
    print('-'*30)
    df=pd.read_excel('最终结果.xlsx')
    numbers=len(set(list(df['病人姓名'])))
    print(numbers)
    df=get_it()
    df3=final(df)
    df3.to_excel('new.xlsx')
    print('end')
    df=pd.read_excel('new.xlsx')
    numbers=len(set(list(df['病人姓名'])))
    print(numbers)'''
    #df=pd.read_excel('结果.xlsx')
    #df2=final(df)
    #df2.to_excel('结果.xlsx')
    df=pd.read_excel('结果.xlsx')
    numbers=len(set(list(df['病人姓名'])))
    print(numbers)
    #df=pd.read_excel('result.xlsx')
    #df.drop_duplicates(inplace=True)
    #df.to_excel('结果.xlsx')
