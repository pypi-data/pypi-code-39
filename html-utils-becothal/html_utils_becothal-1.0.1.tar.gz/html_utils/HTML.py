from file_model import file_model
import re
import base64
from CSS import CSS


class HTML(file_model):

    cssRegex = "(<link rel=\"stylesheet\".* href=\".*\\.css\">)"
    jsRegex = "(<script.*src=\".*\"><\/script>)"

    def __init__(self):
        file_model.__init__(self)
        print"HTML init"

    def inlineCSS(self):
        """
        Searches for linked CSS files and copies the content into the HTML file,
        so that there is only one file in the end.
        """
        tempString = ""
        if self.content == "":
            print "InlineCSS: cannot inline. File must be read first."
            return
        cssFiles = re.findall(self.cssRegex, self.content)
        if len(cssFiles) > 0:
            i = 0
            for item in cssFiles:
                if i == 0:
                    tempString = "<style>"

                cssFile = CSS()
                cssFile.readFile(self.rootDir + HTML.getFilePathFromLink(str(item)))
                cssFile.removeComments("", "/*", "*/")
                cssFile.trueTypeToBase64()
                tempString += cssFile.toString()

                if i == len(cssFiles)-1:
                    tempString += "</style>"

                self.content = self.content.replace(str(item), tempString)

                tempString = ""
                i += 1

    def inlineJS(self):
        """
        Searches the HTML file for linked JavaScript files and inlines them to the HTML file.
        """
        tempString = ""
        if self.content == "":
            print "inlineJS: cannot inline. Content is Empty. File must be read first"
            return
        jsFiles = re.findall(self.jsRegex, self.content)
        if len(jsFiles) > 0:
            i = 0
            for item in jsFiles:
                if i == 0:
                    tempString = "<script>"
                jsFile = file_model()
                jsFile.readFile(self.rootDir + HTML.getFilePathFromLink(str(item)))
                jsFile.removeComments("//", "/*", "*/")
                tempString += jsFile.toString()
                if i == len(jsFiles)-1:
                    tempString += "</script>"

                self.content = self.content.replace(str(item), tempString)
                tempString = ""
                i += 1

    def writeFile(self, fileName):
        """
        Writes the content of the HTML-Object into a File
        :param fileName: Filename for the output file
        :type fileName: str
        """
        if fileName == "":
            print "writeFile: No FileName provided!"
            return
        else:
            fileHandler = open(fileName, "w")
            fileHandler.write(self.toString())
            fileHandler.close()

    def imagesToBase64(self):
        """
        Converts the source for <img> tags to Base64.
        Only the following formats are possible:
         - bmp
         - gif
         - jpeg
         - png
         - svg
        :return:
        """
        mimeType = {
            "bmp": "bmp",
            "gif": "gif",
            "jpg": "jpeg",
            "jpe": "jpeg",
            "jpeg": "jpeg",
            "png": "png",
            "svg": "svg+xml"
        }
        imageRegex = "<img.*src=.*"
        images = re.findall(imageRegex, self.content)
        for item in images:
            fileName = item[item.find("src=") + 5:item.find("\"", item.find("src=") + 5)]
            with open(self.rootDir + fileName, "rb") as imageFile:
                imageFileContent = imageFile.read()
                encodedString = base64.b64encode(imageFileContent)
                imageFile.close()
            self.content = self.content.replace(fileName, "data:image/"
                + mimeType[fileName[fileName.rfind(".")+1:len(fileName)]] + ";base64," + encodedString)

    @staticmethod
    def getFilePathFromLink(link):
        """
        Returns the filepath for a file in a <link> in HTML
        :param link: <link> from HTML
        :type link: str
        :returns: Filepath provided in the <link>
        :rtype: str
        """
        if link == "":
            print "getFilePathFromLink: No link provided"
            return
        filePath = ""
        if link.find("href=") > 0:
            filePath = link[link.find("href=\"") + 6:link.rfind("\"")]
        elif link.find("src=") > 0:
            filePath = link[link.find("src=\"") + 5:link.rfind("\"")]
        else:
            print "getFilePathFromLink: Unrecognized pattern :" + link
            return
        return filePath