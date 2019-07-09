import os
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import click
import six
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)

from pyfiglet import figlet_format

base_url = 'https://redmine.neurotech.com.br'
        
try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


# conf = ConfigStore("EmailCLI")

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

def registerActivity(redmineinfo):
    login = redmineinfo.get("login")
    password = redmineinfo.get("password")
    activity = redmineinfo.get("activity")
    activity_type = redmineinfo.get("activity_type")
    
    driver = webdriver.Firefox(executable_path='C:\\geckodriver.exe')
    driver.get(base_url)
    
    login_text_field = driver.find_element_by_id('username')
    login_text_field.send_keys(login)
    
    password_text_field = driver.find_element_by_id('password')
    password_text_field.send_keys(password)

    login_button = driver.find_element_by_name('login')
    login_button.click()
    
    activity_url = f'https://redmine.neurotech.com.br/issues/{activity}/time_entries/new'
    driver.get(activity_url)
    
    time_text_field = driver.find_element_by_id('time_entry_hours')
    time_text_field.send_keys('8')
    
    type_field = driver.find_element_by_id('time_entry_activity_id')
    type_field.send_keys(activity_type)
    
    commit_button = driver.find_element_by_name('commit')
    commit_button.click()
    
    response = {'status_code': 202}
    return response

def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)

class EmailValidator(Validator):
    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"

    def validate(self, email):
        if len(email.text):
            if re.match(self.pattern, email.text):
                return True
            else:
                raise ValidationError(
                    message="Invalid email",
                    cursor_position=len(email.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(email.text))

class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))

class FilePathValidator(Validator):
    def validate(self, value):
        if len(value.text):
            if os.path.isfile(value.text):
                return True
            else:
                raise ValidationError(
                    message="File not found",
                    cursor_position=len(value.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))

def askSettingsInformation():
    questions = [
        {
            'type': 'confirm',
            'name': 'load_defaults',
            'message': 'Do you want to load the cached settings?',
        },
    ]
    
    answers = prompt(questions, style=style)
    return answers

def askRedmineInformation():
    
    questions = [
        {
            'type': 'input',
            'name': 'login',
            'message': 'Redmine Login',
            'validate': EmptyValidator
        },
        {
            'type': 'input',
            'name': 'password',
            'message': 'Redmine Password',
            'validate': EmptyValidator
        },
        {
            'type': 'input',
            'name': 'activity',
            'message': 'Activity',
            'validate': EmptyValidator
        },
        {
            'type': 'input',
            'name': 'activity_type',
            'message': 'Activity Type',
            'validate': EmptyValidator
        },
        {
            'type': 'confirm',
            'name': 'register',
            'message': 'Do you want to register the activity now',
        },
    ]
    '''
    {
        'type': 'list',
        'name': 'content_type',
        'message': 'Content Type:',
        'choices': ['Text', 'HTML'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'input',
        'name': 'content',
        'message': 'Enter plain text:',
        'when': lambda answers: getContentType(answers, "text"),
        'validate': EmptyValidator
    },
    {
        'type': 'confirm',
        'name': 'confirm_content',
        'message': 'Do you want to send an html file',
        'when': lambda answers: getContentType(answers, "html")

    },
    {
        'type': 'input',
        'name': 'content',
        'message': 'Enter html:',
        'when': lambda answers: not answers.get("confirm_content", True),
        'validate': EmptyValidator
    },
    {
        'type': 'input',
        'name': 'content',
        'message': 'Enter html path:',
        'validate': FilePathValidator,
        'filter': lambda val: open(val).read(),
        'when': lambda answers: answers.get("confirm_content", False)
    },
    '''

    answers = prompt(questions, style=style)
    return answers


@click.command()
def main():
    """
    Simple CLI for logging activities in Redmine using Selenium
    """
    log("RedCLIne", color="blue", figlet=True)
    log("Welcome to Ian's Redmine CLI", "green")
    
    redmineinfo = {}
    should_ask_for_settings = True
    if os.path.exists('settings.txt'):
        settingsinfo = askSettingsInformation()
        load_defaults = settingsinfo.get('load_defaults', False)
        
        if load_defaults:
            log('Loading cached settings...', 'yellow')
            try:
                with open('settings.txt') as f:
                    redmineinfo['login'] = f.readline().strip()
                    redmineinfo['password'] = f.readline().strip()
                    redmineinfo['activity'] = f.readline().strip()
                    redmineinfo['activity_type'] = f.readline().strip()
                    redmineinfo['register'] = True
                    should_ask_for_settings = False
            except:
                log('Could not load settings.', 'red')
    
    if should_ask_for_settings:
        redmineinfo = askRedmineInformation()
        with open('settings.txt', 'w') as f:
            settings = f'''
            {redmineinfo['login']}
            {redmineinfo['password']}
            {redmineinfo['activity']}
            {redmineinfo['activity_type']}
            '''
            f.write(settings)
    
    if redmineinfo.get("register", False):
        try:
            log('Registering activity...', 'blue')
            response = registerActivity(redmineinfo)
        except Exception as e:
            raise Exception("An error occured: %s" % (e))
        
        if response['status_code'] == 202:
            log("Activity registered successfully", "blue")
        else:
            log("An error while trying to register the activity", "red")

def start():
    main(obj={})
    
if __name__ == '__main__':
    main()