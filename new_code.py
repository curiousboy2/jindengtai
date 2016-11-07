# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import codecs
import pandas as pd
import docx
import re
import os
import numpy as np
__author__ = 'Administrator'

#对结果.xlsx做初步处理
def f_1():
    df=pd.read_excel('结果.xlsx')
    time1=list(df['入院时间'])  #入院时间
    time2=list(df['标本日期'])  #标本日期
    new_time=['{}{}'.format(i[0],i[1]).strip('nan') for i in zip(time1,time2)]
    df['标本日期']=new_time
    df.sort_values(by=['病人姓名','标本日期'],inplace=True)
    df.to_excel('result_1.xlsx')
    print('end')

#将docx中的文件内容读出，而不过格式

def readDocx(docName):
    fullText = []
    doc = docx.Document(docName)
    paras = doc.paragraphs
    for p in paras:
        fullText.append(p.text)
    file_context='\n'.join(fullText)
    context=re.sub(r'\n+','\n',file_context)
    return context

def one_docx(context):
    row_lists=context.split('\n')
    p_name=row_lists.pop(0)
    p_name=re.sub(r'\d+','',p_name)
    date_str=[i for i in filter(lambda x:re.match('\d+',x),row_lists)]
    date_index=[row_lists.index(y) for y in date_str]
    tmp_d={}
    for j in range(len(date_str)):
        date=date_str[j]
        if j+1<len(date_index):
            start,stop=date_index[j],date_index[j+1]
            tmp_d[date]='\n'.join(row_lists[start:stop])
        else:
            start=date_index[j]
            tmp_d[date]='\n'.join(row_lists[start:])
    return p_name,tmp_d


def main():
    df=pd.read_excel('result_1.xlsx')
    headers=list(df.columns)
    headers.insert(4,'处方日期')
    headers.insert(5,'处方')
    df['处方日期']=[np.nan]*len(df)
    df['处方']=[np.nan]*len(df)
    basedir=os.getcwd()
    series_list=[]
    for one in  os.listdir('data/东方医院15年'):
        context=readDocx('data/东方医院15年/'+one)
        patient_name,tmp_d=one_docx(context)
        biaoben_riqis=list(df.ix[df['病人姓名']==patient_name]['标本日期'])
        if len(biaoben_riqis)==0:
            continue
        biaoben_riqis.sort()
        chuf_riqis=list(tmp_d)
        chuf_riqis.sort()
        for i in chuf_riqis:
            s=pd.Series(index=list(df.columns))
            s['病人姓名']=patient_name
            s['处方日期']=i
            s['标本日期']=i
            series_list.append(s)
    df_chuf=pd.DataFrame(series_list)
    df_chuf=df_chuf[:,headers]
    df=df[:,headers]
    df_result=pd.concat([df,df_chuf],axis=0,ignore_index=True)
    df_result.sort_values(by=['病人姓名','标本日期'],ascending=[True,True],inplace=True,na_position='first')
    df_result.to_excel('result_2.xlsx')
    print('end')
if __name__ == '__main__':
    context=readDocx('data/东方医院15年/100001刘坚.docx')
    #print(context.split('\n'))
    patient_name,tmp_d=one_docx(context)
    #print(patient_name)
    #print(tmp_d['2016.01.27'])
    #print(context.strip('\n')[-2])





