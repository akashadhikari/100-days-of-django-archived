from django import forms


class BlogForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title of your code.'
    }))
    code_description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Describe what the code is doing.',
        'rows':4,
        'cols': 15
    }))
    content = forms.CharField(help_text='<b>Place your code snippet in the blank region bounded by '
                                        '<code> code </code> tag. Change <code> class="language-python" </code> '
                                        'to your desired language.</b>'
                                        '<a href="#" data-toggle="modal" data-target="#helpCodeModal">'
                                        ' See Example</a>',
                              widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))


class CommentForm(forms.Form):
    comment = forms.CharField(help_text='<b>You can also create a code snippet inside <code> pre </code> tags</b>.<br>'
                                        '<a href="#" data-toggle="modal" data-target="#helpCodeModal">See Example</a>.',
                              widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows':2,
        'cols': 2,
        'placeholder': 'Submit your comment.'
    }))
