from django.contrib import admin
from goods_fd.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexGoodsTypeBanner, GoodsSKU, Goods, \
    GoodsImage
from django.core.cache import cache


# Register your models here.


class BaseModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """新增或更新表中的数据时调用"""
        super().save_model(request, obj, form, change)

        # 发出任务，让celery worker重新生成首页静态页面
        from goods_fd.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首恶的缓存数据
        cache.delete('index_page_data')
        print(cache.get('index_page_data'))
    def delete_model(self, request, obj):
        """删除表中的数据时调用"""
        super().delete_model(request, obj)
        # 发出任务让celery worker 重新生成首页静态页面
        from goods_fd.tasks import generate_static_index_html
        generate_static_index_html.delay()

        # 清除首页的缓存数据
        cache.delete('index_page_data')
        print(cache.get('index_page_data'))

class GoodsTypeAdmin(BaseModelAdmin):
    pass


class IndexGoodsBannerAdmin(BaseModelAdmin):
    pass


class IndexGoodsTypeBannerAdmin(BaseModelAdmin):
    pass


class IndexPromotionBannerAdmin(BaseModelAdmin):
    pass


class GoodsSKUAdmin(BaseModelAdmin):
    pass


class GoodsAdmin(BaseModelAdmin):
    pass


class GoodsImageAdmin(BaseModelAdmin):
    pass


admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(IndexGoodsBanner, IndexGoodsBannerAdmin)
admin.site.register(IndexGoodsTypeBanner, IndexGoodsTypeBannerAdmin)
admin.site.register(IndexPromotionBanner, IndexPromotionBannerAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsSKU, GoodsSKUAdmin)
admin.site.register(GoodsImage, GoodsImageAdmin)
