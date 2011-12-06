

class ExtremelyCommentedLine:
    
    def __init__(self):
        self.line = None
        self.extremeComments = []
        
    def setLine(self, line):
        self.line = line
        
    def addExtremeComment(self, line):
        self.extremeComments.append(line)
        
class ExtremelyCommentedLines:
    
    def __init__(self, extremeCommentLineSelector):
        self.lines = []
        self.extremeCommentLineSelector = extremeCommentLineSelector

        
    def addLines(self, lines):
        nextLine = None
        for line in lines:
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

