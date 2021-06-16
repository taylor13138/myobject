#员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator   #分页功能
from myadmin.models import User    #把model类导入进来，在下面对他进行实例化   ulist = User.objects.all()
from myadmin.models import Category    #把model类导入进来，在下面对他进行实例化   ulist = User.objects.all()
from myadmin.models import Shop1    #把model类导入进来，在下面对他进行实例化   ulist = User.objects.all()
from myadmin.models import Product    #把model类导入进来，在下面对他进行实例化   ulist = User.objects.all()
from datetime import datetime
# Create your views here.

def index(request,pIndex=1):
    '''浏览信息'''
    #try:
    #获取它的实例对象
    pmod = Product.objects
    #获取它的所有信息     umod.filter(status__lt=9)意思是过滤掉状态值为9的数据
    plist = pmod.filter(status__lt=9)  # 获取所有用户信息，封装到list里面  这两句可以简写成 ulist = User.objects.all()   status__lt=9获取status小于9的所有数据
    mywhere=[]   #在下一页也能维持搜索条件  # 定义一个用于存放搜索条件列表  保证传到模板文件中后面还有这个值
    #获取并判断搜索条件
    kw = request.GET.get("keyword",None)   #获取、判断并封装关keyword键搜索
    if kw:    #Q用来代表或方法
        plist = plist.filter(name__contains=kw)  #  username__contains=kw  获取username中包含kw对应值的所以数据  的对象
        mywhere.append('keyword='+kw)  #把条件重新拼好
    #获取并判断搜索菜品类别的条件
    cid = request.GET.get("category_id", None)  # 获取、判断并封装关keyword键搜索
    if cid:  # Q用来代表或方法
        plist = plist.filter(category_id=cid)  # username__contains=kw  获取username中包含kw对应值的所以数据  的对象
        mywhere.append('category_id=' + cid)  # 把条件重新拼好

        # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        plist = plist.filter(status=status)
        mywhere.append("status=" + status)

    #执行分页处理
    pIndex = int(pIndex)   #保证页码是整形的  pIndex就是页数  当前页
    page = Paginator(plist,10)   #获取一个page对象，   5条数据为一页，实例化分页对象  page相当于是带分页格式的ulist对象
    maxpages = page.num_pages   #获取最大页码数
    #判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)   #执行分页操作，接收我们的页数信息   获取当前页数据 获取page对象的当前页的对象  page.page(pIndex)第一个page是对象，第二个page（）是固定方法，pIndex是方法运算需要的变量
    plist = page.page_range    #获取页码列表信息 范围  方便输出页码数据 知道有多少个页码
    for vo in list2:        #在list2里不断输出category表中的shop_id，找到和Shop1实例化对象一样的值，放到sob中，sob这条数据的name属性就获得了，找到在vo中追加出来的shopname属性放到index.html中可以循环输出
        sob = Shop1.objects.get(id=vo.shop_id)    #跨表查询，并且封装好，对另外表的name 汉字
        vo.shopname = sob.name
        cob = Category.objects.get(id=vo.category_id)
        vo.categoryname = cob.name
    context = {"productlist": list2, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages, 'mywhere':mywhere}  # 把这些数据ulist放到userlist里面  成为一个字典   把这些数据ulist封装一下，封装后的名字叫userlist,把mywhere送到模板中去
    return render(request, "myadmin/product/index.html", context)  # 加载模板(返回一个模板)  因为index。html能用到这些信息，所以把它封装成一个context(就是把查询出来的数据扔进去)放进去
    #except:
        #return HttpResponse("没有找到用户信息！")

def add(request):
    '''加载信息添加表单'''
    svo = Shop1.objects.values('id','name') #实例化Shop1表中的字段 id 和 name，因为需要用到另一个表的id和表名，所以引入
    context = {'shoplist': svo}    #把获取到的数据封装成对象，放到add.html里
    # cvo = Category.objects.values('id', 'name')  # 实例化Shop1表中的字段 id 和 name，因为需要用到另一个表的id和表名，所以引入
    # context['categorylist'] = cvo
    return render(request,"myadmin/product/add.html",context)

def insert(request):
    '''执行信息添加'''
    try:
        ob = Product()    #把User这个模型（表）实例化出来，成为一个对象ob
        #从用post的方式从表单中获取信息  并封装到ob对象中
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()  #执行保存操作
        context = {'info': "添加成功！"}   #存储一个成功的信息
    except Exception as err:
        print(err)
        context = {'info': "添加失败！"}   #塞一个失败的信息   因为在myadmin/info.html模板中会用到context，所有把context也放进去（render中）（以字典形式）
    return render(request,"myadmin/info.html",context)

def delete(request,pid=0):
    '''执行信息删除'''
    try:
        ob = Product.objects.get(id=pid) #这个删除其实是一个修改操作，修改状态为9，过滤掉。  获取到要修改的对象的数据信息
        ob.status = 9   #ulist = umod.filter(status__lt=9)已经过滤掉了状态大于等于9的数据，只剩下小于9的数据
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()  # 执行保存操作
        context = {'info': "删除成功！"}  # 存储一个成功的信息
    except Exception as err:
        print(err)
        context = {'info': "删除失败！"}  # 塞一个失败的信息   因为在myadmin/info.html模板中会用到context，所有把context也放进去（render中）（以字典形式）
    return render(request, "myadmin/info.html", context)

def edit(request,pid=0):
    '''加载信息编辑表单'''
    try:
        ob = Product.objects.get(id=pid)  # 这个删除其实是一个修改操作，修改状态为9，过滤掉。  获取到要修改的对象的数据信息
        context = {'product': ob}  #把ob获取到的信息封装成context，取名叫user,方便edit.html里面用
        svo = Shop1.objects.values('id', 'name')  # 实例化Shop1表中的字段 id 和 name，因为需要用到另一个表的id和表名，所以引入
        context["shoplist"] = svo
        # cvo = Category.objects.values('id', 'name')  # 实例化Shop1表中的字段 id 和 name，因为需要用到另一个表的id和表名，所以引入
        # context['categorylist'] = cvo
        return render(request,"myadmin/product/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info': "没有找到要修改的信息！"}  # 塞一个失败的信息   因为在myadmin/info.html模板中会用到context，所有把context也放进去（render中）（以字典形式）
        return render(request, "myadmin/info.html", context)

def update(request,pid):
    '''执行信息编辑'''
    try:
        # uid = request.POST['id']  # 获取要修改数据的id
        ob = Product.objects.get(id=pid)  # 获取这条数据的实例化
        # 从表单中获取要添加的信息并封装到ob对象中
        ob.name = request.POST['name']
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.price = request.POST['price']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()  # 执行保存
        context = {"info": "修改成功！"}  # 提供一个info的信息，封装成一个context
    except Exception as err:
        print(err)
        context = {"info": "修改失败！"}
    return render(request, "myadmin/info.html", context)