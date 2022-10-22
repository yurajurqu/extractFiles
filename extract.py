import logging
logging.basicConfig(filename='extract.log',level=logging.DEBUG,format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S')

# extract.py

# TODO 2
# al extraer validar repetidos
# permitir escoger varias carpetas o recursivo
# iterar y borrar (no esperar al final)

import os
import zipfile
from pathlib import Path
import shutil
import glob
import properties



class ZipfileLongPaths(zipfile.ZipFile):
    def _extract_member(self, member, targetpath, pwd):
        targetpath = winapi_path(targetpath)
        return zipfile.ZipFile._extract_member(self, member, targetpath, pwd)
def rename(name,forbidden_words):
    for word in forbidden_words:
        name=name.replace(word,"")
    return name
def winapi_path(dos_path, encoding=None):
    path = os.path.abspath(dos_path)
    if path.startswith("\\\\"):
        path = "\\\\?\\UNC\\" + path[2:]
    else:
        path = "\\\\?\\" + path
    return path


def extractZipsFromCurrentDir(argDirectory):
    currentDirectory = ''
    if argDirectory:
        currentDirectory = argDirectory
    currentDirectory= properties.running_directory
    garbage_files= properties.garbage_files_zip

    zipsToRemove=[]
    os.chdir(currentDirectory)
    print(currentDirectory)
    logging.info("CurrentDirectory: "+currentDirectory)
    files = [f for f in os.listdir(currentDirectory) if os.path.isfile(os.path.join(currentDirectory,f))]
    logging.info("files")
    logging.info(files)
    for currentFile in files:
        print(currentFile)
        logging.info(currentFile)
        if currentFile.endswith(".zip"):
            print('processing')
            logging.info('processing file '+currentFile )
            foundCourseContent=False
            with ZipfileLongPaths(os.path.join(currentDirectory,currentFile)) as zip:
                for zip_info in zip.infolist():
                    print(zip_info.filename)
                    logging.info(zip_info.filename)
                    if "~Get Your Course Here !" in  zip_info.filename:
                        if not foundCourseContent:
                            foundCourseContent=True
                        zip_info.filename=zip_info.filename.replace("/~Get Your Course Here !","")
                        zip_info.filename=rename(zip_info.filename,properties.forbidden_words)
                        logging.info('extracting zip '+ zip_info.filename)
                        zip.extract(zip_info)
                            # print(zip_info.filename)
                    else:
                    # elif currentFile[:-3] in  zip_info.filename:


                        if not foundCourseContent:
                            foundCourseContent=True

                        zip_info.filename=rename(zip_info.filename,properties.forbidden_words)
                        zip.extract(zip_info)
                        # zip_info.filename=zip_info.filename.replace("/~Get Your Course Here !","")
                        # print(zip_info.filename)

            if foundCourseContent:
                zipsToRemove.append(os.path.join(currentDirectory,currentFile))
                # print('Eliminating '+currentDirectory+currentFile)
                # os.remove(currentDirectory+currentFile)
        else:
            print(currentFile + 'not zip')
            logging.info(currentFile + 'is not zip ')
    for file in zipsToRemove:
        os.remove(file)

if __name__ == "__main__":
    extractZipsFromCurrentDir(None)