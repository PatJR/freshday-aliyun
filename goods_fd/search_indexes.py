from haystack import indexes
from goods_fd.models import GoodsSKU
"""
 创建一个索引类 Creating SearchIndexes
 创建一个SearchIndex类需要继承indexes.SearchIndex & indexes.Indexable
 还得定义get_model()方法
SearchIndex对象是Haystack确定应该在搜索索引中放置什么数据并处理数据流的方法。
您可以认为它们类似于Django模型或表单，因为它们是基于字段的，并且操作/存储数据。
我们将创建下面的GoodsSKUIndex来对应于我们的Note模型。
这段代码通常放在应用程序的search_index .py文件中，
不过这不是必需的。这允许Haystack自动获取它
"""


class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    document=True：
    每个SearchIndex都要求有一个(且只有一个)字段document=True。
    这向Haystack和搜索引擎表明，哪个字段是搜索的主要字段。
    当您选择document=True字段时，应该在所有的SearchIndex类中一致地命名它，
    以避免混淆后端。惯例是将此字段命名为text,也可以命名为其他的，例如：picked等等。
    use_template=True：
    此外，我们在 text 字段上提供了use_template=True。
    这允许我们使用数据模板(而不是容易出错的连接)来构建搜索引擎将索引的文档。
    您需要在模板目录(templates)中创建一个名为search/indexes/myapp/note_text.txt的新模板，
    并将以下内容放入其中:
    search/indexes/应用名称/索引类小写名_text.txt  ：   search/indexes/goods_fd/goodssku_text.txt
    """
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsSKU

    def index_queryset(self, using=None):
        """用于更新模型的整个索引"""
        return self.get_model().objects.all()

