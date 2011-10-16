from pygments import highlight
from pygments.filter import Filter
from pygments.lexers import RubyLexer
from pygments.token import Token, STANDARD_TYPES
from pygments.formatters import HtmlFormatter


STANDARD_TYPES[Token.Comment.Negative] = "cn"

class RelabelNegativeCommentsFilter(Filter):
    def filter (self, lexer, stream):
        for ttype, value in stream:
            if ttype == Token.Comment.Single and value.startswith("#N "):
                yield Token.Comment.Negative, value[3:]
            else:
                #print(" ttype = %s, value = %r" % (ttype, value))
                yield ttype, value

def main(inputFileName):
    outputFileName = "%s.html" % inputFileName
    rubyLexer = RubyLexer()
    rubyLexer.add_filter(RelabelNegativeCommentsFilter())
    htmlFormatter = HtmlFormatter(full = True, cssfile = "default.css", noclobber_cssfile = True)
    
    inputFile = open(inputFileName, "r")
    code = inputFile.read()
    inputFile.close()
    
    print("pygmentizing %s into %s ..." % (inputFileName, outputFileName))
    
    outputFile = open(outputFileName, "w")
    
    highlight(code, rubyLexer, htmlFormatter, outfile = outputFile)
    outputFile.close()

if __name__ == "__main__":
    inputFileName = "synqa.rb"
    main(inputFileName)
