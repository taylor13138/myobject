#员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator   #分页功能
from myadmin.models import User    #把model类导入进来，在下面对他进行实例化   ulist = User.objects.all()
from django.db.models import Q
from datetime import datetime
# Create your views here.

def index(request,pIndex=1):
    '''浏览信息'''
    #try:
    #获取它的实例对象
    umod = User.objects
    #获取它的所有信息     umod.filter(status__lt=9)意思是过滤掉状态值为9的数据
    ulist = umod.filter(status__lt=9)  # 获取所有用户信息，封装到list里面  这两句可以简写成 ulist = User.objects.all()   status__lt=9获取status小于9的所有数据
    mywhere=[]   #在下一页也能维持搜索条件  # 定义一个用于存放搜索条件列表  保证传到模板文件中后面还有这个值
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)   #获取、判断并封装关keyword键搜索
    if kw:    #Q用来代表或方法
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))  #  username__contains=kw  获取username中包含kw对应值的所以数据  的对象
        mywhere.append('keyword='+kw)  #把条件重新拼好

        # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status=" + status)

    #执行分页处理
    pIndex = int(pIndex)   #保证页码是整形的  pIndex就是页数  当前页
    page = Paginator(ulist,5)   #获取一个page对象，   5条数据为一页，实例化分页对象
    maxpages = page.num_pages   #获取最大页码数
    #判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)   #执行分页操作，接收我们的页数信息   获取当前页数据 获取page对象的当前页的对象  page.page(pIndex)第一个page是对象，第二个page（）是固定方法，pIndex是方法运算需要的变量
    plist = page.page_range    #获取页码列表信息 范围  方便输出页码数据 知道有多少个页码
    context = {"userlist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere':mywhere}  # 把这些数据ulist放到userlist里面  成为一个字典   把这些数据ulist封装一下，封装后的名字叫userlist,把mywhere送到模板中去
    return render(request, "myadmin/user/index.html", context)  # 加载模板(返回一个模板)  因为index。html能用到这些信息，所以把它封装成一个context(就是把查询出来的数据扔进去)放进去
    #except:
        #return HttpResponse("没有找到用户信息！")

def add(request):
    '''加载信息添加表单'''
    return render(request,"myadmin/user/add.html")

def insert(request):
    '''执行信息添加'''
    try:
        ob = User()    #把User这个模型（表）实例化出来，成为一个对象ob
        #从用post的方式从表单中获取信息  并封装到ob对象中
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']
        #对密码进行md5加密，并且进行加盐   # 将当前员工信息的密码做md5处理
        import hashlib, random
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password'] + str(n)  # 从表单中获取密码并添加干扰值
        md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
        ob.password_hash = md5.hexdigest()  # 获取md5值
        ob.password_salt = n

        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()  #执行保存操作
        context = {'info': "添加成功！"}   #存储一个成功的信息
    except Exception as err:
        print(err)
        context = {'info': "添加失败！"}   #塞一个失败的信息   因为在myadmin/info.html模板中会用到context，所有把context也放进去（render中）（以字典形式）
    return render(request,"myadmin/info.html",context)

def delete(request,uid=0):
    '''执行信息删除'''
    try:
        ob = User.objects.get(id=uid) #这个删除其实是一个修改操作，修改状态为9，过滤掉。  获取到要修改的对象的数据信息
        ob.status = 9   #ulist = umod.filter(status__lt=9)已经过滤掉了状态大于等于9的数据，只剩下小于9的数据
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()  # 执行保存操作
        context = {'info': "删除成功！"}  # 存储一个成功的信息
    except Exception as err:
        print(err)
        context = {'info': "删除失败！"}  # 塞一个失败的信息   因为在myadmin/info.html模板中会用到context，所有把context也放进去（render中）（以字典形式）
    return render(request, "myadmin/info.html", context)

def edit(request,uid=0):
    '''加载信息编辑表单'''
    try:
        ob = User.objects.get(id=uid)  # 这个删除其实是一个修改操作，修改状态为9，过滤掉。  获取到要修改的对象的数据信息
        context = {'user': ob}  #把ob获取到的信息封装成context，取名叫user,方便edit.html里面用
        return render(request,"myadmin/user/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！"}  # 塞一个失败的信息   因为在myadmin/info.html模板中会用到context，所有把context也放进去（render中）（以字典形式）
        return render(request, "myadmin/info.html", context)

def update(request,uid):
    '''执行信息编辑'''
    try:
        # uid = request.POST['id']  # 获取要修改数据的id
        ob = User.objects.get(id=uid)  # 获取这条数据的实例化
        # 从表单中获取要添加的信息并封装到ob对象中
        ob.status = request.POST['status']
        ob.nickname = request.POST['nickname']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()  # 执行保存
        context = {"info": "修改成功！"}  # 提供一个info的信息，封装成一个context
    except Exception as err:
        print(err)
        context = {"info": "修改失败！"}
    return render(request, "myadmin/info.html", context)