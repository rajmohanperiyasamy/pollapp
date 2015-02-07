from community.models import Entry

def set_answer_ratings(request):
    data = {}
    try:
        rating = request.GET.get('rating','like')
        answer = Entry.objects.get(id = request.GET['aid'])
        flg = rating
        if rating == 'like':
            try:
                if request.session['%s%s'%(flg, answer.id)] != answer.id:
                    try:
                        if request.session['dislike%s'%(answer.id)] == answer.id:
                            del request.session['dislike%s'%(answer.id)]
                            answer.rateminus = answer.rateminus - 1
                    except:pass
                    request.session['%s%s'%(flg, answer.id)] = answer.id
                    answer.rateplus = answer.rateplus + 1 
                    answer.save()
                else:
                    ####pass###
                    try:
                        if request.session['like%s'%(answer.id)] == answer.id:
                            del request.session['like%s'%(answer.id)]
                            answer.rateplus = answer.rateplus - 1
                            answer.save()
                            rating = 'relike'
                    except:
                        pass
                    
            except:
                try:
                    try:
                        if request.session['dislike%s'%(answer.id)] == answer.id:
                            del request.session['dislike%s'%(answer.id)]
                            answer.rateminus = answer.rateminus - 1
                    except:pass        
                    request.session['%s%s'%(flg,answer.id)] = answer.id 
                    answer.rateplus = answer.rateplus + 1 
                    answer.save()  
                except:
                    pass   
        else:
            try:
                if request.session['%s%s'%(flg, answer.id)] != answer.id:
                    try:
                        if request.session['like%s'%(answer.id)] == answer.id:
                            del request.session['like%s'%(answer.id)]
                            answer.rateplus = answer.rateplus - 1
                    except:pass
                    request.session['%s%s'%(flg, answer.id)] = answer.id
                    answer.rateminus = answer.rateminus + 1 
                    answer.save()
                else:
                    ####pass###
                    try:
                        if request.session['dislike%s'%(answer.id)] == answer.id:
                            del request.session['dislike%s'%(answer.id)]
                            answer.rateminus = answer.rateminus - 1
                            answer.save()
                            rating = 'redislike'
                    except:pass
            except:
                try:
                    try:
                        if request.session['like%s'%(answer.id)] == answer.id:
                            del request.session['like%s'%(answer.id)]
                            answer.rateplus = answer.rateplus - 1
                    except:pass        
                    request.session['%s%s'%(flg,answer.id)] = answer.id 
                    answer.rateminus = answer.rateminus + 1 
                    answer.save()  
                except:pass    
        status = True        
    except:status = False
    data['rating'] = rating
    data['likes'] = answer.rateplus                
    data['dislikes'] = answer.rateminus 
    data['total_count'] = answer.rateplus
    #data['total_count'] = answer.rateplus - answer.rateminus 
    data['status'] = status
    return data
