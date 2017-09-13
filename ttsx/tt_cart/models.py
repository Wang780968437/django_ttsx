from django.db import models

# Create your models here.

class CartInfo(models.Model):
    #用户
    #商品
    #数量
    user=models.ForeignKey('ttsx_user.UserInfo')
    goods=models.ForeignKey('tt_goods.GoodsInfo')
    count=models.IntegerField()

    # 谁买了什么


