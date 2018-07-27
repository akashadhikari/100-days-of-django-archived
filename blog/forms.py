from django import forms


class BlogForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title'
    }))
    code_description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Describe what the code is doing'
    }))
    content = forms.CharField(help_text='<b>Place your code snippet in the blank region bounded by '
                                        '<code> code </code> tag. Change <code> class="language-python" </code> '
                                        'to your desired language.</b>',
                              widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))

    def clean_content(self):
        error_message = """<pre class="language-python"><code></code></pre> """
        if '<pre' and '</code></pre>' not in self.cleaned_data['content']:
            raise forms.ValidationError(error_message)
