#! /usr/bin/env python

from rpi_util import *
from pins import *

import random
import time

init(data, (pi_send, b_load, d_load), (cout,))

def sub(a, b):
    ''' ALU result of a-b '''
    put(b)
    ctl(b_load)
    put(a)
    c = getpin(cout)
    ctl(d_load)
    return get(), c

def expect(a, b):
    ''' expected result of a-b '''
    r = a + ((~b) & 0xff) + 1
    return r & 0xff, r > 0xff

def check(a, b):
    ''' return True for correct operation '''
    d,c = sub(a, b)
    xd,xc = expect(a, b)
    if d == xd and c == xc: return True
    print '{:08b} - {:08b} = {:1b}:{:08b} got {:1b}:{:08b}'.format(a, b, xc, xd, c, d)
    return False

def test():
    err = 0
    for a in xrange(0x100):
        for b in xrange(0x100):
            if not check(a, b): err += 1
    return err

def main():
    pas = 0
    err = 0
    while 1:
        err += test()
        pas += 1
        print 'passes',pas,'errors',err

main()
