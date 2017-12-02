from test import *
printHelloWordInSameDir()

import test
test.printHelloWordInSameDir()

import sys
sys.path.append('./modules/')
from testInModules import * 
printHelloWordInModule()