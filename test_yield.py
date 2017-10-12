#!/usr/bin/python
#-*- coding: utf-8 -*-
# File Name: test_yield.py
# Created Time: Wed Oct 11 22:24:20 2017

__author__ = 'Crayon Chaney <mmmmmcclxxvii@gmail.com>'

# value = 0

def consumer():
    value = 0
    while 1:
        value = (yield value)
        if value:
            print "consuming ",value
            value = 'return here'
        else:
            break


def process(c):
    now = c.next()
    while now < 5:
        now = now + 1
        print "processing ",now
        msg = c.send(now)
        print msg
    c.close()

if __name__ == '__main__':
    c = consumer()
    process(c)
