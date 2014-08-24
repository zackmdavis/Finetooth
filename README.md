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

* *Recommended*: [set up a virtualenv including
   Pip](https://docs.python.org/3/library/venv.html#an-example-of-extending-envbuilder)

* Install the requirements: `pip install -r requirements.txt`

* Set up the database: `./manage.py syncdb --migrate`

* You might want some Posts, Comments, and Votes in the database! You
  can create them at the Django shell:

```
$ ./manage.py shell
Python 3.4.0 (default, Apr 11 2014, 13:05:11) 
[GCC 4.8.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from core.models import *
>>> Post.objects.create(content="hello Django model world 1")
<Post: #1: hello Django>
>>> Post.objects.create(content="hello Django model world 2")
<Post: #2: hello Django>
>>> Comment.objects.create(content="rah", post=Post.objects.get(pk=1))
<Comment: #1: rah>
>>> Post.objects.get(pk=1).vote_set.create(value=1)
<PostVote: 1 on post #1>
```

* `./manage.py runserver` and visit http://localhost:8000/ in your
  favorite browser!