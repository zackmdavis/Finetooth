import random
from math import log, ceil
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from datetime import datetime
from collections import OrderedDict

import factory

from core.models import (
    FinetoothUser, Post, Comment, PostVote, CommentVote, Tag
)

FACTORY_USER_PASSWORD = "f:O>r<5H%UsBu"

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
    content = """*Lorem Ipsum* is simply dummy text of the printing and
        typesetting industry. Lorem Ipsum has been the industry's standard
        dummy text ever since the *1500s*, when an unknown printer took a
        galley of type and scrambled it to make a type specimen book."""
    published_at = datetime.now()
