"""新闻模型"""
from plugins.private.orm import Common, db


class NewsColumn(Common, db.Model):
    """新闻栏目
    一级分类:新闻板块
    二级分类:新闻栏目
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自动编号')
    name = db.Column(db.String(length=10), nullable=False, comment='栏目名/板块名')
    icon = db.Column(db.String(length=255), default='', comment='栏目图标')
    introduction = db.Column(db.String(length=255), default='', comment='栏目/板块 简介')
    grade = db.Column(db.SMALLINT, nullable=False, comment='类型等级.1:一级,2:二级')
    superior_id = db.Column(db.Integer, db.ForeignKey('news_column.id', ondelete='CASCADE'), comment='上级类型')

    __table_args__ = (
        db.UniqueConstraint('name', 'superior_id', name='uix_name_superior'),
        db.Index('ix_name_superior_type', 'name', 'superior_id'),
    )
    superior = db.relationship('NewsColumn', lazy='select', backref=db.backref('subordinate', cascade='all,delete'),
                               remote_side=id)

    def _serialization(self):
        """自定义序列化,满足前端特定需求
        去除id,改为index字段
        """
        result = self.serialization(remove={'id', 'create_time'})
        result['index'] = self.id
        return result

    def subordinates(self):
        """获取所有子集"""
        superior = {**self._serialization(), 'children': []}

        for subordinate in self.subordinate:
            superior['children'].append(subordinate.subordinates())
        return superior

    def column_num(self, result: dict, *args, **kwargs):
        """序列化数据,添加版块下栏目的数量并返回"""
        column_num = NewsColumn.query.filter_by(superior_id=self.id).count()  # 获取板块下栏目数量
        result.update({'column_num': column_num})

    def news_num(self, result: dict, *args, **kwargs):
        """序列化数据,添加栏目下新闻的数量并返回"""
        news_num = NewsColumnNews.query.filter_by(column_id=self.id).count()  # 获取栏目下新闻的数量
        plate = NewsColumn.query.filter_by(id=self.superior_id).first_or_404()  # 获取栏目对应的父板块名
        result.update({'news_num': news_num, 'plate_name': plate.name})


class NewsColumnNews(Common, db.Model):
    """新闻专栏的新闻
    """
    news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete='CASCADE'), nullable=False, comment='新闻id')
    column_id = db.Column(db.Integer, db.ForeignKey('news_column.id', ondelete='CASCADE'), nullable=False,
                          comment='栏目id')
    sort = db.Column(db.SMALLINT, default=0, comment='新闻排序')
    top = db.Column(db.SMALLINT, default=0, comment='新闻置顶')
    release = db.Column(db.SMALLINT, default=1, comment='新闻是否显示')
    recommend = db.Column(db.SMALLINT, default=0, comment='栏目推荐')

    news = db.relationship('News', cascade='all,delete')
    news_column = db.relationship('NewsColumn', cascade='all,delete')

    def news_info(self, result: dict, *args, **kwargs):
        """完善栏目新闻置顶排序等信息"""
        remove = set()
        if kwargs.get('remove'):
            remove = remove | kwargs.get('remove')
            kwargs.pop('remove')
        result.update({'news_info': self.news.serialization(remove=remove, **kwargs)})

    def column_info(self, result: dict, *args: tuple, **kwargs: dict):
        """完善新闻栏目信息"""
        remove = {'introduction', 'grade', 'icon', 'create_time'}
        result.update({'column_info': self.news_column.serialization(remove=remove)})


class NewsTag(Common, db.Model):
    """新闻标签"""

    name = db.Column(db.String(length=10), nullable=False, unique=True, comment='标签名')
    description = db.Column(db.String(length=100), default='', comment='标签描述')


class News(Common, db.Model):
    """新闻"""

    title = db.Column(db.String(length=255), nullable=False, comment='新闻标题')
    introduction = db.Column(db.String(length=255), default='', comment='新闻简介')
    creator = db.Column(db.String(length=16), default='', comment='编辑者/创建者')
    source = db.Column(db.String(length=255), default='', comment='新闻来源')
    source_logo = db.Column(db.String(length=255), default='', comment='新闻来源图标')
    seo_title = db.Column(db.String(length=255), default='', comment='seo标题')
    cover = db.Column(db.String(length=255), default='', comment='新闻封面图')
    content = db.Column(db.Text, comment='新闻内容')
    original = db.Column(db.SMALLINT, nullable=False, default=1, comment='是否原创.1:是,2:否')

    _tags = db.relationship('NewsTagsRelation', foreign_keys='NewsTagsRelation.news_id')

    def tags(self):
        """新闻所有标签关系"""
        tags_id = [item.tag_id for item in self._tags]
        self.all_tag = NewsTag.query.filter(NewsTag.id.in_(tags_id)).all()
        return self.all_tag

    @property
    def get_tags(self):
        """获取全部标签"""
        if getattr(self, 'all_tag', None):
            return self.all_tag
        else:
            return self.tags()

    def tags_info(self, result: dict, args: tuple = None, kwargs: dict = None):
        """标签详情"""
        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = dict()
        result['tags_info'] = [{'tag_name': item.name, 'id': item.id} for item in self.get_tags]


class NewsTagsRelation(Common, db.Model):
    """新闻标签关系"""

    news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete='CASCADE'), nullable=False, comment='新闻id')
    tag_id = db.Column(db.Integer, db.ForeignKey('news_tag.id', ondelete='CASCADE'), nullable=False, comment='标签id')

    tag = db.relationship('NewsTag', foreign_keys=[tag_id])
