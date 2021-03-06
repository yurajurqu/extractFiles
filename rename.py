from distutils.command.clean import clean
from operator import ne
import os
from os import listdir, rmdir
from shutil import move, copy
import stat
import this
import random  

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
                # firstname,_,surname = fn.rpartition(' ')
        newname=cleanName(fn,properties.forbidden_words)
        currentFolderName =fn
        if newname != fn:
            try:
                print("renaming from ",fn," to ",newname)
                os.rename(os.path.join(basedir, fn),os.path.join(basedir, newname))
            except FileExistsError:
                print('having a duplicate folder with same name')
                suffix = ''.join((random.choice(string.ascii_uppercase) for x in range(3)))
                newname =  newname+ "_" + suffix
                os.rename(os.path.join(basedir, fn),os.path.join(basedir, newname))
            currentFolderName = newname
    else:
        print("Nothing to do with file: ",fn)
        currentFolderName =fn
    return currentFolderName

def renameFile(basedir, fn, newname):
    #procesar directorios
    currentFolderName =fn
    if newname != fn:
        try:
            print("renaming from ",fn," to ",newname)
            os.rename(os.path.join(basedir, fn),os.path.join(basedir, newname))
        except FileExistsError:
            print('having a duplicate folder with same name')
            newname =  newname+ "_[0dup]"
            os.rename(os.path.join(basedir, fn),os.path.join(basedir, newname))
        currentFolderName = newname
    return currentFolderName
def cleanIndividualFolderPlab(dirName):
    basedir = dirName
    for fn in os.listdir(basedir):
        thisFile = os.path.join(basedir, fn)
        if not os.path.isdir(thisFile):
            print(fn)
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
            #TODO validar si es necesario renombrar
            #renameFileIfNeeded(dirName, fn)
        else:

            #remove if folder is empty
            if len(os.listdir('\\\\?\\'+thisFile)) == 0:
                print("Directory is empty ", thisFile)
                empty_folders.append(thisFile)
                continue

            currentFolderName = renameFileIfNeeded(basedir, fn)
        
            rootBase= os.path.join(basedir, currentFolderName)
            meaninglessFolder = os.path.join(rootBase, '~Get Your Files Here !')
            print(meaninglessFolder)
            if os.path.exists(meaninglessFolder):
                print('Gonna remove placeholder folder ', meaninglessFolder,' and promote content up to parent')
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
                    print('fn '+ fn)
                    if currentFolderName in fn:
                        #mark folder as placeholder folder
                        meaninglessFolder = os.path.join(rootBase, fn)
                        print('Gonna remove placeholder folder ', fpath,' and promote content up to parent')
                        for filename in listdir(meaninglessFolder):
                            origin= os.path.join(meaninglessFolder, filename)
                            destination = os.path.join(rootBase, filename)
                            print("origin: ",origin)
                            print("dest: ",destination)
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
                            os.remove('\\\\?\\'+fpath)
                        except PermissionError:
                            print('PermissionError Permission Denied to eliminate file ', fpath)
                    else:
                        print('keeping file ', fpath)
    for empty_folder in empty_folders:
        rmdir(empty_folder)



def processParentDirectory(parentDir):
    for fn in os.listdir(parentDir):
        filePath = os.path.join(parentDir, fn)
        if not os.path.isdir(filePath):
            renameFileIfNeeded(parentDir,fn)
        else:
            blacklisted_directories= ["The Project Gutenberg EBook pgdvd042010"]
            if fn in blacklisted_directories:
                print("Directory "+ filePath+" is blacklisted")
                continue
            cleanIndividualFolder(filePath)


# basedir = 'd:\\content\\tut\\ss\\productivity'
# basedir = 'd:\\content\\buch\\0fin\\'
# basedir = 'd:\\content\\buch\\'
# basedir = 'E:\\omar\\tor\\libros\\'
basedir = properties.running_directory
# basedir = 'C:\\ws\\scrapy\\nyaa_spider\\downloads\\full\\plab\\ACP\\acp\\'
# basedir = 'd:\\c\\tut\\cross\\'
# basedir="g:\\cont\\tut\\net\\"
# basedir="d:\\content\\tut\\css\\"
# basedir="E:\\omar\\tor\\tut\\"
# basedir="d:\\cont\\tut\\arch\\ts\\"
# basedir = 'g:\\content\\buch\\0raspberrypi\\'
# basedir="e:\\omar\\tor\\libros\\"
# basedir = 'E:\\omar\\tor\\tut\\arch\\'
# basedir="H:\\cont\\tut\\health\\"
# basedir="E:\\omar\\tor\\tut\\azure\\devops\\"
# basedir="E:\\omar\\tor\\tut\\office\\excel\\"
# cleanIndividualFolder(basedir)
# cleanIndividualFolderPlab(basedir)
processParentDirectory(basedir)