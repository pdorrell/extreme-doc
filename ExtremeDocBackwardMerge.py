import re

extremeOrNegativeCommentRegex = re.compile(r'^\s*#[E|N] ')

def isExtremeOrNegativeComment(line):
    return extremeOrNegativeCommentRegex.match(line)

def copyFileFiltered(inputFileName, outputFileName, linesToRemoveFilter):
    print("Copying filtered lines from %r to %r ..." % (inputFileName, outputFileName))
    with open(inputFileName, 'r') as inputFile:
        with open(outputFileName, 'w') as outputFile:
            for line in inputFile:
                if not linesToRemoveFilter(line):
                    print("line = %r" % line)
                    outputFile.write(line)

def main():
    inputFileName = "ed/ExtremeDocHighlighting.py"
    outputFileName = "ExtremeDocHighlighting.py"
    copyFileFiltered(inputFileName, outputFileName, isExtremeOrNegativeComment)

if __name__ == "__main__":
    main()
