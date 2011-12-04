

class ExtremelyCommentedLine:
    
    def __init__(self):
        self.line = None
        self.extremeComments = []
        
    def setLine(self, line):
        self.line = line
        
    def addExtremeComment(self, line):
        self.extremeComments.append(line)
        
class ExtremelyCommentedLines:
    
    def __init__(self):
        self.lines = []
        self.currentLine = None
        
