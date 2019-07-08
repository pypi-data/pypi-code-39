from IPython.display import display
from IPython.display import clear_output


def manual_captcha_solver(image):

  display(Image.fromarray(image))
  captcha = input()
  clear_output()
  return captcha
