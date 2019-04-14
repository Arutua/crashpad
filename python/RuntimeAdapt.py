import sys
import os

# Get & Dipslay the parameters
folder = sys.argv[1]
mode = sys.argv[2]
runTime = sys.argv[3]

print "Folder : " , str(folder)
print "Mode : " , str(mode)
print "RunTime : " , str(runTime)

path = os.path.realpath('.')
print "Current Folder : " , str(path)

parent = os.path.abspath(os.path.join(path, '..'))
print "Parent Folder : " , str(parent)

workfolder = parent + "\out\\" + folder
print workfolder

# Check if path exist
isDir = os.path.isdir(workfolder)
print isDir

if not isDir:
    print "Error destination os not a folder"
    exit(1)

# check parameters
if (mode != "Release") and (mode != "Debug"):
    print "Error mode must be Relase or Debug"
    exit(1)

if (runTime != "DLL") and (runTime != "NoDLL"):
    print "Error mode must be DLL or NoDLL"
    exit(1)

if  (runTime == "DLL") and (mode == "Release"):
    toAdd = [" /MD", " /O2" ]
    toRemove = [" /MT", " /MTd", " /Mdd", " /Od"]

if  (runTime == "DLL") and (mode == "Debug"):
    toAdd = [" /MDd", " /Od" ]
    toRemove = [" /MT", " /MTd", " /Md", " /O2"]

if  (runTime == "NoDLL") and (mode == "Release"):
    toAdd = [" /MT", " /O2" ]
    toRemove = [" /MD", " /MTd", " /Mdd", " /Od"]

if  (runTime == "NoDLL") and (mode == "Debug"):
    toAdd = [" /MTd", " /Od" ]
    toRemove = [" /MT", " /MDd", " /Md", " /O2"]    

# get list of all files
listFiles = [val for sublist in [[os.path.join(i[0], j) for j in i[2]if j.endswith('.ninja')] for i in os.walk(workfolder)] for val in sublist]
#print listFiles

for ninjaFile in listFiles: 
    f = open(ninjaFile, "r+")
    fileOut = open(ninjaFile+"1", "w+")
    for line in f:
        if "cflag" in line:
            print "found in " + ninjaFile 
            print "before :" + line
            for option in toRemove:
                if option in line:
                    print "removing :" + option
                    line = line.replace(option,'')
            for option in toAdd:
                if option not in line:
                    print "adding :" + option
                    line = line.rstrip() + option
            print "after :" + line
            fileOut.write(line)
            break
        fileOut.write(line)
    f.close()
    fileOut.close()

for ninjaFile in listFiles: 
    os.remove(ninjaFile)

for ninjaFile in listFiles: 
    os.rename(ninjaFile+"1", ninjaFile)
