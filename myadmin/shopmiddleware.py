#自定义中间类（执行是否登录判断）需要导入这些东西
from django.shortcuts import redirect
from django.urls import reverse
import re

class ShopMiddleware:
    def __init__(self, get_response):   # 程序最开始启动时才会被调用 类似于java中的初始化
        self.get_response = get_response
        print("ShopMiddleware")

    def __call__(self, request):    #每次请求这个方法都会被执行
        path = request.path     #获取用户要访问的url路径
        print("url:",path)

        #判断管理后台是否登录
        #定义后台不登录也可直接访问的url列表
        urllist = ['/myadmin/login','/myadmin/logout','/myadmin/dologin','/myadmin/verify']
        #判断当前请求url地址是否是以/myadmin开头,并且不在urllist中，才做是否登录判断
        if re.match(r'^/myadmin',path) and (path not in urllist):      #正则判断
            #判断是否登录(在于session中没有adminuser  这个字典数据)  代表没有登录
            if 'adminuser' not in request.session:
                #重定向到登录页   redirect重定向  reverse反向解析
                return redirect(reverse("myadmin_login"))
                #pass

        #判断大堂点餐请求的判断，判断是否登录（session中是否有webuser）
        if re.match(r'^/web',path):
            #判断是否登录(在于session中没有webuser)
            if 'webuser' not in request.session:
                #重定向到登录页
                return redirect(reverse("web_login"))

        #判断移动端是否登录
        #定义移动端不登录也可直接访问的url列表
        urllist = ['/mobile/register','/mobile/doregister']
        #判断当前请求url地址是否是以/mobile开头,并且不在urllist中，才做是否登录判断
        if re.match(r'^/mobile',path) and (path not in urllist):      #正则判断
            #判断是否登录(在于session中没有mobileuser  这个字典数据)  代表没有登录
            if 'mobileuser' not in request.session:
                #重定向到登录页   redirect重定向  reverse反向解析
                return redirect(reverse("mobile_register"))


        response = self.get_response(request)    #后两句是放行  允许通过的意思
        # Code to be executed for each request/response after
        # the view is called.
        return response