
class file_model:
    rootDir = ""
    sourceFileName = ""
    content = ""
    finalComment = "[finalComment]"


    def __init__(self):
        self.rootDir = ""
        self.sourceFileName = ""
        self.content = ""

    def readFile(self, fileName):
        if fileName == "":
            return
        self.extractFileNameAndRoot(fileName)
        fileHandler = file
        try:
            fileHandler = open(self.rootDir + self.sourceFileName)
            self.content = fileHandler.read()
            fileHandler.close()
        except (OSError, IOError) as e:
            fileHandler.close()
            raise IOError(e.errno + e.errmessage)

    def toString(self):
        """
        Returns the content of Object as String.
        :returns: Content of the Object as String
        :rtype: str
        """
        return self.content

    def extractFileNameAndRoot(self, fileName):
        if fileName == "":
            print "getRootPath: FileName was empty!"
            return
        fileName.replace("\\", "/")
        self.sourceFileName = fileName[fileName.rfind('/'):]
        self.rootDir = fileName[:fileName.rfind('/') + 1]

    def removeComments(self, singleLineComment = "", multiLineCommentStart = "" , multiLineCommentEnd = ""):
        """
        Removes all the comments from a file.
        :param singleLineComment: Tag for single line comment
        :param multiLineCommentStart: Start tag for a multi line comment
        :param multiLineCommentEnd: End tag for a multi line comment
        :return: void
        """
        lines = self.getContentInLines()
        self.content = ""
        isMultiline = False
        checkMultiline = False
        checkSingleline = False
        if multiLineCommentEnd != "" and multiLineCommentStart != "":
            checkMultiline = True
        if singleLineComment != "":
            checkSingleline = True

        for i in range(len(lines)):
            if lines[i].find('\"') > -1 or lines[i].find('\'') > -1:
                self.content += lines[i] + "\n"
                continue
            if checkMultiline and not isMultiline and lines[i].find(multiLineCommentStart) > -1:
                if lines[i].find(self.finalComment) > -1:
                    self.content += lines[i].replace(file_model.finalComment, "") + "\n"
                else:
                    isMultiline = True
                    if lines[i].find(multiLineCommentEnd) > -1:
                        isMultiline = False
                        temp = lines[i][lines[i].index(multiLineCommentEnd) + len(multiLineCommentEnd):]
                        self.content += lines[i][:lines[i].index(multiLineCommentStart)] + temp + "\n"
                    else:
                        self.content += lines[i][:lines[i].index(multiLineCommentStart)] + "\n"
            elif checkMultiline and isMultiline:
                if lines[i].find(multiLineCommentEnd) > -1:
                    isMultiline = False
                    self.content += lines[i][lines[i].index(multiLineCommentEnd) + len(multiLineCommentEnd):] + "\n"

            elif checkSingleline and lines[i].find(singleLineComment) > -1:
                if lines[i].find(self.finalComment) > -1:
                    self.content += lines[i].replace(self.finalComment, "") + "\n"
                else:
                    self.content += lines[i][:lines[i].index(singleLineComment)] + "\n"
            else:
                self.content += lines[i] + "\n"


    def getContentInLines(self):
        """
        This function converts the content into an array of lines.
        :return: content
        :rtype: array
        """
        lines = []
        if(self.content == ""):
             return lines
        lines = self.content.splitlines()
        return lines

    def uglify(self):
        """
        Removes all the `\n` from the file so the file becomes a single line.
        :return:
        """
        self.content = self.content.replace("\n", "")