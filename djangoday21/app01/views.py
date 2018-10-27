from django.shortcuts import render,HttpResponse,redirect

# Create your views here.

from django.core.handlers.wsgi import WSGIRequest
# def index(request):
#
#     # print(request.environ)  封装了所有用户请求信息
#     # for k,y in request.environ.items():
#     #     print(k,y)
#     # print(request.environ['HTTP_USER_AGENT'])
#     return HttpResponse('ok')

from utils import pagination


USER_LIST=[]
for i in range(500):
    USER_LIST.append(i)
def tpl1(request):
    return render(request,'tpl1.html')
def tpl2(request):
    return render(request,'tpl2.html')
def tpl3(request):
    return render(request,'tpl3.html')
def tpl4(request):
    return  render(request,'tpl4.html')
def user_list(request):
    current_page=request.GET.get('p',1)
    current_page=int(current_page)

    a=request.COOKIES.get('per_page_count',10)
    a=int(a)
    page_obj=pagination.Page(current_page,len(USER_LIST),a)
    start=page_obj.start
    end=page_obj.end
    data = USER_LIST[start:end]
    count=page_obj.all_count
    page_str=page_obj.page_str('user_list')
    return render(request,'user_list.html',{'user_list':data,'page_str':page_str})










######################## cookie ########################


user_info={
    "dachengzi":{"pwd":"123123"},
    "dajuzi":{"pwd":"asdasd"},
}
def auth(func):
    def inner(request,*args,**kwargs):
        v = request.COOKIES.get('username111')
        if not v:
            return redirect('/login/')
        return func(request,*args,**kwargs)
    return inner
from django import views
from django.utils.decorators import method_decorator

@method_decorator(auth,name='dispatch')
class Order(views.View):

    # @method_decorator(auth)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(Order,self).dispatch( request, *args, **kwargs)

    # @method_decorator(auth)
    def get(self,request,*args,**kwargs):
        v = request.COOKIES.get('username111')
        return render(request, 'index.html', {'user': v})

    # @method_decorator(auth)
    def post(self,request,*args,**kwargs):
        pass

def login(request):
    if request.method=='GET':
        return render(request,'login.html')
    elif request.method=='POST':
        u=request.POST.get('username')
        p=request.POST.get('pwd')
        user=user_info.get(u)

        if not user:

            return redirect('/login/')

        if user['pwd']==p:
            import  datetime
            time=datetime.datetime.utcnow()

            time=time+datetime.timedelta(seconds=5)

            res=redirect('/index/')
            res.set_cookie("username111",u,expires=time)
            # res.set_signed_cookie("username111",u,expires=time,salt='asd')#加密盐
            return res
@auth
def index(request):
    v=request.COOKIES.get('username111')
    # v=request.get_signed_cookie('username111',salt='asd')#解密盐

    return render(request,'index.html',{'user':v})



def cookie():
    #设置cookie
    res = redirect('/index/')
    res.set_cookie("username111", "value")
    return res
    #获取
    # v = request.COOKIES.get('username111')
    # v = request.COOKIES['username111']
    #设置cookie，等N秒后过期
    # res = redirect('/index/')
    # res.set_cookie("username111", "value",max_age=10)
    # return res
    # 设置cookie，截至N秒后过期
    # import datetime
    # time = datetime.datetime.utcnow()
    #
    # time = time + datetime.timedelta(seconds=5)
    #
    # res = redirect('/index/')
    # res.set_cookie("username111", u, expires=time)
    # return res
