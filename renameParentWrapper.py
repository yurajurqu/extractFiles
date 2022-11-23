import rename
import logging
logging.basicConfig(filename='rename.log',level=logging.DEBUG)
import sys, traceback


if len(sys.argv)>=3:
    parts = sys.argv[1:]
    directory = " ".join(parts)
else:
    directory = sys.argv[1]
logging.info("Renaming parent directory: "+ directory)
try:
    rename.processParentDirectory(directory)
except:
    print ("Exception in user code:")
    traceback.print_exc(file=sys.stdout)
    # input("Waiting...")