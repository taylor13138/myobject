#订单信息管理视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime

from myadmin.models import User,Member,Orders,OrderDetail,Payment,Shop1,Category,Product

def index(request,pIndex=1):
    ''' 浏览订单信息 '''
    umod = Orders.objects
    ulist = umod.filter(status__lt=4)
    mywhere=[]
     # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status','')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status="+status)

    ulist = ulist.order_by("-id")#对id排序
    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist,10) #以每页10条数据分页
    maxpages = page.num_pages #获取最大页数
    #判断当前页是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #获取当前页数据
    plist = page.page_range #获取页码列表信息

    for vo in list2:
            member = Member.objects.only("nickname").get(id=vo.member_id)
            shop = Shop1.objects.only("name").get(id=vo.shop_id)
            vo.membername = member.nickname
            vo.shopname = shop.name
            # product = OrderDetail.objects.only("product_id").get(order_id=vo.id)
            # cate = Product.objects.only("category_id").get(id=product.product_id)
            # category = Category.objects.only("name").get(id=cate.category_id)
            # vo.categoryname = category.name

    context = {"orderslist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/orders/list.html",context)

def insert(request):
    ''' 执行订单添加 '''
    try:
        #执行订单信息的添加
        od = Orders()
        od.shop_id = request.session['shopinfo']['id']
        od.member_id = 0
        od.user_id = request.session['webuser']['id']
        od.money = request.session['total_money']
        od.status = 1 #订单状态:1过行中/2无效/3已完成
        od.payment_status = 2 #支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        #执行支付信息添加
        op = Payment()
        op.order_id = od.id #订单id号
        op.member_id = 0
        op.type = 2
        op.bank = request.GET.get("bank",3) #收款银行渠道:1微信/2余额/3现金/4支付宝
        op.money = request.session['total_money']
        op.status = 2 #支付状态:1未支付/2已支付/3已退款
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        #执行订单详情的添加
        cartlist = request.session.get("cartlist",{}) #获取购物车中的菜品信息
        #遍历购物车中的菜品并添加到订单详情中
        for item in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id  #订单id
            ov.product_id = item['id']  #菜品id
            ov.product_name = item['name'] #菜品名称
            ov.price = item['price']     #单价
            ov.quantity = item['num']  #数量
            ov.status = 1 #状态:1正常/9删除
            ov.save()

        del request.session["cartlist"]
        del request.session['total_money']
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")

def detail(request):
    ''' 加载订单详情 '''
    oid = request.GET.get("oid",0)
    dlist = OrderDetail.objects.filter(order_id=oid)
    context = {"detaillist":dlist}
    return render(request,"web/detail.html",context)

def status(request):
    ''' 修改订单状态 '''
    try:
        oid = request.GET.get("oid",0)
        ob = Orders.objects.get(id=oid)
        ob.status = request.GET['status']
        ob.save()
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")