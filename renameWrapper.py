import rename
import logging
logging.basicConfig(filename='extractEntry.log',level=logging.DEBUG)
import sys

directory = sys.argv[1]
logging.info("Renaming individual directory: "+ directory)
rename.cleanIndividualFolder(directory)