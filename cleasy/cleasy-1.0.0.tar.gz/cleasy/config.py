from PyInquirer import Token, style_from_dict


class Config:
    menu = None

    prompt_style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#673AB7 bold',
        Token.Instruction: '',
        Token.Answer: '#2196f3 bold',
        Token.Question: '',
    })

    banner_figlet_font = 'colossal'
    banner_header_color = 'blue'
    banner_subheader_color = 'green'


config = Config()
