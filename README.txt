Writing Streak is a web app for daily writing, along the lines of
https://writingstreak.io, that you can clone and run locally on your computer.
No need to worry about someone else managing your personal writing, and if you
want a new feature, you can just implement it.

Writing Streak is a Django app. To install and run, you'll need Python 3.6 or
later (older versions of Python 3 may also work, but I have not confirmed it).

    # If you use virtualenvwrapper
    $ mkvirtualenv writingstreak --python=python3

    $ git clone https://github.com/iafisher/writingstreak.git
    $ cd writingstreak
    $ pip3 install -r requirements.txt
    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    $ ./manage.py runserver

You are free to use this code however you like, but if you plan on deploying it
to any kind of production setting make sure to change the SECRET_KEY setting in
the writingstreak/settings.py module.
