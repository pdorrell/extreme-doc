from pygments import highlight
from pygments.filter import Filter
from pygments.lexers import RubyLexer
from pygments.token import Token, STANDARD_TYPES
from pygments.formatters import HtmlFormatter

import os, re
from urllib.request import urlopen
from io import StringIO

STANDARD_TYPES[Token.Comment.Negative] = "cn"
STANDARD_TYPES[Token.Comment.Extreme] = "ce"

JSQUERY_VERSION = "1.6.4"
JSQUERY_URL = "http://ajax.googleapis.com/ajax/libs/jquery/%s/jquery.min.js" % JSQUERY_VERSION
JSQUERY_FILENAME = "jquery.min.%s.js" % JSQUERY_VERSION
JSQUERY_FILE_LOCATION = "js/%s" % JSQUERY_FILENAME

class RelabelExtremeCommentsFilter(Filter):
    def filter (self, lexer, stream):
        for ttype, value in stream:
            if ttype == Token.Comment.Single:
                if value.startswith("#N "):
                    yield Token.Comment.Negative, value[3:]
                elif value.startswith ("#E "):
                    yield Token.Comment.Extreme, value[3:]
                else:
                    yield ttype, value
            else:
                #print(" ttype = %s, value = %r" % (ttype, value))
                yield ttype, value
                
class HtmlPageFormatter(HtmlFormatter):
    
    def __init__(self, **options):
        HtmlFormatter.__init__(self, **options)
        self.relativeBaseDir = options.get("relativeBaseDir", "")
    
    def htmlStart(self):
        return """%s
<html>
<head>
<title>%s</title>
%s
%s
<body>
""" % (self.htmlDocType(), self.title, self.cssIncludes(), self.javascriptIncludes())
    
    def cssIncludes(self):
        return "\n".join(["<link href = \"%s%s\" type = \"text/css\" rel = \"stylesheet\"/>" 
                          % (self.relativeBaseDir, cssFile)
                          for cssFile in self.cssFiles()])
    
    def javascriptIncludes(self):
        return "\n".join(["<script src=\"%s%s\" type=\"text/javascript\"></script>" % 
                          (self.relativeBaseDir, javascriptFile)
                          for javascriptFile in self.javascriptFiles()])
    
    def cssFiles(self):
        return ["default.css", "extreme-doc.css"]
    
    def javascriptFiles(self):
        return [JSQUERY_FILE_LOCATION, "extreme-doc.js"]
    
    def htmlDocType(self):
        return "<!DOCTYPE html>"
    
    def htmlEnd(self):
        return "</body></html>\n"

    emptyLineRegex = re.compile(r'^(\s*)$')
    cLineRegex = re.compile(r'^(\s*)(<span class="(c[ne])">(.*))$')
    lineRegex = re.compile(r'^(\s*)(<span class="(.*))$')
    
    codeLineTemplate = "<div class=\"%s\"><code>%s%s</code></div>"
    
    def taggedCodeLine(self, indentWhitespace, line, tag):
        return HtmlPageFormatter.codeLineTemplate % (tag, 
                                                     indentWhitespace.replace(" ", "&nbsp"), 
                                                     line)
    
    def divifiedSpanLine(self, spanLine):
        match = HtmlPageFormatter.cLineRegex.match(spanLine)
        if match:
            return self.taggedCodeLine(match.group(1), match.group(2), "%s-line" % match.group(3))
        else:
            match = HtmlPageFormatter.emptyLineRegex.match(spanLine)
            if match:
                return self.taggedCodeLine(match.group(1), "", "line")
            else:
                match = HtmlPageFormatter.lineRegex.match(spanLine)
                if match:
                    return self.taggedCodeLine(match.group(1), match.group(2), "line")
                else:
                    raise Exception("Unexpected pygments line: %r" % spanLine)

    firstLineRegex = re.compile(r'^(<div.*)<pre>(.*)$')
    
    lastLineRegex = re.compile(r'^(.*)</pre>(</div>)$')
    
    def writeDivifiedHtml(self, spannedHtml, outfile):
        lines = spannedHtml.split("\n")
        
        firstLine = lines[0]
        print("firstLine = %r" % firstLine)

        firstLineMatch = HtmlPageFormatter.firstLineRegex.match(firstLine)
        if firstLineMatch:
            outfile.write("%s\n" % firstLineMatch.group(1))
            outfile.write("%s\n" % self.divifiedSpanLine(firstLineMatch.group(2)))
        else:
            raise Exception("First line %r does not match expected pattern" % firstLine)
        
        for i in range(1, len(lines)-2):
            #print(" line %r" % lines[i])
            outfile.write("%s\n" % self.divifiedSpanLine(lines[i]))
            
        lastLine = lines[-2]
        print("lastLine = %r" % lastLine)
        
        lastLineMatch = HtmlPageFormatter.lastLineRegex.match(lastLine)
        if lastLineMatch:
            outfile.write("%s\n" % self.divifiedSpanLine(lastLineMatch.group(1)))
            outfile.write("%s\n" % lastLineMatch.group(2))
        else:
            raise Error("Last line %r does not match expected pattern" % lastLine)
            
        veryLastLine = lines[-1]
        if veryLastLine != '':
            raise Error("very last line %r is not empty" % veryLastLine)
        
    def format_unencoded(self, tokensource, outfile):
        outfile.write(self.htmlStart())
        stringBuffer = StringIO()
        HtmlFormatter.format_unencoded(self, tokensource, stringBuffer)
        highlightedHtml = stringBuffer.getvalue()
        self.writeDivifiedHtml(highlightedHtml, outfile)
        stringBuffer.close()
        outfile.write(self.htmlEnd())

def downloadUrlToFile(url, fileName, clobberIfThere = False):
    print("Downloading %s to %s ..." % (url, fileName))
    if clobberIfThere or not os.path.exists(fileName):
        webFile = urlopen(url)
        localFile = open(fileName, 'wb')
        localFile.write(webFile.read())
        webFile.close()
        localFile.close()
        print(" downloaded.")
    else:
        print (" not replacing existing file %s" % fileName)
    
def process(inputFileName, relativeBaseDir = ""):
    
    outputFileName = "%s.html" % inputFileName
    rubyLexer = RubyLexer()
    rubyLexer.add_filter(RelabelExtremeCommentsFilter())
    htmlPageFormatter = HtmlPageFormatter(title = inputFileName, relativeBaseDir = relativeBaseDir)
    
    inputFile = open(inputFileName, "r")
    code = inputFile.read()
    inputFile.close()
    
    print("pygmentizing %s into %s ..." % (inputFileName, outputFileName))
    
    outputFile = open(outputFileName, "w")
    
    highlight(code, rubyLexer, htmlPageFormatter, outfile = outputFile)
    outputFile.close()
    
def main():
    downloadUrlToFile (JSQUERY_URL, JSQUERY_FILE_LOCATION, clobberIfThere = False)
    #inputFileName = "synqa.rb"
    inputFileName = "ed/ExtremeDocHighlighting.py"
    process(inputFileName, "../")

if __name__ == "__main__":
    main()
    