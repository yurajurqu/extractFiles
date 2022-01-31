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

currentDirectory= properties.running_directory
garbage_files= properties.garbage_files_zip


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

zipsToRemove=[]
os.chdir(currentDirectory)
print(currentDirectory)
files = [f for f in os.listdir(currentDirectory) if os.path.isfile(currentDirectory+f)]
for currentFile in files:
    print(currentFile)
    if currentFile.endswith(".zip"):
        print('processing')
        foundCourseContent=False
        with ZipfileLongPaths(currentDirectory+currentFile) as zip:
            for zip_info in zip.infolist():
                print(zip_info.filename)
                if "~Get Your Course Here !" in  zip_info.filename:
                    if not foundCourseContent:
                        foundCourseContent=True
                    zip_info.filename=zip_info.filename.replace("/~Get Your Course Here !","")
                    zip_info.filename=rename(zip_info.filename,properties.forbidden_words)

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
            zipsToRemove.append(currentDirectory+currentFile)
            # print('Eliminating '+currentDirectory+currentFile)
            # os.remove(currentDirectory+currentFile)
    else:
        print('not zip')
for file in zipsToRemove:
    os.remove(file)

# archive = ZipfileLongPaths(currentDirectory+singleFile+".zip")


# for file in archive.namelist():
#     if file.startswith(singleFile+"/~Get Your Course Here !/"):
#         print(file)
#         archive.extract(file)


# filename=currentDirectory+singleFile
# with zipfile.ZipFile(filename,"r") as zip_ref:
#     zip_ref.extractall(currentDirectory)
#     baseName=Path(filename).stem
#     os.chdir(currentDirectory+baseName)
#     for removeFile in filesToRemove:
#         if os.path.exists(currentDirectory+baseName+"\\"+removeFile):
#             os.remove(currentDirectory+baseName+"\\"+removeFile)
#         else:
#             print("Can not delete the file as it doesn't exists: "+removeFile)
#     print(currentDirectory+baseName+"\\"+contentPath+"\\"+"*")
#     os.chdir(currentDirectory+baseName+"\\"+contentPath)
#     files = glob.glob(".\*")
#     # print(files)
#     for f in files:
#         shutil.move(f, currentDirectory+baseName)
#     os.chdir("..")
#     filesToRemove=["Resources.url","Passwords - only if needed when extracting.txt","How to Support [ FreeCourseWeb.com ] for Free.txt","Bonus Courses + Project Files.url"]
#     directoriesToRemove=["~Get Your Course Here !"]

#     for removeFile in filesToRemove:
#         if os.path.exists(removeFile):
#             os.remove(removeFile)
#         else:
#             print("Can not delete the file as it doesn't exists: "+removeFile)
#     for dirToRemoe in directoriesToRemove:
#         if os.path.exists(dirToRemoe):
#             os.rmdir(dirToRemoe)
#         else:
#             print("Can not delete the directory as it doesn't exists: "+dirToRemoe)
#     os.chdir("..")
# # os.remove(filename)
