import sys
from api import API
from history import History
from computation import Computation
def main():
    test = API()
    test.myfunc()
    test = History()
    test.myfunc()
    test = Computation()
    test.myfunc()
    return 0

main()