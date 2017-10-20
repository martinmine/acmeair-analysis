#!/usr/bin/python

from itertools import izip
from csv import reader, writer
import sys

with open(sys.argv[1]) as f:
    with open(sys.argv[2], 'w') as fw:
        writer(fw, delimiter=',').writerows(izip(*reader(f, delimiter=',')))
