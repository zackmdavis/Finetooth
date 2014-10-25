# Finetooth

<blockquote>
A social network or commenting system that allows everyone to
highlight or vote on sentences in each other's comments.
</blockquote>
&mdash;[@MemberOfSpecies](https://twitter.com/MemberOfSpecies/status/488422875703947265)

<blockquote>
@MemberOfSpecies highlight arbitrary substrings, and combine the votes
where highlighted substrings overlap. character-by-character feedback
</blockquote>
&mdash;[@admittedlyhuman](https://twitter.com/admittedlyhuman/status/488472521457823745)

(idea used without permission)

## Development Setup

Requires Python 3.

* Clone the repository: `git clone git@github.com:zackmdavis/Finetooth.git`

* *Recommended*: [set up a virtualenv including Pip](https://docs.python.org/3/library/venv.html#an-example-of-extending-envbuilder)

* Install the requirements: `pip install -r requirements.txt`

* Set up the database: `./manage.py migrate`

* Run the tests!

  * Django tests: `./manage.py test core`

  * JavaScript tests:

    - Get local copies of jQuery and Underscore: `wget http://code.jquery.com/jquery-2.1.1.min.js http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.7.0/underscore-min.js http://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.7.0/underscore-min.map -P static/libs/`

    - `jasmine`

    - Visit *http://localhost:8888/* in your favorite browser!

* Use the site! `./manage.py runserver` and visit *http://localhost:8000/* in your favorite browser!

