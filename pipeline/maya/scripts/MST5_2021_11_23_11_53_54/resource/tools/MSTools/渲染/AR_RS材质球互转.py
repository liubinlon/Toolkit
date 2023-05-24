import ConvertMat_AR_RS
reload(ConvertMat_AR_RS)
global startConvert
try:
    startConvert.close()
except:
    pass
    
startConvert = ConvertMat_AR_RS.ConvertMaterial_UI()