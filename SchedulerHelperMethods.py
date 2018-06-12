# -*- coding: utf-8 -*-
"""
Created on Thu May 24 14:57:45 2018

@author: evin
"""
import os 
from datetime import datetime
from pydispatch import dispatcher
from EventType import EventType
import logging 
import Questionnaire
from pygame import mixer # Load the required library
import inspect
import Database
from collections import OrderedDict

scheduler = None
actionUnitConfigSection = "ACTIONUNIT"
    
def getAbsPath(fileName):
    """
    returns absolute path of a given fileName
    """
    APP_FOLDER = os.getcwd()#path.dirname(os.path.realpath(sys.argv[0]))
    filePath = os.path.join(APP_FOLDER, fileName)
    return filePath

def playSound(fileName):
    """
    plays the sound file where the relative path to the file is inputted
    """
    filePath = getAbsPath(fileName)
    mixer.init()
    mixer.music.load(filePath)
    mixer.music.play()
    logMessage("Sound file named : %s played at %s" % (filePath, str(datetime.now())))

def printMessage(actionType, message):
    """
    Calls printMessageAction method via scheduler and saves action unit details to DB
    """
    try:
        argumentsArray = [message]
        currentFunctionName = inspect.currentframe().f_code.co_name
        currentTime = datetime.now()
        scheduler.add_job(printMessageAction, args=argumentsArray)#possible to give the function moduleName:functionName
        #printMessageAction(message)
        saveActionUnitToDB(actionType, currentTime, currentFunctionName, argumentsArray)
    except Exception,e:
        print e.message

def printMessageAction(message):
    print "::::::::::::::::::::::::::::::::::"
    print "Message is ", message
    print "::::::::::::::::::::::::::::::::::"

def openQuestionnaire(actionType, masterFrame, title, questType, questionFileName):
    """
    open the questionnaire window with params 
    """
    filePath = getAbsPath(questionFileName)
    questionnaire = Questionnaire.Questionnaire(masterFrame, title, questType, filePath)
    questionnaire.run()
    logMessage("Questionnaire file named : %s opened at %s" % (questionFileName, str(datetime.now())))
        
def playSoundAndOpenQuestionnaire(actionType, soundFileName, questTitle, questType, questFileName):
    """
    Calls playSoundAndOpenQuestionnaireAction method via scheduler and saves action unit details to DB
    """
    try:
        argumentsArray = [soundFileName, questTitle, questType, questFileName]
        currentFunctionName = inspect.currentframe().f_code.co_name
        currentTime = datetime.now()
        scheduler.add_job(playSoundAndOpenQuestionnaireAction, args=argumentsArray)#possible to give the function moduleName:functionName
        saveActionUnitToDB(actionType, currentTime, currentFunctionName, argumentsArray)
    except Exception,e:
        print e.message
    
def playSoundAndOpenQuestionnaireAction(soundFileName, questTitle, questType, questFileName):
    """
    Sound is played and dispatcher send the signal to open the questionnaire
    """
    playSound(soundFileName)
    #move this line to whenever you want to open popup window
    dispatcher.send(EventType.OpenQuestSignal, EventType.OpenQuestSender, questTitle, questType, questFileName)
    logMessage("Open questionnaire  %s event sent: %s" % (questFileName, str(datetime.now())))
    
def logMessage(message):
    """
    Appends the message to the scheduler default logger
    """
    logger = logging.getLogger('apscheduler.executors.default')
    if logger:
        logger.info(message)

        
def saveActionUnitToDB(actionType, currentTime, currentFunctionName, argumentsArray):
        """
        Creates an ordereddict from the given data and saves them to DB with user information(which is included in Database module)
        """
        dataArr = []
        dataArr.append(("timeStamp", currentTime))
        dataArr.append(("function", currentFunctionName))
        dataArr.append(("actionType", actionType))
        dataArr.append(("args", argumentsArray))
        Database.saveToDB(actionUnitConfigSection, OrderedDict(dataArr))      
        
#import tkinter as Tk
#def popupWindow(frame):
#    """
#    Just for trying to open a simple popupwindow
#    """
#    counter = 1
#    t = Tk.Toplevel(frame)
#    t.wm_title("Window #%s" % counter)
#    l = Tk.Label(t, text="This is window #%s" % counter)
#    l.pack(side="top", fill="both", expand=True, padx=100, pady=100)