# encoding=utf8
from cmath import log
from distutils.command.clean import clean
from operator import ne
import os
from os import listdir, rmdir
from shutil import move, copy
import stat
import this
import random  
import logging
import errno
import sys  
from errno import EACCES, EPERM, ENOENT
reload(sys)  

sys.setdefaultencoding('utf8')

logging.basicConfig(filename='rename.log',level=logging.DEBUG,format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S')

import properties
import string  
# "[FreeCourseLab.com] ","[DesireCourse.Com] ","[FreeCoursesOnline.Me] [LINKEDIN LEARNING] ","[FreeTutorials.Eu] [UDEMY] ","[pluralsight.com] "
def cleanName(name,forbidden_words):
    for word in forbidden_words:
        name=name.replace(word,"")
    return name

def renameFileIfNeeded(basedir, fn):
    #procesar directorios
    if any(word in fn for word in properties.forbidden_words):
        print("Incorrect file name: ",fn)
        logging.info("Incorrect file name: "+fn)
                # firstname,_,surname = fn.rpartition(' ')
        newname=cleanName(fn,properties.forbidden_words)
        currentFolderName =fn
        if newname != fn:
            try:
                print("renaming from ",fn," to ",newname)
                logging.info("renaming from " + fn + " to " +newname)
                os.rename(os.path.join(basedir, fn),os.path.join(basedir, newname))
            except OSError as e:
                if e.errno == errno.EEXIST:
                    print('having a duplicate folder with same name')
                    logging.error('having a duplicate folder with same name')
                    suffix = ''.join((random.choice(string.ascii_uppercase) for x in range(3)))
                    newname =  newname+ "_" + suffix
                    os.rename(os.path.join(basedir, fn),os.path.join(basedir, newname))
                else:
                    raise
                
            currentFolderName = newname
    else:
        print("Filename is correct: ",fn)
        logging.info("Filename is correct: " + fn)
        currentFolderName =fn
    return currentFolderName

def renameFile(basedir, fn, newname):
    #procesar directorios
    currentFolderName =fn
    if newname != fn:
        try:
            print("renaming from ",fn," to ",newname)
            logging.info("renaming from " + fn + " to " + newname)
            os.rename(os.path.join(basedir, fn),os.path.join(basedir, newname))
        except OSError as e:
            if e.errno == errno.EEXIST:
                print('having a duplicate folder with same name')
                logging.error('having a duplicate folder with same name')
                newname =  newname+ "_[0dup]"
                os.rename(os.path.join(basedir, fn),os.path.join(basedir, newname))
            else:
                raise
        currentFolderName = newname
    return currentFolderName
def cleanIndividualFolderPlab(dirName):
    basedir = dirName
    for fn in os.listdir(basedir):
        thisFile = os.path.join(basedir, fn)
        if not os.path.isdir(thisFile):
            print(fn)
            logging.info("Iterating Filename "+ fn )
            renameFile(basedir, fn, fn.replace("plab","plab_ACP"))
 
def cleanIndividualFolder(dirName):
    basedir = dirName
    empty_folders = []    
    for fn in os.listdir(basedir):
        currentFolderName =''
        thisFile = os.path.join(basedir, fn)
        if not os.path.isdir(thisFile):
            #caso archivos
            print("No directorio: ",fn)
            logging.info("No directorio: " + fn)
            #TODO validar si es necesario renombrar
            renameFileIfNeeded(dirName, fn)
        else:

            #remove if folder is empty
            if len(os.listdir('\\\\?\\'+thisFile)) == 0:
                print("Directory is empty ", thisFile)
                logging.info("Directory is empty " + thisFile)
                empty_folders.append(thisFile)
                continue

            currentFolderName = renameFileIfNeeded(basedir, fn)
        
            rootBase= os.path.join(basedir, currentFolderName)
            meaninglessFolder = os.path.join(rootBase, '~Get Your Files Here !')
            print(meaninglessFolder)
            if os.path.exists(meaninglessFolder):
                print('Gonna remove placeholder folder ', meaninglessFolder,' and promote content up to parent')
                logging.info('Gonna remove placeholder folder '+ meaninglessFolder +' and promote content up to parent')
                for filename in listdir('\\\\?\\'+meaninglessFolder):
                    src= os.path.join(meaninglessFolder, filename)
                    dest = os.path.join(rootBase, filename)
                    os.chmod('\\\\?\\'+src, stat.S_IWRITE)
                    if os.path.exists('\\\\?\\'+dest):
                        os.chmod('\\\\?\\'+dest, stat.S_IWRITE)
                    move('\\\\?\\'+src, '\\\\?\\'+dest)
                rmdir(meaninglessFolder)

            #remove meaningless folder and promote content to parent folder    
            for fn in os.listdir(rootBase):
                fpath = os.path.join(rootBase, fn)
                if os.path.isdir(fpath):
                    print('currentFolderName '+ currentFolderName)
                    logging.info('currentFolderName '+ currentFolderName)
                    print('fn '+ fn)
                    logging.info('fn '+ fn)
                    if currentFolderName in fn:
                        #mark folder as placeholder folder
                        meaninglessFolder = os.path.join(rootBase, fn)
                        print('Gonna remove placeholder folder ', fpath,' and promote content up to parent')
                        logging.info('Gonna remove placeholder folder '+ fpath + ' and promote content up to parent')
                        for filename in listdir(meaninglessFolder):
                            origin= os.path.join(meaninglessFolder, filename)
                            destination = os.path.join(rootBase, filename)
                            print("origin: ",origin)
                            logging.info("origin: " + origin)
                            print("dest: ",destination)
                            logging.info("dest: " + destination)
                            try:
                                os.chmod('\\\\?\\'+origin, stat.S_IWRITE)
                                if os.path.exists('\\\\?\\'+destination):
                                    os.chmod('\\\\?\\'+destination, stat.S_IWRITE)
                                move('\\\\?\\'+origin,'\\\\?\\'+destination)
                            except:
                                copy('\\\\?\\'+origin, '\\\\?\\'+destination )
                        rmdir(meaninglessFolder)
            #remove garbage files
            for fn in os.listdir(rootBase):
                fpath = os.path.join(rootBase, fn)
                if not os.path.isdir(fpath):
                    #remove garbage files
                    lst = properties.garbage_simple_files
                    if any(s in fn for s in lst):
                        try:
                            print('removing garbage file ',fpath)
                            logging.info('removing garbage file ' + fpath)
                            os.remove('\\\\?\\'+fpath)
                        except (IOError, OSError) as e:
                            if e.errno==EPERM or e.errno==EACCES:
                                print('PermissionError Permission Denied to eliminate file ', fpath)
                                logging.info('PermissionError Permission Denied to eliminate file ' + fpath)
                            else:
                                raise
                    else:
                        print('keeping file ', fpath)
                        logging.info('keeping file ' + fpath)
    for empty_folder in empty_folders:
        rmdir(empty_folder)



def processParentDirectory(parentDir):
    for fn in os.listdir(parentDir):
        filePath = os.path.join(parentDir, fn)
        logging.info("Processing subfile "+ fn)
        if not os.path.isdir(filePath):
            renameFileIfNeeded(parentDir,fn)
        else:
            blacklisted_directories= ["The Project Gutenberg EBook pgdvd042010"]
            if fn in blacklisted_directories:
                print("Directory "+ filePath+" is blacklisted")
                logging.info("Directory "+ filePath+" is blacklisted")
                continue
            logging.info("Processing sub directory "+ directory)
            cleanIndividualFolder(filePath)

directories = [
    'E:\\omar\\tor\\libros\\',
    'E:\\omar\\tor\\libros\\0js\\',
    'E:\\omar\\tor\\libros\\0google\\',

    'd:\\content\\tut\\ss\\productivity',
	'd:\\content\\tut\\js\\',
    'd:\\content\\buch\\0fin\\',
    'd:\\content\\buch\\',
	
	'd:\\cont\\tut\\js\\',

    "E:\\omar\\tor\\tut\\",
    "E:\\omar\\tor\\tut\\arch\\",
    "E:\\omar\\tor\\tut\\google\\",
    "E:\\omar\\tor\\tut\\ai\\",
    "E:\\omar\\tor\\tut\\tools\\",
    "E:\\omar\\tor\\tut\\tools\\linkedin\\",
    "E:\\omar\\tor\\tut\\tools\\teams\\",
    "E:\\omar\\tor\\tut\\write\\",
    "E:\\omar\\tor\\tut\\blockchain\\",
    "E:\\omar\\tor\\tut\\ss\\",
    "E:\\omar\\tor\\tut\\sec\\",
    "E:\\omar\\tor\\tut\\read\\",
    "E:\\omar\\tor\\tut\\design\\",
    "E:\\omar\\tor\\tut\\manage\\",
    "E:\\omar\\tor\\tut\\js\\",
	"E:\\omar\\tor\\tut\\fin\\",
    "E:\\omar\\tor\\tut\\azure\\",
    "E:\\omar\\tor\\tut\\office\\excel\\",
    "E:\\omar\\tor\\tut\\music\\",
    "E:\\omar\\tor\\tut\\music\\piano\\",


    "E:\\omar\\tor\\lang\\",
    "E:\\omar\\tor\\draw\\",
	
	'd:\\cont\\tut\\',
	'd:\\cont\\tut\\js\\',

 
]

for directory in directories:
    if(os.path.exists(directory)):
        logging.info("Processing directory "+ directory)
        processParentDirectory(directory)
    else:
        logging.info('Directory '+directory +" does not exist")