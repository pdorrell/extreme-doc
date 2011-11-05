from pygments import highlight
from pygments.filter import Filter
from pygments.lexers import RubyLexer
from pygments.token import Token, STANDARD_TYPES
from pygments.formatters import HtmlFormatter

import os
from urllib.request import urlopen

STANDARD_TYPES[Token.Comment.Negative] = "cn"

JSQUERY_VERSION = "1.6.4"
JSQUERY_URL = "http://ajax.googleapis.com/ajax/libs/jquery/%s/jquery.min.js" % JSQUERY_VERSION
JSQUERY_FILENAME = "jquery.min.%s.js" % JSQUERY_VERSION
JSQUERY_FILE_LOCATION = "js/%s" % JSQUERY_FILENAME

class RelabelNegativeCommentsFilter(Filter):
    def filter (self, lexer, stream):
        for ttype, value in stream:
            if ttype == Token.Comment.Single and value.startswith("#N "):
                yield Token.Comment.Negative, value[3:]
            else:
                #print(" ttype = %s, value = %r" % (ttype, value))
                yield ttype, value
                
class HtmlPageFormatter(HtmlFormatter):
    
    def __init__(self, **options):
        HtmlFormatter.__init__(self, **options)
    
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
        return "\n".join(["<link href = \"%s\" type = \"text/css\" rel = \"stylesheet\"/>" % cssFile 
                          for cssFile in self.cssFiles()])
    
    def javascriptIncludes(self):
        return "\n".join(["<script src=\"%s\" type=\"text/javascript\"></script>" % javascriptFile
                          for javascriptFile in self.javascriptFiles()])
    
    def cssFiles(self):
        return ["default.css", "extreme-doc.css"]
    
    def javascriptFiles(self):
        return [JSQUERY_FILE_LOCATION, "extreme-doc.js"]
    
    def htmlDocType(self):
        return "<!DOCTYPE html>"
    
    def htmlEnd(self):
        return "</body></html>\n"
    
    def format_unencoded(self, tokensource, outfile):
        outfile.write(self.htmlStart())
        HtmlFormatter.format_unencoded(self, tokensource, outfile)
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
    
def main(inputFileName):
    
    outputFileName = "%s.html" % inputFileName
    rubyLexer = RubyLexer()
    rubyLexer.add_filter(RelabelNegativeCommentsFilter())
    htmlPageFormatter = HtmlPageFormatter(title = inputFileName)
    
    inputFile = open(inputFileName, "r")
    code = inputFile.read()
    inputFile.close()
    
    print("pygmentizing %s into %s ..." % (inputFileName, outputFileName))
    
    outputFile = open(outputFileName, "w")
    
    highlight(code, rubyLexer, htmlPageFormatter, outfile = outputFile)
    outputFile.close()

if __name__ == "__main__":
    downloadUrlToFile (JSQUERY_URL, JSQUERY_FILE_LOCATION, clobberIfThere = False)
    inputFileName = "synqa.rb"
    main(inputFileName)
