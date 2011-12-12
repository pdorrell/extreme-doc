import re
import difflib

class ExtremelyCommentedLine:
    
    def __init__(self):
        self.line = None
        self.extremeComments = []
        
    def setLine(self, line):
        self.line = line
        
    def addExtremeComment(self, line):
        self.extremeComments.append(line)
    
    def __str__(self):
        return "%s%s" % ("".join(["%s\n" % comment for comment in self.extremeComments]), 
                           self.line)
    
    def __repr__(self):
        return "%sLINE: %s\n\n" % ("".join([" COMMENT: %s\n" % comment for comment in self.extremeComments]), 
                             self.line)
        
class ExtremelyCommentedLines:
    
    def __init__(self, extremeCommentLineSelector):
        self.lines = []
        self.extremeCommentLineSelector = extremeCommentLineSelector

        
    def addLines(self, lines):
        nextLine = None
        for line in lines:
            if line.endswith("\n"):
                line = line[:-1]
            if nextLine == None:
                nextLine = ExtremelyCommentedLine()
                self.lines.append(nextLine)
            if self.extremeCommentLineSelector(line):
                nextLine.addExtremeComment(line)
            else:
                nextLine.setLine(line)
                nextLine = None
        if nextLine != None:
            if nextLine.line == None:
                nextLine.setLine("")
                
    def getUncommentedLines(self):
        return [line.line for line in self.lines]
                
    def __str__(self):
        return "".join([str(line) for line in self.lines])
    
    def mergeForwardTo(self, newSourceLines):
        print("mergeForwardTo ...")
        oldUncommentedLines = self.getUncommentedLines()
        newUncommentedLines = newSourceLines.getUncommentedLines()
        matcher = difflib.SequenceMatcher(None, oldUncommentedLines, newUncommentedLines)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            #print("tag: %s" % tag)
            #print(" %s-%s, %s-%s" % (i1, i2, j1, j2))
            print ("####################################################################")
            if tag == "equal":
                print ("##EQUAL")
                for i in range(i1, i2):
                    oldLine = self.lines[i]
                    newSourceLine = newSourceLines.lines[i + (j1-i1)]
                    for comment in oldLine.extremeComments:
                        print("%s" % comment)
                    if len(newSourceLine.extremeComments) > 0:
                        print("#>>>")
                        for comment in newSourceLine.extremeComments:
                            print("%s" % comment)
                    print(newSourceLine.line)
            elif tag == "delete":
                print ("##DELETE")
                for i in range(i1, i2):
                    print ("%s" % self.lines[i])
            elif tag == "insert":
                print ("##INSERT")
                for i in range(j1, j2):
                    print ("%s" % newSourceLines.lines[i])
            elif tag == "replace":
                print ("##REPLACE")
                for i in range(i1, i2):
                    print ("%s" % self.lines[i])
                print ("#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                for i in range(j1, j2):
                    print ("%s" % newSourceLines.lines[i])
                
def readExtremelyCommentedLines(fileName, extremeCommentLineSelector):
    inputFile = open(fileName, "r")
    extremelyCommentedLines = ExtremelyCommentedLines(extremeCommentLineSelector)
    extremelyCommentedLines.addLines(inputFile)
    inputFile.close()
    return extremelyCommentedLines

pythonExtremeCommentRegex = re.compile("^\s*#[EN]\s.*$")

def pythonExtremeCommentsSelector(line):
    return pythonExtremeCommentRegex.match(line)

def main():
    mainSourceFileName = "ExtremeDocHighlighting.py"
    commentedSourceFileName = "ed/ExtremeDocHighlighting.py"
    
    mainSourceLines = readExtremelyCommentedLines(mainSourceFileName, pythonExtremeCommentsSelector)
    commentedSourceLines = readExtremelyCommentedLines(commentedSourceFileName, pythonExtremeCommentsSelector)
    
    #print("mainSourceLines = \n%s" % mainSourceLines)
    #print("commentedSourceLines = \n%s" % commentedSourceLines)
    
    commentedSourceLines.mergeForwardTo(mainSourceLines)
    
if __name__ == "__main__":
    main()
