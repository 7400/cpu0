#! /usr/bin/env python

import random
import sys
import time
from itertools import islice, izip, repeat, cycle

from rpi_util import *
from pins import *

init(data, (pi_send, xl_load, xh_load, mem_we), ())

def gray(n):
    ''' https://en.wikipedia.org/wiki/Gray_code '''
    for i in xrange(1<<n):
        yield i ^ (i >> 1)

def antigray(n):
    ''' gray code changes one bit at a time, this changes as many as possible '''
    m=(1<<n)-1
    for i in gray(n-1):
        yield i
        yield (~i)&m

def setaddr(a):
    put(a&0xff)
    ctl(xl_load)
    put(a>>8)
    ctl(xh_load)

def fillmem(addrs, dat):
    for a,d in izip(addrs, dat):
        setaddr(a)
        put(d)
        ctl(mem_we)

def dumpmem(addrs):
    v = []
    for a in addrs:
        setaddr(a)
        v.append(get())
    return v

def gen0():
    while 1:
        yield random.randint(0,0xff)

def gen1():
    '''
    either the odd items or even items are all 0xff
    remaining items have 1 bit set
    '''
    ff = random.random() < .5
    one = cycle(cylon())
    while 1:
        if ff: yield 0xff
        ff = 1
        yield one.next()

def readtest(addrs, dat):
    err = 0
    for a,w,r in izip(addrs, dat, dumpmem(addrs)):
        if w != r:
            print 'address {:04x}  expect {:08b}  got {:08b}'.format(a, w, r)
            err += 1
    return err

def cylona():
    ''' cylon the address bus '''
    for i in cycle(cylon(xrange(16))):
        setaddr(i)
        time.sleep(.2)

def main():
    write = 1
    passes = 0
    errors = 0
    #addrs = range(0x1000)
    addrs = tuple(antigray(12))
    #dat = cycle(xrange(0x100))
    #dat = gen0()
    dat = gen1()
    while 1:
        for i in xrange(0, 0x1000, 0x8000):
            a = [i+j for j in addrs]
            d = tuple(islice(dat, len(a)))
            if write: fillmem(a, d)
            e = readtest(a, d)
            sys.stdout.write('x' if e else '.')
            sys.stdout.flush()
            errors += e
            write = 1
        passes += 1
        print ' passes', passes, 'errors', errors

#while 1:dcycle(cylon())
#cylona()
main()
