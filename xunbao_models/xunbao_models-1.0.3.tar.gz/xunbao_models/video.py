"""视频模型"""
from plugins.private.orm import Common, db


class VideoColumn(Common, db.Model):
    """视频栏目
    一级分类:视频板块
    二级分类:视频栏目
    """
    name = db.Column(db.String(length=10), nullable=False, comment='栏目名/板块名')
    icon = db.Column(db.String(length=255), default='', comment='栏目图标')
    introduction = db.Column(db.String(length=255), default='', comment='栏目/板块 简介')
    grade = db.Column(db.SMALLINT, nullable=False, comment='类型等级.1:一级,2:二级')
    superior_id = db.Column(db.Integer, db.ForeignKey('video_column.id', ondelete='CASCADE'), comment='上级类型')

    superior = db.relationship('VideoColumn', cascade='all,delete')

    __table_args__ = (
        db.UniqueConstraint('name', 'superior_id', name='uix_name_superior'),
        db.Index('ix_name_superior_type', 'name', 'superior_id'),
    )

    def column_num(self, result: dict, args: tuple = None, kwargs: dict = None):
        """序列化数据,自定义序列化,满足前端特定需求,添加版块下栏目的数量并返回"""
        column_num = VideoColumn.query.filter_by(superior_id=self.id).count()  # 获取板块下栏目数量
        result.update({'column_num': column_num})
        return result

    def video_num(self, result: dict, args: tuple = None, kwargs: dict = None):
        """序列化数据添加->视频计数"""
        video_num = VideoColumnVideo.query.filter_by(column_id=self.id).count()  # 获取栏目下视频的数量
        result.update({'video_num': video_num})

    def plate_name(self, result: dict, args: tuple = None, kwargs: dict = None):
        """序列化数据添加->板块名"""
        if self.superior_id:
            plate = VideoColumn.query.filter_by(id=self.superior_id).first_or_404()  # 获取栏目对应的父板块名
            result.update({'plate_name': plate.name})


class VideoColumnVideo(Common, db.Model):
    """视频专栏的视频
    """
    video_id = db.Column(db.Integer, db.ForeignKey('video.id', ondelete='CASCADE'), nullable=False, comment='视频id')
    column_id = db.Column(db.Integer, db.ForeignKey('video_column.id', ondelete='CASCADE'), nullable=False,
                          comment='栏目id')
    sort = db.Column(db.SMALLINT, default=0, comment='视频排序')
    top = db.Column(db.SMALLINT, default=0, comment='视频置顶')
    release = db.Column(db.SMALLINT, default=1, comment='视频是否显示')
    recommend = db.Column(db.SMALLINT, default=0, comment='栏目推荐')

    video = db.relationship('Video', cascade='all,delete')
    video_column = db.relationship('VideoColumn', cascade='all,delete')

    def video_info(self, result: dict, *args, **kwargs):
        """完善栏目视频置顶排序等信息"""
        remove = {'id'}
        if kwargs.get('remove'):
            remove = remove | kwargs.get('remove')
            kwargs.pop('remove')
        result.update({'video_info': self.video.serialization(remove=remove, **kwargs)})

    def column_info(self, result: dict, *args: tuple, **kwargs: dict):
        """完善视频栏目信息"""
        remove = {'id', 'introduction', 'grade', 'icon', 'create_time'}
        result.update({'column_info': self.video_column.serialization(remove=remove)})


class VideoTag(Common, db.Model):
    """视频标签"""

    name = db.Column(db.String(length=10), nullable=False, unique=True, comment='标签名')
    description = db.Column(db.String(length=100), default='', comment='标签描述')


class Video(Common, db.Model):
    """视频"""

    title = db.Column(db.String(length=255), nullable=False, comment='视频标题')
    introduction = db.Column(db.String(length=255), default='', comment='视频简介')
    source = db.Column(db.String(length=255), default='', comment='视频来源')
    seo_title = db.Column(db.String(length=255), default='', comment='seo标题')
    cover = db.Column(db.String(length=255), default='', comment='视频封面图')
    url = db.Column(db.String(length=255), default='', comment='视频链接')

    playback_count = db.Column(db.Integer, default=0, comment='播放量')
    sharing_count = db.Column(db.Integer, default=0, comment='分享数')
    collection_count = db.Column(db.Integer, default=0, comment='收藏数')

    _tags = db.relationship('VideoTagsRelation', foreign_keys='VideoTagsRelation.video_id')

    def tags(self):
        """视频所有标签关系"""
        tags_id = [item.tag_id for item in self._tags]
        self.all_tag = VideoTag.query.filter(VideoTag.id.in_(tags_id)).all()
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


class VideoTagsRelation(Common, db.Model):
    """视频标签关系"""

    video_id = db.Column(db.Integer, db.ForeignKey('video.id', ondelete='CASCADE'), nullable=False, comment='视频id')
    tag_id = db.Column(db.Integer, db.ForeignKey('video_tag.id', ondelete='CASCADE'), nullable=False, comment='标签id')

    tag = db.relationship('VideoTag', foreign_keys=[tag_id])
