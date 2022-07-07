import utils.server

version = 1.2
sql = 'create table signInLog(ID  integer not null constraint signIn_pk primary key autoincrement, QQ text not null, getMoney integer)'
result, reason = utils.server.execute_sql(sql)

if result:
    print(f'数据库更新成功, 当前版本：{version}')

else:
    print(f"数据库更新失败, 原因：{reason}, 请联系开发者获得帮助")

input('按回车键退出')
