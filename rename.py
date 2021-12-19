import os
from os import listdir, rmdir
from shutil import move
# basedir = 'd:\\content\\tut\\ss\\productivity'
# basedir = 'd:\\content\\buch\\0fin\\'
# basedir = 'd:\\c\\tut\\cross\\'
# basedir="g:\\cont\\tut\\net\\"
basedir="d:\\cont\\tut\\forensics\\"
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
for fn in os.listdir(basedir):
    currentFolderName =''
    if not os.path.isdir(os.path.join(basedir, fn)):
        print("No directorio: ",fn)
        continue # Not a directory
    else:
        if any(word in fn for word in forbidden_words):
            print("Incorrect folder name: ",fn)
            # firstname,_,surname = fn.rpartition(' ')
            newname=rename(fn,forbidden_words)
            currentFolderName =fn
            if newname != fn:
                print("renaming from ",fn," to ",newname)
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
                move(os.path.join(meaninglessFolder, filename), os.path.join(rootBase, filename))
            rmdir(meaninglessFolder)
        for fn in os.listdir(rootBase):
            fpath = os.path.join(rootBase, fn)
            if os.path.isdir(fpath):
                if currentFolderName in fn:
                    #mark folder as placeholder folder
                    meaninglessFolder = os.path.join(rootBase, fn)
                    print('Gonna remove placeholder folder ', fpath,' and promote content up to parent')
                    for filename in listdir(meaninglessFolder):
                        move(os.path.join(meaninglessFolder, filename), os.path.join(rootBase, filename))
                    rmdir(meaninglessFolder)
            else:
                #remove garbage files
                lst = ["~uTorrentPartFile_", "Downloaded from", "TutsNode.com.txt"]
                if any(s in fn for s in lst):
                    print('removing garbage file ',fpath)
                    os.remove(fpath)