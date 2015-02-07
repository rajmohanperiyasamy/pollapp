import datetime
import getsettings
from article.models import Article


today = datetime.date.today()


def process_scheduled_arts():
    scheduled_art = Article.objects.filter(status='S', published_on__lte=today)
    scheduled_art.update(status='P')
    print "%d Articles published . . ." % (scheduled_art.count())


process_scheduled_arts()