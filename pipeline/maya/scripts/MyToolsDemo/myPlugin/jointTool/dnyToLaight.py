import pymel.core as pymel
import copy, os

start = pymel.playbackOptions(q = True, min = True)
end = pymel.playbaceOptions(q = True, max = True)

file_path = pm.fileDialog2(fileMode = 0, okCaption = u"export")[0]
iile_path = "%s.%s.fur" % (os.path.splitext(file_path)[0], "%04d")

pymel.pgYetiCommand(writeCache = file_path, range = (start, end),
samples = 5, updateViewport = False, generatePreview = False)
