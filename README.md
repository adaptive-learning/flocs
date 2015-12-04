# Flow of Computer Science
Flocs is an intelligent web application for learning computer science,
aiming at creating a [flow experience][1].
Flocs is developed by [Adaptive Learning group][2] at Faculty of informatics, Masaryk university.

  [1]: https://en.wikipedia.org/wiki/Flow_(psychology)
  [2]: http://www.fi.muni.cz/adaptivelearning/

## Start working on the project

1. Install Python 3, virtualenv, virtualenvwrapper and npm:

        $ sudo pacman -S python python-virtualenv python-virtualenvwrapper npm

2. Install Grunt and Bower using npm:

        $ sudo npm install -g grunt-cli karma-cli bower

2. Configure virtualenv and virtualenvwrapper by adding the following two lines in your `~/.bashrc`:

        export WORKON_HOME=~/.virtualenvs
        source /usr/bin/virtualenvwrapper.sh

  Load the changes:

        $ source ~/.bashrc

3. Clone the project repository:

        $ git clone https://github.com/effa/flocs.git

4. Create virtual environment and bind it with the project directory:

        $ cd flocs
        $ mkvirtualenv flocs && setvirtualenvproject

  The name of the virtual envirnoment (flocs) should now appear in front of the prompt.

5. Install dependencies and initialize DB:

        $ make update

  The `make update` command uses pip, npm and bower to install both backend and frontend dependencies (including django and pylint) and it also sets up the database for development. (See Makefile for details.)

You can check that Django was installed correctly by command `django-admin --version`,
which should output 1.8.2.
You can deactivate the virtual environment by calling `deactivate`.

## Workflow

1. Start the virtual environment and jump to the project directory:

        $ workon flocs

2. Pull the changes from the repository.

        $ git pull

3. Update dependencies and database:

        $ make update

4. Take a look at the code written by your friends (quick code review).
  Also look at the documentation, diagrams and issues to decide what feature you want to implement.

5. Create and checkout a git branch for the implemented feature.

        $ git checkout -b name_of_the_feature

6. Write unit tests for the implemented feature (and possibly integration tests as well).
  Check that the tests don't pass.

        $ make test

7. Develop the feature. Enjoy it, experience the state of flow :-)

  *  If you need a python console (with all models automatically imported), call:

          $ ./manage.py shell_plus

  * If you need a testing server, call:

          $ ./manage.py runserver

  * If you change data in fixtures and want to load them to the database:

          $ make db-load-data

  * If you change the data model, create and apply a migration:

          $ ./manage.py makemigrations
          $ ./manage.py migrate

  * If you are working on frontend, you need to start the testing server and run `grunt work` task to automatically apply all changes into a development build (cancatenating html partials, JavaScript and CSS files, compiling index.html, etc.). This can be done by a single command:

          $ ./manage.py gruntserver

  * Take a regular breaks (e.g. after 25 minuts), stretch yourself (including your eyes).

8. Test the implemented feature and check the code by pylint:

        $ make test
        $ make check

9. Commit changes:

        $ git add changed_files
        $ git commit -m "feature X implemented"

10. Merge the feature branch to the master branch:

        $ git checkout master
        $ git merge name_of_the_feature

11. Push changes to the GitHub:

        $ git push

12. Deactivate the virtual environment:

        $ deactivate

13. Celebrate the developed feature with some physical exercise and healthy snack.


## Additional recommendations

* Check our [style guide](https://github.com/effa/flocs/wiki/Style-Guide).
* Check our [development tools](https://github.com/effa/flocs/wiki/Development-tools) wiki page.
* If you are using vim, take a look at syntastic and vim-fugitive plugins.
