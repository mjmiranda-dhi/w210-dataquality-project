
# ERRATUM.IO
### DMB web development for W210 Capstone Project

I've been working for a bit on the new site design.  Left to do:
1. Clean up user registration (pages/links)
2. Move from using registration-redux simple backend (no activation required) to full backend.  Until we switch that over (for which we'll need a working SMTP server), some of the registration functionality won't work yet.
3. Move from original site to Demo page:
  * `<div>` ids for targets
  * Target 1 (row 1): upload functionality
  * Target 2 (row 1): field definition functionality (optional--was doing this in Angular browser-side)
  * Target 3 (row 2): Tim's file stat table
  * Target 4 (row 2): "before" visualization.  We may get more utility from just showing errors in a table.  Future functionality: add slider for user to specify level of confidence.
  * Target 5 (row 2): "after" visualization.  For continuity and comparability, this should be the same type of viz as the "before."

## Installation

1. Create a virtual environment.  In Windows, this can be done in Anaconda using the following (note that we are using Python 3!):
```
conda create -n erratum python=3.4 anaconda
```

2. Activate the virtual environment.  You'll need to do this before installing the other packages.
```
activate erratum
```

3. Install required packages.  If using conda, Django can be installed using `conda install django`.
```
pip install django
pip install django-progressbarupload
pip install django-registration-redux
pip install django-crispy-forms
```

## Running this thing.

If you haven't used Django before, no worries.  Running this is dead easy.  First, activate the _erratum_ virtual environment (if it isn't already activated) and in the root of the web directory (where _manage.py_ is), run the following command: `python manage.py runserver`.

## Notes on users

I created users here--log in as any of them.  __dmburt__ is the superuser (it was the first account I created in this).  The other accounts are dev accounts: judofighter25 (_maxpassword_), rtimothy (_timpassword_), mjmiranda (_mjpassword_).


