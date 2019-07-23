#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-19 18:32
# @Author  : weihuchao

import importlib
import os


def _analysis_patterns(urls, preifx, urlpatterns):
    for urlpattern in urlpatterns:
        full_path = preifx + urlpattern.regex.pattern
        if getattr(urlpattern, "url_patterns", None):
            _analysis_patterns(urls, full_path, urlpattern.url_patterns)
        else:
            urls.append(full_path)


def get_all_urls(project_name=None):
    """
    get django project all urls list.
    must run in base project dir.
    """
    urls = []

    if not project_name:
        project_name = os.path.basename(os.getcwd())

    project_urls_ = importlib.import_module(project_name + ".urls")

    _analysis_patterns(urls, "", project_urls_.urlpatterns)
    return urls
