from django import forms
from .models import Message
from organisation.models import Team


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['team', 'subject', 'body']
        widgets = {
            'team': forms.Select(attrs={'class': 'form-select sky-select'}),
            'subject': forms.TextInput(attrs={
                'class': 'form-control sky-search-input',
                'placeholder': 'Enter subject',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control sky-textarea',
                'placeholder': 'Type your message here...',
                'rows': 8,
            }),
        }
        labels = {
            'team': 'Select Team',
            'subject': 'Subject',
            'body': 'Message',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.filter(status='active')
        self.fields['team'].empty_label = 'Choose a team...'
