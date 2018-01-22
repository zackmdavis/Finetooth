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

Developed on Python 3.4 (earlier Python 3s may or may not work).

* Clone the repository: `git clone git@github.com:zackmdavis/Finetooth.git`

* *Recommended*: [set up a virtualenv including Pip](https://docs.python.org/3/library/venv.html#an-example-of-extending-envbuilder)

* Install the requirements: `pip install -r dev_requirements.txt`

* Create a file called `.development` (the presence of this file is used to determine that we should use development rather than production-like Django settings): `touch .development`

* Configure static files!

  * If you want to serve static JavaScripts and CSS locally, download them with `./manage.py download_statics`.

  * If you want to use CDNs, export a truthy "NONLOCAL_STATIC_LIBS" environment variable: `export NONLOCAL_STATIC_LIBS=1`.

* Set up the database: `./manage.py migrate`

* *Optional*: run the tests maybe!

  * Django tests: `./manage.py test`

  * JavaScript tests:

    - `jasmine`

    - Visit *http://localhost:8888/* in your favorite browser!

* Use the site! `./manage.py runserver` and visit *http://localhost:8000/* in your favorite browser!
