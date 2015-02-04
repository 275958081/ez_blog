from redis_accessor import get_safe_redis
from django.http import HttpResponse






def get_visitor_ip(req):
    if req.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  req.META['HTTP_X_FORWARDED_FOR']
    else :
        ip = req.META['REMOTE_ADDR']
    return ip



def is_bad_ip(str_ip):
    if len(str_ip)  < 6 or  len(str_ip) > 18 :
        return True


def add_to_attacker_list(ip):
    r = get_safe_redis()
    r.sadd('ATTACKER_LIST',ip)
    r.save()


def is_atttcker(ip):
    r = get_safe_redis()
    return r.sismember('ATTACKER_LIST',ip)



def try_login(req):
       name = req.POST.get('name')
       password = req.POST.get('password')
       visitor_ip = get_visitor_ip(req)
       if ( is_atttcker( visitor_ip )) :
           return 0
       key = 'TRY_LOGIN_IP_' + visitor_ip
       r = get_safe_redis()

       if r.get(key) != None :
          if (  int(r.get(key)) >= 5 ) :
              r.save()
              add_to_attacker_list(visitor_ip)
              return 0
       if name =='leepeng' and password =='lee928928' :
          r.set(key,0)
          req.session['lp_login'] = True
          req.session.set_expiry( 5 * 60 )
          r.save()
          return  9527
       else :
           leave_times = 5 - 5-r.incr(key);
           r.save()
           return leave_times
    
