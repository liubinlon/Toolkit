import ZCheck_JBY
global startZCheck
try:
    startZCheck.close()
except:
    pass
startZCheck = ZCheck_JBY.CheckTheScene_UI()