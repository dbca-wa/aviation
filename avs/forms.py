from django import forms
from uni_form.helpers import Submit, FormHelper
from avs.models import *
from django.forms.models import BaseInlineFormSet

class DateRangeForm(forms.Form):
    date_from = forms.DateField(('%d/%m/%Y',), label='Date From', required=False,  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input daterange',            
        })
    )
    date_to = forms.DateField(('%d/%m/%Y',), label='Date To', required=False,  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input daterange',            
        })
    )
class PilotFilterDRForm(DateRangeForm):
    pilot = forms.ModelMultipleChoiceField(queryset = Pilot.objects.all().order_by("first_name"),required=False, label='Pilots', 
        widget=forms.SelectMultiple(attrs={'width': '100px','height':'300px',}))

class FieldFilterForm(forms.Form):
    aircraft = forms.ModelMultipleChoiceField(queryset = Aircraft.objects.all().order_by("name"),required=True, label='Aircraft',
        widget=forms.SelectMultiple(attrs={'class':'multiselect'})) 
    pilot = forms.ModelMultipleChoiceField(queryset = Pilot.objects.all().order_by("first_name"),required=True, label='Pilots',
        widget=forms.SelectMultiple(attrs={'class':'multiselect'}))
    task = forms.ModelMultipleChoiceField(queryset = Task.objects.all().order_by("name"),required=True, label='Tasks',
        widget=forms.SelectMultiple(attrs={'class':'multiselect'}))

class FieldFilterDRForm(DateRangeForm, FieldFilterForm):
    None

class FlightLogFieldSearch(FieldFilterDRForm):
    flight_log_number = forms.CharField(required=False, label="Flight Log Number", widget=forms.TextInput(attrs={
            'style':'width:150px',            
        })
    )
    fire_number = forms.CharField(required=False, label="Fire Number", widget=forms.TextInput(attrs={
            'style':'width:150px',            
        })
    )
    job_number = forms.CharField(required=False, label="Job Number", widget=forms.TextInput(attrs={
            'style':'width:200px',            
        })
    )
    

class AircraftFilterForm(forms.Form):
     aircraft = forms.ModelMultipleChoiceField(queryset = Aircraft.objects.all().order_by("name"),required=False, label='Aircraft',
        widget=forms.SelectMultiple(attrs={'class':'multiselect'}))    

class AircraftTaskFilterDRForm(AircraftFilterForm):
    task = forms.ModelMultipleChoiceField(queryset = Task.objects.all().order_by("name"),required=False, label='Task',
        widget=forms.SelectMultiple(attrs={'class':'multiselect'}))

class DutyRangeForm(forms.Form):
    date_from = forms.DateField(('%d/%m/%Y',), label='Date From', required=False,  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input daterange',            
        })
    )
    date_to = forms.DateField(('%d/%m/%Y',), label='Date To', required=False,  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input daterange',            
        })
    )
    start_point = forms.DateField(('%d/%m/%Y',), label='Start Point', required=False,  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input daterange',            
        })
    )
    
class DateRangeSortForm(forms.Form):
    date_from = forms.DateField(('%d/%m/%Y',), label='Date From', required=False,  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input daterange',            
        })
    )
    date_to = forms.DateField(('%d/%m/%Y',), label='Date To', required=False,  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input daterange',            
        })
    )
    sort = forms.ChoiceField(label='Sort Date', choices=(('A', 'Ascending'),('D', 'Descending')))
    

class BaseForm(forms.ModelForm):
    helper = FormHelper()
    submit = Submit('save','Save Changes')
    helper.add_input(submit)
    
    class Meta:
        None

class PilotForm(BaseForm):
    effective_to = forms.DateField(('%d/%m/%Y',), label='Effective To', required=False,  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input daterange',            
        })
    )   
    class Meta:
        model = Pilot
        fields = ('first_name','last_name','code','effective_to')
        exclude = ['creator', 'modifier','effective_from']
        widgets = {'first_name':forms.TextInput(attrs={'size':40}),}

