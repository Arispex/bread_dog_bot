import utils.server

version = 1.7

sql = 'create table prize_pool(ID integer primary key autoincrement, Name text not null,Price int not null, Progress text not null, ProgressServer integer default 1 not null, Content text);'

result, reason = utils.server.execute_sql(sql)

if result:
    print(f'数据库更新成功, 当前版本：{version}')

else:
    print(f"数据库更新失败, 原因：{reason}, 请联系开发者获得帮助")

input('按回车键退出')