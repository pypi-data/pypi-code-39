import re
from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import quote

__version__ = '0.1.2'


def main():
  arg_parser = ArgumentParser(
      description='Generates navigation for a markdown file. Just add comments <!-- nav --><!-- /nav --> to the desired position.')
  arg_parser.add_argument('files', help='list of markdown files', nargs='+')
  arg_parser.add_argument(
      '--title', default='Table of Contents', help='navigation title')
  args = arg_parser.parse_args()

  for file in args.files:
    with Path(file).resolve().open('r+') as fp:
      content = fp.read()
      # Сначала нормализуем контент, удаляя все вставки кода
      cleaned = re.sub(r'`.*?`', '', content, flags=re.S)

      cleaned = re.sub(r'\<!-- (nav) --\>.*?\<!-- /\1 --\>',
                       '', cleaned, flags=re.S)

      # Теперь ищем заголовки
      headers = re.findall('^#.*', cleaned, re.M)

      nav = ['', '# {}'.format(args.title), '']
      for header in headers:
        name = header.lstrip('#')
        depth = len(header) - len(name)
        name = name.strip()
        # Теперь вырезаем ссылки
        name = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', name)
        uri = name.lower()
        # Вырезаем все не буквенно-цифровые символы
        # «-» то же не нужно вырезать
        uri = re.sub(r'[^\w\s-]', '', uri)
        # Заменяем пробелы на «-»
        uri = uri.replace(' ', '-')
        uri = quote(uri)
        nav.append('{}1. [{}](#{})'.format('   ' * (depth - 1), name, uri))

      nav.append('')
      content = re.sub(r'(?<=\<!-- (nav) --\>).*?(?=\<!-- /\1 --\>)',
                       '\n'.join(nav), content, flags=re.S)

      fp.seek(0)
      fp.truncate()
      fp.write(content)
