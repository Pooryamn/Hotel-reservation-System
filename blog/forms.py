from datetime import date
from django import forms
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from .models import Score


class HotelDatePickerForm(forms.Form):
    begin = JalaliDateField(label=('تاریخ ورود:'), widget=AdminJalaliDateWidget)
    end = JalaliDateField(label=('تاریخ خروج:'), widget=AdminJalaliDateWidget)

    def clean(self):
        cleaned_data = super(HotelDatePickerForm, self).clean()
        begin = cleaned_data.get('begin')
        end = cleaned_data.get('end')
        # Check if begin date is greater than today date
        if begin < date.today() or begin >= end:
            raise forms.ValidationError('تاریخ ها نامعتبر است.')


class ReservationTrackingForm(forms.Form):
    tracking_code = forms.CharField(max_length=10, label="کد پیگیری")
    phone = forms.CharField(max_length=11, label='شماره تلفن همراه')
    

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ('score', 'description')
