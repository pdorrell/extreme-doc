import re

class ExtremelyCommentedLine:
    
    def __init__(self):
        self.line = None
        self.extremeComments = []
        
    def setLine(self, line):
        self.line = line
        
    def addExtremeComment(self, line):
        self.extremeComments.append(line)
    
    def __str__(self):
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
                
    def __str__(self):
        return "".join([str(line) for line in self.lines])
                
def readExtremelyCommentedLines(fileName, extremeCommentLineSelector):
    inputFile = open(fileName, "r")
    extremelyCommentedLines = ExtremelyCommentedLines(extremeCommentLineSelector)
    extremelyCommentedLines.addLines(inputFile)
    inputFile.close()
    return extremelyCommentedLines

pythonExtremeCommentRegex = re.compile("^\s*#[E|D]\s.*$")

def pythonExtremeCommentsSelector(line):
    return pythonExtremeCommentRegex.match(line)

def main():
    mainSourceFileName = "ExtremeDocHighlighting.py"
    commentedSourceFileName = "ed/ExtremeDocHighlighting.py"
    
    mainSourceLines = readExtremelyCommentedLines(mainSourceFileName, pythonExtremeCommentsSelector)
    commentedSourceLines = readExtremelyCommentedLines(commentedSourceFileName, pythonExtremeCommentsSelector)
    
    print("mainSourceLines = \n%s" % mainSourceLines)
    print("commentedSourceLines = \n%s" % commentedSourceLines)
    
if __name__ == "__main__":
    main()
