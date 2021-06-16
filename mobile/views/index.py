from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import Member,Shop1,Category,Product
from myadmin.models import Orders,OrderDetail,Payment
from datetime import datetime
# Create your views here.

def index(request):
    '''移动端首页'''
    #获取并判断当前店铺信息
    shopinfo = request.session.get("shopinfo",None)  #获取session中shopinfo的值，如果没有就默认为none
    if shopinfo is None:
        return redirect(reverse("mobile_shop"))    #重定向到店铺选择页
    #获取当前店铺下的菜品类别和菜品信息
    # ob = Category.objects.get(shop_id=request.session.shopinfo.id)
    clist = Category.objects.filter(shop_id=shopinfo['id'],status=1)  #遍历shop id得到对应店铺所有菜的类别
    productlist = dict()    #定义一个字典列表   把菜和类别封装到里面去
    for vo in clist:
        plist = Product.objects.filter(category_id=vo.id,status=1)    #遍历 category中的id得到对应菜类别的所有菜
        productlist[vo.id] = plist  #把菜品一个一个放进菜品信息列表，每个菜系对应的几道菜品信息，   拿到的是一组一组的菜品，是以菜品类别的id塞进去的，形成了键值对，中餐：{包子，豆浆，油条}
    context = {'categotylist':clist,'productlist':productlist.items(),'cid':clist[0]}  #开始拼装数据,放到一个变量中去    productlist = dict()  字典的数据需要加items()，不然在后面没法进行for in的循环,  cid获取clist中的第一条数据
    return render(request,"mobile/index.html",context)

def register(request):
    '''移动端会员注册/登录表单'''
    return render(request,"mobile/register.html")

def doRegister(request):
    '''执行会员注册/登录'''
    # return render(request,"mobile/index.html")
    try:
        # 执行验证码的校验
        if request.POST['code'] != request.session['verifycode']:
            context = {"info": "验证码错误！"}
            return render(request, 'mobile/register.html', context)  # 如果不相同就返回了，相同自动运行下面代码，不需要else

        # 获取它的model对象，并执行get查询，get获取的是单条数据，可能拿到，也可能拿不到，    拿到了我们这个用户对象,通过request.POST.get['username']获取到用户在login页面输入的username信息，看model对象中是否存在这个username信息，判断账号是否存在
        user = Member.objects.get(mobile=request.POST['mobile'])
        # 判断当前用户是否是管理员
        if user.status == 1:
            # 判断登录密码是否相同
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['password'] + user.password_salt  # 从表单中获取密码并添加user对象表中的干扰值
            md5.update(s.encode('utf-8'))  # 将要产生md5的子串放进去
            if user.password_hash == md5.hexdigest():  # 获取md5值  判断和表中的md5值是否相同
                print("登陆成功")
                # 将当前登陆成功的用户信息以adminuser为key写入到session中  session中只能接收字典格式   浏览器每一次请求时，会塞一个cookie值，cookie中有sessionid号，服务器通过数据库取出来
                request.session['mobileuser'] = user.toDict()  # 服务器通过请求过来的key,去数据库查找session_data，如果已添加，就放行，还没添加就自动拦截到登录页。  request.session['adminuser']  session是可以通过request获取的
                # 重定向到后台管理首页
                return redirect(reverse("mobile_index"))
            else:
                context = {"info": "登录密码错误！"}
        else:
            context = {"info": "无效的登录账号！"}
        # 通过post方式获取到表单中提交的密码
    except Exception as err:
        print(err)
        context = {"info": "登录账号不存在"}
    return render(request, 'mobile/register.html', context)  # 需要放context的直接用return render

def shop(request):
    '''移动端选择店铺页面'''
    context = {"shoplist":Shop1.objects.filter(status=1)}  #获取当前正常的店铺信息，一shoplist的名字放到shop.html中
    return render(request,"mobile/shop.html",context)

def selectShop(request):
    '''执行移动端店铺选择操作'''
    #获取选择的店铺信息，并放置到session中
    ob = Shop1.objects.get(id=request.GET['sid'])
    request.session['shopinfo'] = ob.toDict()     #退出时这个session其实也可以删掉
    request.session['cartlist'] = {}   #切换店铺，进行购物车清空操作
    # 跳转到首页
    return redirect(reverse("mobile_index"))

def addOrders(request):
    '''移动端下单表单页'''
    # 尝试从session中获取名字为cartlist的购物车信息，若没有返回{}
    cartlist = request.session.get('cartlist', {})
    total_money = 0  # 初始化一个总金额
    # 遍历购物车中的菜品并累加总金额
    for vo in cartlist.values():
        total_money += vo['num'] * vo['price']
    request.session['total_money'] = total_money  # 放进session
    return render(request,"mobile/addOrders.html")

def doAddOrders(request):
    ''' 执行订单添加操作 '''
    try:
        #执行订单信息的添加
        od = Orders()
        od.shop_id = request.session['shopinfo']['id']
        od.member_id = request.session['mobileuser']['id']
        od.user_id = 0
        od.money = request.session['total_money']
        od.status = 1 #订单状态:1过行中/2无效/3已完成
        od.payment_status = 2 #支付状态:1未支付/2已支付/3已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        #执行支付信息添加
        op = Payment()
        op.order_id = od.id #订单id号
        op.member_id = request.session['mobileuser']['id']
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
    except Exception as err:
        print(err)
    return render(request,"mobile/orderinfo.html",{"order":od})

# 输出验证码
def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
