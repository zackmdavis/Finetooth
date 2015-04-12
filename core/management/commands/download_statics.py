import os
from urllib.request import urlretrieve

from django.core.management.base import BaseCommand, CommandError

our_statics = {
    'jquery-2.1.1.min.js': "https://code.jquery.com/jquery-2.1.1.min.js",
    'underscore-min.js': (
        "https://cdnjs.cloudflare.com/ajax/libs/"
        "underscore.js/1.7.0/underscore-min.js"),
    os.path.join('css', "bootstrap.min.css"): (
        "https://netdna.bootstrapcdn.com/bootstrap/3.2.0/css/"
        "bootstrap.min.css"),
    os.path.join('fonts', "glyphicons-halflings-regular.woff"): (
        "https://netdna.bootstrapcdn.com/bootstrap/3.2.0/fonts/"
        "glyphicons-halflings-regular.woff"),
    os.path.join('fonts', "glyphicons-halflings-regular.ttf"): (
        "https://netdna.bootstrapcdn.com/bootstrap/3.2.0/fonts/"
        "glyphicons-halflings-regular.ttf"),
    'words': "http://www.cs.duke.edu/~ola/ap/linuxwords"
}

class Command(BaseCommand):

    def handle(self, *args, **options):
        for static, upstream in our_statics.items():
            destination = os.path.join('static', 'libs', static)
            if not os.path.exists(destination):
                self.stdout.write("downloading {} from {} ...".format(
                    destination, upstream))
                urlretrieve(upstream, destination)
            else:
                self.stdout.write("we already have {}".format(static))
