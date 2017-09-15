from django.db import models

# Create your models here.

class OrderInfo(models.Model):
    # 订单编号
    oid = models.CharField(max_length=20,primary_key=True)
    # 订单用户,来自用户信息表
    user = models.ForeignKey('ttsx_user.UserInfo')
    # 下单日期
    odate = models.DateTimeField(auto_now_add=True)
    # 是否支付
    oIsPay = models.BooleanField(default=False)
    # 金额总计
    ototal = models.DecimalField(max_digits=6,decimal_places=2)
    # 获取地址
    oaddress = models.CharField(max_length=150)


class OrderDetailInfo(models.Model):
    # 商品
    goods = models.ForeignKey('tt_goods.GoodsInfo')
    # 订单
    order = models.ForeignKey(OrderInfo)
    # 价格
    price= models.DecimalField(max_digits=5,decimal_places=2)
    # 数量
    count = models.IntegerField()