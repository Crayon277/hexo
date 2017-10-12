#!/usr/bin/python
#-*- coding: utf-8 -*-
# File Name: cp_code.py
# Created Time: Sun Apr  2 08:53:38 2017

__author__ = 'Crayon Chaney <mmmmmcclxxvii@gmail.com>'

from sys import argv

if len(argv) == 1:
    print 'Please input parameter'
    print 'if want help, enter python cp_code.py h'
elif len(argv) == 2 and argv[1][0].lower() == 'h':
    print "copy source to des... like"
    print "python cp_code.py tmp_code ./source/_post/xxx"
else:    
    source = argv[1]
    des = argv[2]
    with open(argv[1],'r') as fread, open(argv[2],'a') as fwrite:
        for line in fread.readlines():
            fwrite.write(line)

