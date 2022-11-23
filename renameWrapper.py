import rename
import logging
logging.basicConfig(filename='renameEntry.log',level=logging.DEBUG)
import sys

if len(sys.argv)>=3:
    parts = sys.argv[1:]
    directory = " ".join(parts)
else:
    directory = sys.argv[1]

logging.info("Renaming individual directory: "+ directory)
rename.cleanIndividualFolder(directory)