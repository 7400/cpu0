# ALL NUMBERS ARE PIN NUMBERS ON THE RPI HEADER
# do not confuse with the other naming scheme, e.g. gpio3

# data bus from LSB to MSB
data = 3,5,7,11,13,15,19,21 # black-purple

'''
23 orange
25-27 nc
29-37 yellow-grey
'''

# control lines
# using a pin for multiple things is ok as long as you only need one at a time

# L=active lo
# H=active hi
# R=rising edge triggered
# F=falling edge triggered

# RPI
pi_send = 33,"H" # rpi sending or receiving data bus

# memory board
xl_load = 29,"R"
xh_load = 31,"R"
mem_we  = 35,"F"
#mem_oe = not pi_send

# ALU
d_load   = 29,"R"
b_load   = 31,"R"
#d_oe    = not pi_send
cout     = 23,"N"

# program counter
pc_clear = ''
pc_load  = ''
pc_inc   = ''
