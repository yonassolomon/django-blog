# LINE 1: Import the forms module from Django
from django import forms
# Think: "Get Django's form tools"

# LINE 2: Import our Post model from current folder
from .models import Post
# Think: "Get our Post database model"

# LINE 3: Create a form class based on Post model
class PostForm(forms.ModelForm):
    # Think: "Make a form that matches our Post table"
    
    # LINE 4: Inner class for configuration
    class Meta:
        # Think: "Settings for this form"
        
        # LINE 5: Which model to use
        model = Post
        # Think: "This form is for Post objects"
        
        # LINE 6: Which fields to include
        fields = ['title', 'content', 'is_published']
        # Think: "Show these 3 fields in the form"