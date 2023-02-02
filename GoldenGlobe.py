import Frame
import preprocess

list = []

preprocess.pre()

def FindAwards():
    testFrame = Frame.FrameByAward("Best Motion Picture - Drama")
    list.append(testFrame)

def FindNominees():
    list[0].addNominee("Argo")
    list[0].addNominee("Django Unchained")
    list[0].addNominee("Life of Pi")
    list[0].addNominee("Lincoln")
    list[0].addNominee("Zero Dark Thirty")

FindAwards()
FindNominees()
list[0].visualize()