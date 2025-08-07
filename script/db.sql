-- init tab icon
insert into file(id, file_name, bucket_name, path, usage_type, remark)
values (100, 'sy.png', 'hxxd', 'tab/sy.png', 'tab_bar_icon', '首页'),
       (200, 'sy_1.png', 'hxxd', 'tab/sy_1.png', 'tab_bar_icon', '首页'),
       (300, 'kf.png', 'hxxd', 'tab/kf.png', 'tab_bar_icon', '客服'),
       (400, 'kf_1.png', 'hxxd', 'tab/kf_1.png', 'tab_bar_icon', '客服'),
       (500, 'gwc.png', 'hxxd', 'tab/gwc.png', 'tab_bar_icon', '购物车'),
       (600, 'gwc_1.png', 'hxxd', 'tab/gwc_1.png', 'tab_bar_icon', '购物车'),
       (700, 'wo.png', 'hxxd', 'tab/wo.png', 'tab_bar_icon', '我'),
       (800, 'wo_1.png', 'hxxd', 'tab/wo_1.png', 'tab_bar_icon', '我')

-- init category
insert into category(id, name, code, icon, parent_id)
       values
         (1, '海参', 'haishen', '1000', 0),
         (2, '虾', 'xia', '2000', 0),
         (3, '贝类', 'beilei', '3000', 0),
         (4, '蟹类', 'xie', '4000', 0),
         (5, '海苔', 'haitai', '5000', 0);

-- init goods
insert
into goods(id, title, price, stock, status, detail, is_hot, main_image, thumb_images, detail_images, category_id)
values
    (100, '海参', 100, 100, True, '海参是海洋中的一种软体动物，富含蛋白质和多种营养成分，具有滋补养生的功效。', True, '1000', '[1001]', '[1001,1002]', 1),
    (200, '黑虎虾', 100, 100, True, '黑虎虾是一种大型海虾，肉质鲜美，富含蛋白质和微量元素，是海鲜中的珍品。', True, '1000', '[1001]', '[1001,1002]', 2),
    (300, '鲍鱼', 100, 100, True, ' 鲍鱼是一种名贵的海���贝类，肉质鲜嫩，营养丰富，常被视为海味珍品。', True, '3000', '[3001]', '[3001,3002]', 3),
    (400, '大闸蟹', 100, 100, True, '大闸蟹是中国特产，以其鲜美的蟹肉和蟹黄闻名，深受食客喜爱。', True, '4000', '[4001]', '[4001,4002]', 4),
    (500, '紫菜', 100, 100, True, '紫菜是一种常见的海藻，富含多种营养成分，常用于汤品和寿司等料理。', True, '5000', '[5001]', '[5001,5002]', 5);
