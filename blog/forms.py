from django import forms


class BlogForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title of your code.'
    }))
    code_description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Describe what the code is doing.',
        'rows': 4,
        'cols': 15
    }))

    TRUE_FALSE_CHOICES = (
        (True, 'Public'),
        (False, 'Private')
    )

    visibility = forms.ChoiceField(choices=TRUE_FALSE_CHOICES,
                                   label="Visibility",
                                   required=True,
                                   initial='',
                                   widget=forms.Select(attrs={
                                       'class': 'form-control',
                                   }))
    content = forms.CharField(help_text='<b>Place your code snippet in the blank region bounded by '
                                        '<code> code </code> tag. Change <code> class="language-python" </code> '
                                        'to your desired language.</b>'
                                        '<a href="#" data-toggle="modal" data-target="#helpCodeModal">'
                                        ' See Example</a>',
                              widget=forms.Textarea(attrs={
                                  'class': 'form-control',
                              }))

    def __init__(self, *args, **kwargs):
        self.is_auth = kwargs.get('initial').get('visibility')

        super(BlogForm, self).__init__(*args, **kwargs)

        # import ipdb; ipdb.set_trace()

        if not self.is_auth:
            del self.fields['visibility']


class CommentForm(forms.Form):
    comment = forms.CharField(help_text='<b>You can also create a code snippet inside <code> pre </code> tags</b>.<br>'
                                        '<a href="#" data-toggle="modal" data-target="#helpCodeModal">See Example</a>.',
                              widget=forms.Textarea(attrs={
                                  'class': 'form-control',
                                  'rows': 2,
                                  'cols': 2,
                                  'placeholder': 'Submit your comment.'
                              }))
