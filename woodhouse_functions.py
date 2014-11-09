from PySide import QtGui, QtCore
import woodhouse
import sys, os, time
import configparser

rulefile = os.path.join(os.environ['HOME']+'/.woodhouse/rules.conf')

def saverules(folder, rulename, time, timescale, subfolders):
    #config.filename = 'rules.conf'
    config = configparser.ConfigParser()
    section = str(folder + '::' + rulename)
    config[section] = {}
    config[section]['Time'] = time
    config[section]['Timescale'] = timescale
    config[section]['Subfolder'] = str(subfolders)
    config[section]['activated'] = 'False'

    with open(rulefile,'a') as config_file:
        config.write(config_file)
    # saves the rule to a file and sends an ok
    return 'OK'


def deleterules(folder, rulename):
    if not os.path.exists(rulefile):
        return 'No config found!'
    config = configparser.ConfigParser()
    config.read('~/.woodhouse/rules.conf')
    section = str(folder + '::' + rulename)
    config.remove_section(section)

    with open(rulefile, 'w') as config_file:
        config.write(config_file)
    return 'OK'

def toggleactivateRule(folder, rulename):
    config = configparser.ConfigParser()
    config.read(rulefile)
    section = section = str(folder + '::' + rulename)
    if config[section]['activated'] == 'False':
        config[section]['activated'] = 'True'
    else:
        config[section]['activated'] = 'False'
    with open(rulefile, 'w') as config_file:
        config.write(config_file)
    return 'OK'

def getRules(folder):
    #returns a list of rulenames corresponding to the folder
    listofrules = []
    if not os.path.exists(rulefile):
        return None
    config = configparser.ConfigParser()
    config.read(rulefile)
    sections = config.sections()
    for sec in sections:
        if folder in sec:
            name = sec.split('::')
            listofrules.append(name[1])
    return listofrules

def getFolders():
    #return a list of foldernames
    listoffolders = []
    if not os.path.exists(rulefile):
        return listoffolders
    config = configparser.ConfigParser()
    config.read(rulefile)
    sections = config.sections()
    for sec in sections:
        folder = sec.split('::')
        #remove duplicates
        for item in folder:
            if folder.index(item) %2 == 0:
                listoffolders.append(item)
    listoffolders = list(set(listoffolders))
    return listoffolders


def showruletime(folder, name):
    config = configparser.ConfigParser()
    config.read(rulefile)
    section = str(folder + '::' + name)
    return config[section]['Time']

def showruletimescale(folder, name):
    config = configparser.ConfigParser()
    config.read(rulefile)
    section = str(folder + '::' + name)
    return config[section]['Timescale']

def showrulesubfolder(folder, name):
    config = configparser.ConfigParser()
    config.read(rulefile)
    section = str(folder + '::' + name)
    return config[section]['Subfolder']

def showruleactive(folder, name):
    config = configparser.ConfigParser()
    config.read(rulefile)
    section = str(folder + '::' + name)
    return config[section]['activated']

def testrules(folder):
    systemtime = time.time()
    config = configparser.ConfigParser()
    config.read(rulefile)
    for s in config.sections():
        if folder in s:
            nameandfolder = s.split('::')
            folder = nameandfolder[0]
            bestbeforetime = float(config[s]['time'])
            bestbeforescale = config[s]['timescale']
            #converting the time scale to seconds and multiply them time
            if bestbeforescale == 'days':
                #a day has 86400 seconds
                bestbeforedelta = bestbeforetime * 86400
            elif bestbeforescale == 'months':
                #a month has 2628000 seconds
                bestbeforedelta = bestbeforetime * 2628000
            elif bestbeforescale == 'years':
                #a year has 31536000 seconds
                bestbeforedelta = bestbeforetime * 31536000
            if config[s]['Subfolder'] == 'False':
                onlyfiles = []
                for files in os.listdir(folder):
                    if os.path.isfile(os.path.join(folder, files)) == True:
                        fullpath = os.path.join(folder, files)
                        lastmodified = os.path.getmtime(fullpath)
                        bestbefore = lastmodified + bestbeforedelta
                        if bestbefore <= systemtime:
                            onlyfiles.append(fullpath)
                return onlyfiles
            else:
                filesandfolders = []
                for root, dirs ,files in os.walk(folder):
                    for name in files:
                        fullpath = os.path.join(root, name)
                        lastmodified = os.path.getmtime(fullpath)
                        bestbefore = lastmodified + bestbeforedelta
                        if bestbefore <= systemtime:
                            filesandfolders.append(fullpath)
                    for name in dirs:
                        fullpath = os.path.join(root, name)
                        lastmodified = os.path.getmtime(fullpath)
                        bestbefore = lastmodified + bestbeforedelta
                        if bestbefore <= systemtime:
                            filesandfolders.append(fullpath)
                return filesandfolders



def clean(test=True):
    if not os.path.exists(rulefile):
        pass
    else:
        #seconds since the last epoch
        systemtime = time.time()
        config = configparser.ConfigParser()
        config.read(rulefile)
        sections = config.sections()
        todelete = []
        if test == False:
            for s in sections:
                if config[s]['activated'] == "True":
                    nameandfolder = s.split('::')
                    name = nameandfolder[1]
                    folder = nameandfolder[0]
                    bestbeforetime = float(config[s]['time'])
                    bestbeforescale = config[s]['timescale']

                    #converting the time scale to seconds and multiply them time
                    if bestbeforescale == 'days':
                        #a day has 86400 seconds
                        bestbeforedelta = bestbeforetime * 86400
                    elif bestbeforescale == 'months':
                        #a month has 2628000 seconds
                        bestbeforedelta = bestbeforetime * 2628000
                    elif bestbeforescale == 'years':
                        #a year has 31536000 seconds
                        bestbeforedelta = bestbeforetime * 31536000

                    if config[s]['Subfolder'] == 'False':
                        for files in os.listdir(folder):
                            if os.path.isfile(os.path.join(folder, files)) == True:
                                fullpath = os.path.join(folder, files)
                                lastmodified = os.path.getmtime(fullpath)
                                bestbefore = lastmodified + bestbeforedelta
                                if bestbefore <= systemtime:
                                    os.remove(fullpath)
                    else:
                        for root, dirs ,files in os.walk(folder, topdown = False):
                            for name in files:
                                fullpath = os.path.join(root, name)
                                lastmodified = os.path.getmtime(fullpath)
                                bestbefore = lastmodified + bestbeforedelta
                                if bestbefore <= systemtime:
                                    with open('wooghouse.log', 'a') as log:
                                        log.write("[" + str(time.strftime("%x"
                                                                         + " "
                                                                         + "%X"))
                                        + "]: Deleting" + str(fullpath) + "\n")
                                    os.remove(fullpath)
                            for name in dirs:
                                fullpath = os.path.join(root, name)
                                lastmodified = os.path.getmtime(fullpath)
                                bestbefore = lastmodified + bestbeforedelta
                                if bestbefore <= systemtime:
                                    with open('woodhouse.log', 'a') as log:
                                        log.write("[" + str(time.strftime("%x"
                                                                         + " "
                                                                         + "%X"))
                                        + "]: Deleting" + str(fullpath) + "\n"
                                                  )
                                    os.rmdir(fullpath)



def main():
    app = QtGui.QApplication(sys.argv)
    woodhouse = woodhousegui.MainWindow()
    app.exec_()
    sys.exit()



if __name__ == '__main__':
    main()
