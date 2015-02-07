

import getsettings
from movies.models import Movies


def update_deactivated_movies():
    Movies.objects.filter(status='N').update(status='B')
    return True

update_deactivated_movies()