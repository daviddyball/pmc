#!/usr/bin/env python

import sys
from pmc import Main

if __name__ == '__main__':
    if '-d' in sys.argv:
        Main(debug=True).run()
    else:
        Main().run()
