# Flow of Computer Science
Flocs is an intelligent web application for learning computer science,
aiming at creating a [flow experience][1].
Flocs is developed by [Adaptive Learning group][2] at Faculty of informatics, Masaryk university.

  [1]: https://en.wikipedia.org/wiki/Flow_(psychology)
  [2]: http://www.fi.muni.cz/adaptivelearning/

## Start working on the project

1. Install Python 3, virtualenv and virtualenvwrapper:

        $ sudo pacman -S python python-virtualenv python-virtualenvwrapper

2. Clone the project repository:

        $ git clone https://github.com/effa/flocs.git

3. Create virtual environment and bind it with the project directory:

        $ cd flocs
        $ mkvirtualenv flocs; setvirtualenvproject

  Name of the virtual envirnoment (flocs) should now appear in front of the prompt.

5. Install dependencies and initialize DB:

        $ make install

  The `make install` command just calls `pip install -r requirements.txt` (which includes django and pylint) and `python manage.py migrate` (to setup database).

That's all. You can check that Django was installed correctly by command `django-admin --version`,
which should output 1.8.2.
You can deactivate the virtual environment by calling `deactivate`.

## Workflow

1. Start virtual environment and jump to the project directory:

        $ workon flocs

2. Pull the changes from the repository.

        $ git pull

3. Take a look at the code written by your friends (quick code review).
  Also look at the documentation, diagrams and issues to decide what feature you want to implement.

4. Create and checkout a git branch for the implemented feature.

        $ git checkout -b name_of_the_feature

5. Write unit tests for the implemented feature (and possibly integration tests as well).
  Check that the tests don't pass.

      $ make test

6. Develop the feature. Enjoy it, experience the state of flow :-)

7. If you need a python console (with all models automatically imported), call:

        $ ./manage.py shell_plus

8. If you need a testing server, call:

        $ ./manage.py runserver

9. Take a regular breaks (e.g. after 25 minuts), stretch yourself (including your eyes).

10. Test the implemented feature:

        $ make test

11. Check the code by pylint:

        $ make check

12. Commit changes:

        $ git add changed_files
        $ git commit -m "feature X implemented"

13. Merge the feature branch to the master branch:

        $ git checkout master
        $ git merge name_of_the_feature

14. Push changes to the GitHub:

        $ git push

15. Deactivate the virtual environment:

        $ deactivate

## Style Guide

Try to stick with [Google Python Style Guide][gpsg].

  [gpsg]: http://google.github.io/styleguide/pyguide.html


Docstring format for functions:

```python
def some_function(foo, bar=None):
    """Short description.

    Detailed description of the function...

    Args:
        foo: Some description.
        bar: Some description.

    Returns:
        What the function returns, ideally with example if it's complicated.

    Raises:
        IOError: When the error occurs.
    """
    pass

```

Docstring format for classes:

```python
class SomeClass(object):
    """Short class summary.

    Detailed information about the class...

    Attributes:
        foo: Some description.
        bar: Some description.
    """

    def __init__(self, foo=True):
        """Inits SomeClass."""
        self.foo = foo
        self.bar = 0
```



## Tips

* If you are using vim, take a look at syntastic and vim-fugitive plugins.


