# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 10:59:56 2018

@author: SAMEERGO
"""

word_matrix_train = []
y= []


import urllib.request
import re
from sklearn import svm
from bs4 import BeautifulSoup

    
#print (soup)
#%%

re_digit = re.compile('^\d')
re_colon = re.compile(':')
re_fullstop = re.compile('[a-zA-Z]+\.')
  
#%%

def buiild_trainingset(line,out):
            global word_matrix_train
            global y
            words = line.split(' ')
            word_len = len(words)
            line_mat = []
            line_mat.append(word_len/30)
            dig = int(bool(re_digit.search(line)))
            line_mat.append(dig)
            col= int(bool(re_colon.search(line)))
            line_mat.append(col)
            up_case = sum(map(str.isupper, line))/(1 + sum(map(str.islower, line)) + sum(map(str.isupper, line)))
            line_mat.append(5*up_case)
            fstop = int(bool(re_fullstop.search(line)))
            line_mat.append(fstop)
            word_matrix_train.append(line_mat)
            y.append(out)
#%%

def  section_separator(infile):
        with open (infile) as f:
            lines = f.readlines()
        lines = [x.strip() for x in lines]
        print(lines)
        global word_matrix_train
        word_matrix_train = []
        for line in lines:
            r = urllib.request.urlopen(line).read()
            soup = BeautifulSoup(r, 'html.parser')
            tag = soup.find_all(re.compile('^h[1-6]$'))
            #print (soup)
            for item in tag:
                buiild_trainingset(item.get_text(),1) 
            tag = soup.find_all('p')
            #print(tag)
            for item in tag:
                buiild_trainingset(item.get_text(),0)
            global y
            print(y)
            print(len(word_matrix_train))
        sep = svm.SVC()      
        sep.fit(word_matrix_train,y)
        print(sep.predict([[2/30,0,0,0.6,0],[3/30,1,0,0.6,0]]))
        y= []
        f.close()

section_separator('Features_section_separator1.txt')

#%%
