from django.db.models import Q
from movies.models import Movies, MovieTime, ShowTime

def get_suggested_movies(request):
    send_data = []
    fetched_values = ['title','slug']
    movie_type = request.REQUEST.get('mtype','all') 
    if movie_type == 'all':
        try:
            q=request.POST['query']
            q_key=(Q(title__icontains=q)|Q(synopsis__icontains=q))
            movies = Movies.objects.only(*fetched_values).filter(q_key,status='P').distinct()[:10]
        except:
            movies = Movies.objects.only(*fetched_values).filter(status='P').order_by('title','-release_date')[:10]
    else:
        show_times = ShowTime.objects.distinct('movietime')
        movie_times = MovieTime.objects.filter(id__in = [st.movietime.id for st in show_times]).distinct('movie')
        movies = Movies.objects.only(*fetched_values).filter(id__in = [mt.movie.id for mt in movie_times], status = 'P').order_by('-release_date')[:10]
    
    for movie in movies :
        movie_info = {'id':movie.id,'name':movie.title}
        send_data.append(movie_info)
    
    return send_data 