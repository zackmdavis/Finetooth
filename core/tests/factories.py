import os
import random
from datetime import datetime
from collections import OrderedDict
from urllib.request import urlretrieve

from django.utils.text import slugify

import factory

from core.models import (
    FinetoothUser, Post, Comment, PostVote, CommentVote, Tag
)

FACTORY_USER_PASSWORD = "f:O>r<5H%UsBu"

if os.name == "posix":
    dictionary_path = '/usr/share/dict/words'
else:
    # if we're not on a Unix-like system (!?)
    dictionary_path = os.path.join('static', 'libs', 'words')
    # and haven't already done so
    if not os.path.exists(dictionary_path):
        # let's just grab a wordlist from the internet
        urlretrieve(
            "http://www.cs.duke.edu/~ola/ap/linuxwords", dictionary_path
        )

with open(dictionary_path) as dictionary:
    WORDS = [word for word in dictionary.read().split('\n') if "'" not in word]

def romanize_sort_of(n):
    pseudo_digits = OrderedDict(
        ((100, 'C'), (50, 'L'), (10, 'X'), (5, 'V'), (1, 'I'))
    )
    suffix_segments = []
    for value, letter in pseudo_digits.items():
        factor, n = divmod(n, value)
        suffix_segments.append(factor * letter)
    return ''.join(suffix_segments)


class FinetoothUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = FinetoothUser

    username = factory.Sequence(
        lambda n: "Jennifer_Userton_{}".format(romanize_sort_of(n))
    )
    password = factory.PostGenerationMethodCall(
        'set_password', FACTORY_USER_PASSWORD
    )
    first_name = "Jennifer"
    last_name = factory.Sequence(
        lambda n: "Userton_{}".format(romanize_sort_of(n))
    )
    email = factory.Sequence(
        lambda n: "ju{}@example.com".format(n)
    )
    location = factory.Sequence(lambda n: "Place {}".format(n))
    url = "http://python.org"


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(FinetoothUserFactory)
    title = factory.Sequence(
        lambda n: "The Post About the Number {}".format(n)
    )
    slug = factory.LazyAttribute(lambda p: slugify(p.title))
    content = (
        "*Lorem Ipsum* is simply dummy text of the printing and "
        "typesetting industry. Lorem Ipsum has been the industry's standard "
        "dummy text ever since the *1500s*, when an unknown printer took a "
        "galley of type and scrambled it to make a type specimen book."
    )
    published_at = datetime.now()

class PostVoteFactory(factory.DjangoModelFactory):
    class Meta:
        model = PostVote

    post = factory.SubFactory(PostFactory)
    voter = factory.SubFactory(FinetoothUserFactory)
    value = 1
    start_index = factory.LazyAttribute(
        lambda v: random.randint(0, len(v.post.plaintext)-1)
    )
    end_index = factory.LazyAttribute(
        lambda v: random.randint(v.start_index, len(v.post.plaintext)-1)
    )

class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = Tag

    label = factory.Sequence(lambda _: random.choice(WORDS))