class AircraftForm(BaseForm):
    effective_to = forms.DateField(('%d/%m/%Y',), label='Effective To', required=False,  
    widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input daterange',            
        })
    )
    class Meta:
        model = Aircraft
        fields = ('name','description','effective_to')
        exclude = ['creator', 'modifier','effective_from']

class TaskForm(BaseForm):
    effective_to = forms.DateField(('%d/%m/%Y',), label='Effective To', required=False,  
    widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input daterange',            
        })
    )
    class Meta:
        model = Task
        fields = ('name','description','effective_to')
        exclude = ['creator', 'modifier','effective_from']
        
class AircraftFlightLogForm(BaseForm):   
    fire_danger_index = forms.IntegerField(label='Fire Danger Index', required=False)   
    aircraft = forms.ModelChoiceField(queryset=Aircraft.objects.filter(effective_to__exact=None), empty_label="",
    widget=forms.Select(attrs={
            'style': 'width:150px',            
        })
    )   
       
    date = forms.DateField(('%d/%m/%Y',), label='Date', required=True,  
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class':'input',
        })
    )   
    class Meta:
        model = AircraftFlightLog
        exclude = ['creator', 'modifier']    
    def __init__(self, *args, **kwargs):
        super(AircraftFlightLogForm, self).__init__(*args, **kwargs)
        #self.fields.keyOrder = ['flight_log_number','date','aircraft','fire_danger_index','remarks']
        self.fields.keyOrder = ['flight_log_number','date','aircraft','fire_danger_index','remarks']
    
        
class AircraftFlightLogDetailForm(BaseForm):   
    task = forms.ModelChoiceField(queryset=Task.objects.filter(effective_to__exact=None), empty_label="")
    pilot_in_command = forms.ModelChoiceField(queryset=Pilot.objects.filter(effective_to__exact=None), empty_label="")  
    pilot_in_command_under_supervision = forms.ModelChoiceField(queryset=Pilot.objects.filter(effective_to__exact=None), empty_label="", required=False)
    datcon = forms.DecimalField(widget=forms.TextInput(attrs={
            'style': 'width:50px',            
        })
    )
    time_out = forms.TimeField(('%H%M',), label='Time Out (24)', required=True,  
        widget=forms.TimeInput(format='%H%M', attrs={
            'class':'input',
            'style':'width:70px',            
        })
    )
    fuel_added = forms.IntegerField(required=True, widget=forms.TextInput(attrs={
            'style':'width:70px',            
        })
    )
    landings = forms.IntegerField(required=True, widget=forms.TextInput(attrs={
            'style':'width:70px',            
        })
    )
    fire_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'style':'width:100px',            
        })
    )
    job_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'style':'width:200px',            
        })
    )
    class Meta:
        model = AircraftFlightLogDetail
        exclude = ['creator', 'modifier','aircraft_flight_log']        
    def __init__(self, *args, **kwargs):
        super(AircraftFlightLogDetailForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['datcon', 'time_out', 'task', 'fuel_added','landings','fire_number','job_number','pilot_in_command','pilot_in_command_under_supervision']


class DutyTimeForm(BaseForm):
    remarks = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}),required=False)
    date = forms.DateField(('%d/%m/%Y - %A',), label='Date', required=True, widget=forms.DateInput(format='%d/%m/%Y - %A', attrs={'class':'input','readonly':'readonly',}))
    datetime_on_first = forms.TimeField(('%H%M',), label='Time On (24)', required=False, widget=forms.TimeInput(format='%H%M', attrs={'class':'input',}))
    datetime_off_first = forms.TimeField(('%H%M',), label='Time Off (24)', required=False, widget=forms.TimeInput(format='%H%M', attrs={'class':'input',}))
    class Meta:
        model = DutyTime
        exclude = ['creator', 'modifier']

class RequiredBaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        self.validate_unique()
        if any(self.errors):
            return
        if not self.forms[0].has_changed():
            raise forms.ValidationError("At least one %s is required" % self.model._meta.verbose_name)
        
