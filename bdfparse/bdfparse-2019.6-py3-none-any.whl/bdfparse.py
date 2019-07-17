import numpy as np


class Font:
    def __init__(self, bdfFile):
        self.properties = self.parse_properties(bdfFile)
        self.chars = self.parse_chars(bdfFile)
        self.cols = self.properties["FONTBOUNDINGBOX"][0]
        self.rows = self.properties["FONTBOUNDINGBOX"][1]
        self.shape = (self.rows, self.cols)

    def parse_properties(self, bdfFile):

        properties = {"COMMENT": []}
        with open(bdfFile, "r") as bdf:
            line = bdf.readline()

            while not line.startswith("STARTCHAR"):

                if line.startswith("COMMENT"):
                    properties["COMMENT"].append(
                        line.replace("COMMENT", "").replace("\n", "")
                    )

                if line.startswith("FONT"):
                    properties["FONT"] = line.replace("FONT", "").replace("\n", "")

                if line.startswith("SIZE"):
                    properties["SIZE"] = line.replace("SIZE", "").replace("\n", "")

                if line.startswith("FONTBOUNDINGBOX"):
                    properties["FONTBOUNDINGBOX"] = [
                        int(x)
                        for x in (
                            line.replace("FONTBOUNDINGBOX ", "")
                            .replace("\n", "")
                            .split()
                        )
                    ]

                if line.startswith("STARTPROPERTIES"):
                    properties["STARTPROPERTIES"] = line.replace(
                        "STARTPROPERTIES", ""
                    ).replace("\n", "")

                if line.startswith("FONTNAME_REGISTRY"):
                    properties["FONTNAME_REGISTRY"] = line.replace(
                        "FONTNAME_REGISTRY", ""
                    ).replace("\n", "")

                if line.startswith("FOUNDRY"):
                    properties["FOUNDRY"] = line.replace("FOUNDRY", "").replace(
                        "\n", ""
                    )

                if line.startswith("FAMILY_NAME"):
                    properties["FAMILY_NAME"] = line.replace("FAMILY_NAME", "").replace(
                        "\n", ""
                    )

                if line.startswith("WEIGHT_NAME"):
                    properties["WEIGHT_NAME"] = line.replace("WEIGHT_NAME", "").replace(
                        "\n", ""
                    )

                if line.startswith("SLANT"):
                    properties["SLANT"] = line.replace("SLANT", "").replace("\n", "")

                if line.startswith("SETWIDTH_NAME"):
                    properties["SETWIDTH_NAME"] = line.replace(
                        "SETWIDTH_NAME", ""
                    ).replace("\n", "")

                if line.startswith("ADD_STYLE_NAME"):
                    properties["ADD_STYLE_NAME"] = line.replace(
                        "ADD_STYLE_NAME", ""
                    ).replace("\n", "")

                if line.startswith("PIXEL_SIZE"):
                    properties["PIXEL_SIZE"] = line.replace("PIXEL_SIZE", "").replace(
                        "\n", ""
                    )

                if line.startswith("POINT_SIZE"):
                    properties["POINT_SIZE"] = line.replace("POINT_SIZE", "").replace(
                        "\n", ""
                    )

                if line.startswith("RESOLUTION_X"):
                    properties["RESOLUTION_X"] = line.replace(
                        "RESOLUTION_X", ""
                    ).replace("\n", "")

                if line.startswith("RESOLUTION_Y"):
                    properties["RESOLUTION_Y"] = line.replace(
                        "RESOLUTION_Y", ""
                    ).replace("\n", "")

                if line.startswith("SPACING"):
                    properties["SPACING"] = line.replace("SPACING", "").replace(
                        "\n", ""
                    )

                if line.startswith("AVERAGE_WIDTH"):
                    properties["AVERAGE_WIDTH"] = line.replace(
                        "AVERAGE_WIDTH", ""
                    ).replace("\n", "")

                if line.startswith("CHARSET_REGISTRY"):
                    properties["CHARSET_REGISTRY"] = line.replace(
                        "CHARSET_REGISTRY", ""
                    ).replace("\n", "")

                if line.startswith("CHARSET_ENCODING"):
                    properties["CHARSET_ENCODING"] = line.replace(
                        "CHARSET_ENCODING", ""
                    ).replace("\n", "")

                if line.startswith("DEFAULT_CHAR"):
                    properties["DEFAULT_CHAR"] = line.replace(
                        "DEFAULT_CHAR", ""
                    ).replace("\n", "")

                if line.startswith("FONT_DESCENT"):
                    properties["FONT_DESCENT"] = line.replace(
                        "FONT_DESCENT", ""
                    ).replace("\n", "")

                if line.startswith("FONT_ASCENT"):
                    properties["FONT_ASCENT"] = line.replace("FONT_ASCENT", "").replace(
                        "\n", ""
                    )

                if line.startswith("COPYRIGHT"):
                    properties["COPYRIGHT"] = line.replace("COPYRIGHT", "").replace(
                        "\n", ""
                    )

                if line.startswith("CAP_HEIGHT"):
                    properties["CAP_HEIGHT"] = line.replace("CAP_HEIGHT", "").replace(
                        "\n", ""
                    )

                if line.startswith("X_HEIGHT"):
                    properties["X_HEIGHT"] = line.replace("X_HEIGHT", "").replace(
                        "\n", ""
                    )

                if line.startswith("_GBDFED_INFO"):
                    properties["_GBDFED_INFO"] = line.replace(
                        "_GBDFED_INFO", ""
                    ).replace("\n", "")

                line = bdf.readline()
        return properties

    def parse_chars(self, bdfFile):
        font = {}
        cols = self.properties["FONTBOUNDINGBOX"][0]
        rows = self.properties["FONTBOUNDINGBOX"][1]

        with open(bdfFile, "r") as bdf:
            line = bdf.readline()

            # Go through file until chars start.
            while not line.startswith("CHARS "):
                line = bdf.readline()
            characters = int(line.split(" ")[1])

            for character in range(characters):
                line = bdf.readline()
                char = line.split(" ")[1].replace("\n", "")

                while not line.startswith("BITMAP"):
                    line = bdf.readline()

                bits = ""
                for row in range(rows):

                    bits += bdf.readline()
                font[char] = self.from_hex(bits.strip(), cols)

                if bdf.readline().startswith("ENDFONT"):
                    return font
        return font

    def from_hex(self, values, columns):
        return np.array(
            [list(f"{int(row[:2], 16):0>{columns}b}") for row in values.split("\n")],
            dtype=int,
        )

    def word(self, word: str):
        matrix = np.zeros(self.shape)
        for char in word:
            if char is " ":
                arr = np.zeros(self.shape)
            elif char is "!":
                arr = self.chars["exclam"]
            elif char is "%":
                arr = self.chars["percent"]
            elif char is ",":
                arr = self.chars["comma"]
            elif char is ".":
                arr = self.chars["period"]
            else:
                arr = self.chars[char]

            matrix = np.concatenate((matrix, arr), axis=1)

        return matrix[:, self.cols :]

