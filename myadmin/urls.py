# 后台管理的子路由文件
from django.urls import path
from myadmin.views import index
from myadmin.views import user    #需要先导入用到的视图文件
from myadmin.views import shop
from myadmin.views import category
from myadmin.views import product
from myadmin.views import member,orders
urlpatterns = [
    path('', index.index, name="myadmin_index"),  #后台首页

    #后台管理员登录、退出路由
    path('login', index.login, name="myadmin_login"),  #加载登录表单
    path('dologin', index.dologin, name="myadmin_dologin"),  #执行登录
    path('logout', index.logout, name="myadmin_logout"),  #退出
    path('verify', index.verify, name="myadmin_verify"),  #输出验证码

    #员工信息管理路由
    path('user/<int:pIndex>', user.index, name="myadmin_user_index"), #浏览  需要赋值当前页码pIndex为1
    path('user/add', user.add, name="myadmin_user_add"), #添加表单
    path('user/insert', user.insert, name="myadmin_user_insert"), #执行添加
    path('user/del/<int:uid>', user.delete, name="myadmin_user_delete"), #执行删除
    path('user/edit/<int:uid>', user.edit, name="myadmin_user_edit"), #加载编辑表单
    path('user/update/<int:uid>', user.update, name="myadmin_user_update"), #执行编辑

    #订餐日期管理路由
    path('shop/<int:pIndex>', shop.index, name="myadmin_shop_index"), #浏览  需要赋值当前页码pIndex为1
    path('shop/add', shop.add, name="myadmin_shop_add"), #添加表单
    path('shop/insert', shop.insert, name="myadmin_shop_insert"), #执行添加
    path('shop/del/<int:sid>', shop.delete, name="myadmin_shop_delete"), #执行删除
    path('shop/edit/<int:sid>', shop.edit, name="myadmin_shop_edit"), #加载编辑表单
    path('shop/update/<int:sid>', shop.update, name="myadmin_shop_update"), #执行编辑

    #早中晚餐信息管理路由
    path('category/<int:pIndex>', category.index, name="myadmin_category_index"), #浏览  需要赋值当前页码pIndex为1
    path('category/load/<int:sid>', category.loadCategory, name="myadmin_category_load"),  #用ajax响应的加载
    path('category/add', category.add, name="myadmin_category_add"), #添加表单
    path('category/insert', category.insert, name="myadmin_category_insert"), #执行添加
    path('category/del/<int:cid>', category.delete, name="myadmin_category_delete"), #执行删除
    path('category/edit/<int:cid>', category.edit, name="myadmin_category_edit"), #加载编辑表单
    path('category/update/<int:cid>', category.update, name="myadmin_category_update"), #执行编辑

    #菜品信息管理路由
    path('product/<int:pIndex>', product.index, name="myadmin_product_index"), #浏览  需要赋值当前页码pIndex为1
    path('product/add', product.add, name="myadmin_product_add"), #添加表单
    path('product/insert', product.insert, name="myadmin_product_insert"), #执行添加
    path('product/del/<int:pid>', product.delete, name="myadmin_product_delete"), #执行删除
    path('product/edit/<int:pid>', product.edit, name="myadmin_product_edit"), #加载编辑表单
    path('product/update/<int:pid>', product.update, name="myadmin_product_update"), #执行编辑

    #会员信息管理路由
    path('member/<int:pIndex>', member.index, name="myadmin_member_index"), #浏览  需要赋值当前页码pIndex为1

    #订单处理路由
    path('orders/<int:pIndex>', orders.index, name="myadmin_orders_index"), #订单浏览
    path('orders/insert', orders.insert, name="myadmin_orders_insert"), #执行订单添加
    path('orders/detail', orders.detail, name="myadmin_orders_detail"), #订单详情
    path('orders/status', orders.status, name="myadmin_orders_status"), #修改订单状态

]