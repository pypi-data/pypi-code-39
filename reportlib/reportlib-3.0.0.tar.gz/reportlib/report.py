import os
from os.path import dirname, exists, join, abspath
from uuid import uuid4

import htmlmin
import yaml
from IPython.display import display, HTML
from css_html_js_minify import css_minify

from reportlib.utils.mailing import send_email
from reportlib.utils.pandas.styler import Styler
from reportlib.utils.templating import template_loader, get_template_dirs


class Report:
    def __init__(self, 
                 template_name='base/base.html',
                 styles=None,
                 title=None, extra=None, context=None, 
                 html_output=None, email_config=None, email_env=None):
        self.template_name = template_name
        
        styles = styles or []
        if isinstance(styles, str):
            styles = [styles]
        self.styles = list({'base/styles.css'} | set(styles))
        
        self.title = title
        self.extra = extra
        self.context = context or {}
        self.tables = []
        
        self.html_output = html_output
        self.email_config = email_config
        self.email_env = email_env
        
    def _get_context(self):
        return {
            'title': self.title,
            'extra': self.extra,
            **self.context,
            'tables': self.tables,
            'styles': self._load_styles(),
        }

    def add_table(self, styler):
        if isinstance(styler, Styler):
            styler.set_context(**self.context)
            self.tables.append(styler)
        elif isinstance(styler, (list, tuple)):
            for s in styler:
                self.add_table(s)
        else:
            raise ValueError('`styler` must be an instance of `reportlib.utils.pandas.styler.Styler` or a list of them')
        
    def add_grouped_table(self, stylers):
        if len(stylers) > 1:
            for i, styler in enumerate(stylers):
                if i > 0:
                    styler.set_context(skip_table_open_tag=True)
                if i < len(stylers) - 1:
                    styler.set_context(skip_table_close_tag=True)
        self.add_table(stylers)
        
    def _load_styles(self):
        styles = []
        for path in self.styles:
            for folder in get_template_dirs():
                _path = join(folder, path)
                if exists(_path):
                    with open(_path, 'r') as f:
                        css = f.read()
                        css = css_minify(css)
                        styles.append(css)
                    break
        return styles
      
    def run(self):
        html_string = self.render_html()
        display(HTML(html_string))

        self.write_to_file(html_string)
        self.send_email(html_string)

    def write_to_file(self, html_string):
        if self.html_output:
            html_output = abspath(self.html_output)
            os.makedirs(dirname(html_output), exist_ok=True)
            with open(html_output, 'w', encoding='utf-8') as f:
                f.write(html_string)

    def send_email(self, html_string):
        if self.email_config and self.email_env:
            with open(self.email_config, 'r') as f:
                email_cfgs = yaml.load(f, Loader=yaml.FullLoader)
            if self.email_env in email_cfgs:
                email_cfg = email_cfgs[self.email_env]
                email_cfg['subject'] = email_cfg['subject'].format(uuid4=uuid4(), **self.context)
                send_email(email_cfg, html_string)
            else:
                print(f"ERROR: email_env = {email_env} not exists. Available env: {' '.join(email_cfgs.keys())}")

    def render_html(self, show=True):
        template = template_loader.get_template(self.template_name)
        html_string = template.render(self._get_context())
        html_string = htmlmin.minify(
            html_string,
            remove_comments=True,
            remove_empty_space=True,
            reduce_boolean_attributes=True,
            reduce_empty_attributes=True,
            remove_optional_attribute_quotes=True,
            convert_charrefs=True,
        )
        return html_string

