from LogoCreator.designs import char_designs


class ConsoleLogo:

    design = char_designs

    @staticmethod
    def write_to_console(str_input, size=1, char=']'):
        return '\n'.join(ConsoleLogo._generate_alphabet(str_input, size, char))

    @staticmethod
    def _generate_alphabet(str_input, size, replace_char):
        res = []
        for char in str_input:
            res.append(ConsoleLogo._get_design(char, replace_char, size))
        output = []
        for i in range(len(res[0])):
            output.append((' ' * size).join([item[i] for item in res]))
        return output

    @staticmethod
    def _get_design(character: str, use_char: str, size: int):
        character = ConsoleLogo.design.get(character.upper())
        character = character.replace('*', use_char)
        lines = character.split('\n')
        result = []
        min_lenth = len(character) * size
        for line in lines:
            if len(line.strip()):
                temp = ''.join([x * size for x in line.strip() if x != '\n'])
                min_lenth = min(len(temp), min_lenth)
                result.extend([temp.replace('_', ' ')] * size)
        character = [line[:min_lenth] for line in result]
        return character


if __name__ == '__main__':
    ConsoleLogo.write_to_console('docgen', size=3, char=']')
    ConsoleLogo.write_to_console('v1.12.7', size=2, char=']')
