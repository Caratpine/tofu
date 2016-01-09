#!usr/bin/env python
# coding=UTF-8

Movie_tags = ['爱情', '喜剧', '动画', '剧情', '科幻', '动作', '经典', '悬疑', '青春', '犯罪', '惊悚', '文艺', '纪录片', '搞笑', '励志','恐怖', '战争', '短片', '魔幻', '黑色幽默', '传记', '情色', '动画短片', '感人', '暴力', '音乐', '家庭', '童年', '黑帮','浪漫', '女性', '同志', '史诗', '童话', '烂片', 'cult']

Movie_task_tags = ['童年', '黑帮','浪漫', '女性', '同志', '史诗', '童话', '烂片', 'cult']

Book_tags = {
  "文化": [
    "历史",
    "心理学",
    "哲学",
    "传记",
    "文化",
    "社会学",
    "艺术",
    "设计",
    "政治",
    "社会",
    "建筑",
    "宗教",
    "电影",
    "数学",
    "政治学",
    "回忆录",
    "思想",
    "中国历史",
    "国学",
    "音乐",
    "人文",
    "戏剧",
    "人物传记",
    "绘画",
    "艺术史",
    "佛教",
    "军事",
    "西方哲学",
    "近代史",
    "二战",
    "自由主义",
    "考古",
    "美术"
  ],
  "生活": [
    "爱情",
    "旅行",
    "生活",
    "励志",
    "成长",
    "心理",
    "摄影",
    "女性",
    "职场",
    "美食",
    "教育",
    "游记",
    "灵修",
    "情感",
    "健康",
    "手工",
    "养生",
    "两性",
    "人际关系",
    "家居",
    "自助游"
  ],
  "科技": [
    "科普",
    "互联网",
    "编程",
    "科学",
    "交互设计",
    "用户体验",
    "算法",
    "web",
    "科技",
    "UE",
    "通信",
    "交互",
    "UCD",
    "神经网络",
    "程序"
  ],
  "流行": [
    "漫画",
    "绘本",
    "推理",
    "青春",
    "言情",
    "科幻",
    "东野圭吾",
    "悬疑",
    "武侠",
    "韩寒",
    "奇幻",
    "日本漫画",
    "耽美",
    "亦舒",
    "三毛",
    "安妮宝贝",
    "网络小说",
    "郭敬明",
    "推理小说",
    "穿越",
    "金庸",
    "轻小说",
    "几米",
    "阿加莎·克里斯蒂",
    "张小娴",
    "幾米",
    "魔幻",
    "青春文学",
    "科幻小说",
    "J.K.罗琳",
    "高木直子",
    "古龙",
    "沧月",
    "落落",
    "张悦然",
    "蔡康永"
  ],
  "经管": [
    "经济学",
    "管理",
    "经济",
    "金融",
    "商业",
    "投资",
    "营销",
    "创业",
    "理财",
    "广告",
    "股票",
    "企业史",
    "策划"
  ],
  "文学": [
    "小说",
    "外国文学",
    "文学",
    "随笔",
    "中国文学",
    "经典",
    "散文",
    "日本文学",
    "村上春树",
    "童话",
    "诗歌",
    "杂文",
    "王小波",
    "儿童文学",
    "张爱玲",
    "古典文学",
    "余华",
    "名著",
    "钱钟书",
    "当代文学",
    "鲁迅",
    "外国名著",
    "诗词",
    "茨威格",
    "米兰·昆德拉",
    "杜拉斯",
    "港台"
  ]
}

Book_task_tags = {
  "文化": [
    "历史",
    "心理学",
    "哲学",
    "传记",
    "文化",
    "社会学",
    "艺术",
    "设计",
    "政治",
    "社会",
    "建筑",
    "宗教",
    "电影",
    "数学",
    "政治学",
    "回忆录",
    "思想",
    "中国历史",
    "国学",
    "音乐",
    "人文",
    "戏剧",
    "人物传记",
    "绘画",
    "艺术史",
    "佛教",
    "军事",
    "西方哲学",
    "近代史",
    "二战",
    "自由主义",
    "考古",
    "美术"
  ],
  "生活": [
    "爱情",
    "旅行",
    "生活",
    "励志",
    "成长",
    "心理",
    "摄影",
    "女性",
    "职场",
    "美食",
    "教育",
    "游记",
    "灵修",
    "情感",
    "健康",
    "手工",
    "养生",
    "两性",
    "人际关系",
    "家居",
    "自助游"
  ],
  "科技": [
    "科普",
    "互联网",
    "编程",
    "科学",
    "交互设计",
    "用户体验",
    "算法",
    "web",
    "科技",
    "UE",
    "通信",
    "交互",
    "UCD",
    "神经网络",
    "程序"
  ],
  "流行": [
    "漫画",
    "绘本",
    "推理",
    "青春",
    "言情",
    "科幻",
    "东野圭吾",
    "悬疑",
    "武侠",
    "韩寒",
    "奇幻",
    "日本漫画",
    "耽美",
    "亦舒",
    "三毛",
    "安妮宝贝",
    "网络小说",
    "郭敬明",
    "推理小说",
    "穿越",
    "金庸",
    "轻小说",
    "几米",
    "阿加莎·克里斯蒂",
    "张小娴",
    "幾米",
    "魔幻",
    "青春文学",
    "科幻小说",
    "J.K.罗琳",
    "高木直子",
    "古龙",
    "沧月",
    "落落",
    "张悦然",
    "蔡康永"
  ],
  "经管": [
    "经济学",
    "管理",
    "经济",
    "金融",
    "商业",
    "投资",
    "营销",
    "创业",
    "理财",
    "广告",
    "股票",
    "企业史",
    "策划"
  ],
  "文学": [
    "小说",
    "外国文学",
    "文学",
    "随笔",
    "中国文学",
    "经典",
    "散文",
    "日本文学",
    "村上春树",
    "童话",
    "诗歌",
    "杂文",
    "王小波",
    "儿童文学",
    "张爱玲",
    "古典文学",
    "余华",
    "名著",
    "钱钟书",
    "当代文学",
    "鲁迅",
    "外国名著",
    "诗词",
    "茨威格",
    "米兰·昆德拉",
    "杜拉斯",
    "港台"
  ]
}