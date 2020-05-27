from datetime import date
from django import forms
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget


class HotelDatePickerForm(forms.Form):
    begin = JalaliDateField(label=('date'), widget=AdminJalaliDateWidget)
    end = JalaliDateField(label=('date'), widget=AdminJalaliDateWidget)

    def clean(self):
        cleaned_data = super(HotelDatePickerForm, self).clean()
        begin = cleaned_data.get('begin')
        end = cleaned_data.get('end')
        # print(begin, date.today())
        # Check if begin date is greater than today date
        if begin < date.today() or begin >= end:
            raise forms.ValidationError('تاریخ ها نامعتبر است.')
