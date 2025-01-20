# we need to add the C:\Program Files\WinRAR folder to the PATH environment variable and use CMD to run the script
# command C:/Users/omarb/AppData/Local/Programs/Python/Python38-32/python.exe c:/ws/extractFiles/extractIntoIndividualZips.py
import os
import sys
import rarfile
import zipfile
import shutil
import time
import re
import string
import random
import traceback
import logging
import logging.config
import logging.handlers
import argparse
import subprocess
import platform
import glob
from pyunpack import Archive
import subprocess
import winsound

def processParentDirectory(parentDirectory):
    for root, dirs, files in os.walk(parentDirectory):
        for name in dirs:
            print("Processing directory: " + name)
            directory = os.path.join(root, name)
            processDirectory(directory)
    alertEndOfProcessing()
    alertEndOfProcessing()
    alertEndOfProcessing()

def processDirectory(directory):
    print("Processing directory: " + directory)
    for root, dirs, files in os.walk(directory):
        print(dirs)
        print(files)
        print(root)
        for name in files:
            if name.endswith(".rar"):
                print("Processing rar file: " + name)
                rarFile = os.path.join(root, name)
                print("root: " + root)
                print("name: " + name)
                print("Found rar file: " + rarFile)
                extractRarFile(rarFile)
                extractedFolder = None
                for root, dirs, files in os.walk(directory):
                    #TODO we only need to find the direct child dir, not grand children
                    for name in dirs:
                        print("Processing directory xxx: " + name)
                        if extractedFolder is None:
                            extractedFolder = os.path.join(root, name)
                print("Extracted folder: " + extractedFolder)
                if os.path.exists(extractedFolder):
                    processExtractedFolder(extractedFolder)
                    deleteRarFile(rarFile)
                    deleteExtractedFolder(extractedFolder)
                else:
                    print("!!!!Extracted folder does not exist: " + extractedFolder)
                alertEndOfProcessing()

def alertEndOfProcessing():
    # Frequency (Hz) and Duration (ms)
    frequency = 2000  # 2000 Hz (increased volume)
    duration = 500    # 500 milliseconds (0.5 seconds)
    # Play the beep
    winsound.Beep(frequency, duration)

def extractRarFile(rarFile):
    print("Extracting rar file: " + rarFile)
    rar_path = os.path.dirname(rarFile)
    print("Extracting rar file into path: " + rar_path)
    subprocess.run(["unrar", "x", "-pamourgirls", rarFile, rar_path])
    

def processExtractedFolder(extractedFolder):
    print("Processing extracted folder: " + extractedFolder)
    for root, dirs, files in os.walk(extractedFolder):
        for name in dirs:
            print("Processing directory to cbz: " + name)
            directory = os.path.join(root, name)
            processDirectoryToCbz(directory)

def processDirectoryToCbz(directory):
    grandparent = os.path.dirname(os.path.dirname(directory))
    print("Processing directory to cbz: " + directory)
    for root, dirs, files in os.walk(directory):
        for name in dirs:
            directory = os.path.join(root, name)
            processDirectoryToCbz(directory)
    cbzFile = directory + ".cbz"
    with zipfile.ZipFile(cbzFile, 'w') as myzip:
        for root, dirs, files in os.walk(directory):
            for file in files:
                myzip.write(os.path.join(root, file), file)
    shutil.move(cbzFile, grandparent)
                    
    print("Created cbz file: " + cbzFile)

def deleteRarFile(rarFile):
    os.remove(rarFile)
    print("Deleted rar file: " + rarFile)

def deleteExtractedFolder(extractedFolder):
    shutil.rmtree(extractedFolder)
    print("Deleted extracted folder: " + extractedFolder)

def main():
    # processParentDirectory(r"C:\down\0testtttt\test\test")
    processParentDirectory(r"G:\c\down\0minipack\silver\proces2")

if __name__ == "__main__":
    main()
    # alertEndOfProcessing()