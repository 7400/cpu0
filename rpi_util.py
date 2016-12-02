#! /usr/bin/env python

import atexit
import time

from pins import data, pi_send

import RPi.GPIO as GPIO

def init(data, ctls, inputs):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(data, GPIO.IN)
    msg = "control must be pair (pin#,L/H/R/F)"
    for ctl in ctls:
        assert isinstance(ctl, tuple), msg
        assert len(ctl) == 2, msg
        pin,use = ctl
        assert isinstance(pin, int), msg
        assert isinstance(use, str), msg
        assert len(use) == 1, msg
        assert use[0] in "LHRF", msg
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0 if use in "HR" else 1)
    msg = "input must be pair (pin#,U/D/N)"
    for inp in inputs:
        assert isinstance(inp, tuple), msg
        assert len(inp) == 2, msg
        pin,pull = inp
        assert isinstance(pin, int), msg
        assert isinstance(pull, str), msg
        assert len(pull) == 1, msg
        assert pull[0] in "UDN", msg
        if   pull[0] == "U": GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        elif pull[0] == "D": GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        else               : GPIO.setup(pin, GPIO.IN)
    atexit.register(cleanup)

def cleanup():
    print 'cleanup'
    GPIO.cleanup()

def ctl(ctl, v=None):
    '''
    for active HI, send v
    for active LO, send not v
    for edge trigger, send edge and return to previous level
    '''
    num,use = ctl
    assert GPIO.gpio_function(num) == GPIO.OUT
    if   use == "L":
        GPIO.output(num, not v)
    elif use == "H":
        GPIO.output(num, v)
    elif use == "R":
        GPIO.output(num, 1)
        GPIO.output(num, 0)
    elif use == "F":
        GPIO.output(num, 0)
        GPIO.output(num, 1)

def put(n):
    ''' send to data bus '''
    ctl(pi_send, 1)
    GPIO.setup(data, GPIO.OUT)
    GPIO.output(data, (n&1, n&2, n&4, n&8, n&0x10, n&0x20, n&0x40, n&0x80))

def get():
    ''' read from data bus '''
    GPIO.setup(data, GPIO.IN)
    ctl(pi_send, 0)
    n = 0
    for i,j in enumerate(data):
        if GPIO.input(j): n |= 1 << i
    return n

def getpin(pin):
    return GPIO.input(pin[0])

def cylon(r=None):
    ''' return 'cylon' bit pattern '''
    if r is None: r = range(8)
    else: r = tuple(r)
    return tuple(1<<i for i in r[:-1]) + tuple(1<<i for i in r[-1:0:-1])

def dcycle(values, period=1.):
    ''' cycle data bus through list of values '''
    for i in values:
        put(i)
        time.sleep(period / len(values))

def blink(period=1.):
    ''' blink data bus '''
    dcycle((0, 0xff), period)

def input():
    while 1:
        print "{:08b}".format(get())
        time.sleep(.1)
