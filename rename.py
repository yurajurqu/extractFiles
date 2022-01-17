from distutils.command.clean import clean
from operator import ne
import os
from os import listdir, rmdir
from shutil import move, copy
# basedir = 'd:\\content\\tut\\ss\\productivity'
# basedir = 'd:\\content\\buch\\0fin\\'
# basedir = 'd:\\c\\tut\\cross\\'
# basedir="g:\\cont\\tut\\net\\"
# basedir="d:\\content\\tut\\css\\"
basedir="E:\\omar\\tor\\tut\\"
# basedir="d:\\cont\\tut\\arch\\ts\\"
# basedir = 'g:\\content\\buch\\0raspberrypi\\'
# basedir="e:\\omar\\tor\\libros\\"
# basedir = 'E:\\omar\\tor\\tut\\arch\\'
# basedir="H:\\cont\\tut\\health\\"
# basedir="E:\\omar\\tor\\tut\\azure\\devops\\"
# basedir="E:\\omar\\tor\\tut\\office\\excel\\"

forbidden_words=["[ FreeCourseWeb.com ] ","[ DevCourseWeb.com ] ", "[DesireCourse.Net] ","[FreeCoursesOnline.Me] ","[TechnicsPub] ","[UDACITY] ","[LYNDA] ",
"[GigaCourse.com] ","[CourseClub.NET] ", "[FreeTutorials.Us] ","[Tutorialsplanet.NET] ","[DesireCourse.Com] ","[CourseClub.Me] ", "[FreeTutorials.us] ",
"[FreeAllCourse.Com] ","[ FreeCourseWeb ]","[FreeCourseSite.com] ","[FreeCourseLab.com] ","[Code4startup.Com] ","[PaidCoursesForFree.com] - ","[Tutorialsplanet.NET] ","[Tutorialguide.co] ","[Packtpub.Com] ","[OREILLY] "
,"[FTUForum.com] ","[Apress] ","[FrontendMasters] ","Udemy - ","[Pluralsight] ","[FreeTutorials.Eu] ","[Frontend Masters] - ","[LINKEDIN LEARNING] ",
"[pluralsight-training.net] ","[LinkedIn] ","(Video2Brain) ","[FreeCourseWeb] ","[Packt] ","[Skillshare] ","[UDEMY] ","[NulledPremium.com] ","[NulledPremium] "
,"[FTUForum.com] ","[FreeTutorials.Us] ","[FreeCourseWorld.Com] ","[AhLaNedu.com] ","[ CourseWikia.com ] ","[ CourseBoat.com ] ","[ CourseHulu.com ] "
,"[pluralsight.com] ","[ TutSala.com ] ","[ TutGator.com ] ","[ CourseLala.com ] ","[ CourseMega.com ] ","[ CoursePig.com ] ","[GigaCourse.Com] ","[ TutPig.com ] ","[ TutGee.com ] ","[Skillshare - Original] "
]
# "[FreeCourseLab.com] ","[DesireCourse.Com] ","[FreeCoursesOnline.Me] [LINKEDIN LEARNING] ","[FreeTutorials.Eu] [UDEMY] ","[pluralsight.com] "
def rename(name,forbidden_words):
    for word in forbidden_words:
        name=name.replace(word,"")
    return name

def cleanIndividualFolder(dirName):
    basedir = dirName    
    for fn in os.listdir(basedir):
        currentFolderName =''
        if not os.path.isdir(os.path.join(basedir, fn)):
            #caso archivos
            print("No directorio: ",fn)
            continue # Not a directory
        else:
            #procesar directorios
            if any(word in fn for word in forbidden_words):
                print("Incorrect folder name: ",fn)
                # firstname,_,surname = fn.rpartition(' ')
                newname=rename(fn,forbidden_words)
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
            else:
                print("Nothing to do with file: ",fn)
                currentFolderName =fn
        
            rootBase= os.path.join(basedir, currentFolderName)
            meaninglessFolder = os.path.join(rootBase, '~Get Your Files Here !')
            print(meaninglessFolder)
            if os.path.exists(meaninglessFolder):
                print('Gonna remove placeholder folder ', meaninglessFolder,' and promote content up to parent')
                for filename in listdir(meaninglessFolder):
                    src= os.path.join(meaninglessFolder, filename)
                    dest = os.path.join(rootBase, filename)
                    move(src, dest)
                rmdir(meaninglessFolder)

            #remove meaningless folder and promote content to parent folder    
            for fn in os.listdir(rootBase):
                fpath = os.path.join(rootBase, fn)
                if os.path.isdir(fpath):
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
                                move('\\\\?\\'+origin,'\\\\?\\'+destination)
                            except:
                                copy('\\\\?\\'+origin, '\\\\?\\'+destination )
                        rmdir(meaninglessFolder)
            #remove garbage files
            for fn in os.listdir(rootBase):
                fpath = os.path.join(rootBase, fn)
                if not os.path.isdir(fpath):
                    #remove garbage files
                    lst = ["~uTorrentPartFile_", "Downloaded from", "TutsNode.com.txt","BookRAR.Org","more books, audiobooks, magazines etc.",
                    "free audiobook version","Bonus Resources","Please Consider Making A Donation","How to Support [ FreeCourseWeb.com ] for Free","Please Support Us","Please Support [ FreeCourseWeb.com ] by Visitng Ads"]
                    if any(s in fn for s in lst):
                        try:
                        print('removing garbage file ',fpath)
                        os.remove(fpath)
                        except PermissionError:
                            print('PermissionError Permission Denied to eliminate file ', fpath)
                    else:
                        print('keeping file ', fpath)


def processParentDirectory(parentDir):
    for fn in os.listdir(parentDir):
        filePath = os.path.join(parentDir, fn)
        if not os.path.isdir(filePath):
            continue
        else:
            cleanIndividualFolder(filePath)



#cleanIndividualFolder(basedir)
processParentDirectory(basedir)