# -*- coding:utf-8 -*-
__author__ = 'bee'

from django import forms

from .models import MentorScoreWeek

class MentorScoreWeekForm(forms.ModelForm):
    class Meta:
        model = MentorScoreWeek
        fields = ['year', "week", "score", "info"]

    # def update_rank(self):


class UserForm(forms.Form):
    status = forms.ChoiceField(label='学生状态',choices=((0,'全部'),(1,"正常")),required=False)
    server = None

    def __init__(self, user_list, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["server"] =forms.ModelChoiceField(queryset=user_list, label='客服',required=False)