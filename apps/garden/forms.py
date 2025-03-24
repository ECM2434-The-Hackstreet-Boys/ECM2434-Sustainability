"""
Forms for the garden page

@Author: Edward Pratt
"""

from django import forms
from .models import Block


class BlockForm(forms.ModelForm):
    """Form for adding a new block with all fields."""
    class Meta:
        model = Block
        fields = ['name', 'visibleName', 'blockPath', 'cost', 'value']

class EditBlockForm(forms.ModelForm):
    """Form for editing only cost and value of an existing block."""
    class Meta:
        model = Block
        fields = ['cost', 'value']