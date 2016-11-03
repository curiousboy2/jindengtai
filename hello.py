# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import pandas as pd
__author__ = 'Administrator'

#gcp报告结果导出
def gen_df_from_gcp():
    #ok.xlsx
    df3=pd.read_excel('data\GCP报告结果导出.xlsx')
    df3_sample=df3[['病人姓名','标本日期','项目名称','检验结果']]
    df4=pd.read_excel('data\科研报告结果导出.xls')
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
    df=pd.read_excel('data\GCP报告结果导出.xlsx')
    df_sample=df[['病人姓名','性别','年龄']]
    df2=pd.read_excel('data\科研报告结果导出.xls')
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

if __name__=='__main__':
    '''
    df_main=pd.read_excel('data/中西医治疗组心超基线及随访数据新建.xls',header=2)
    df_2=pd.read_excel('data/检查检验不带分组.xlsx')
    df_middle_1=pd.merge(df_main,df_2,how='left',on='病人姓名')
    df_gcp=pd.read_excel('ok.xlsx')
    df_middle_2=pd.merge(df_middle_1,df_gcp,how='left',on='病人姓名')
    df_info=get_info()
    df=pd.merge(df_middle_2,df_info,how='left',on='病人姓名')
    #print(df)
    df.to_excel('result.xlsx')
'''
    df=pd.read_excel('gcp_report.xlsx')
    df2=pd.read_excel('hello.xlsx')
    df_result=pd.merge(df,df2)
    df_result.to_excel('midell.xlsx')
