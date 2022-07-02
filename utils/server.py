import sqlite3


def execute_sql(sql: str):
    """
     在数据库执行指定的sql语句
    :param sql: 执行的sql语句
    :return: 执行结果 成功返回[True, sql执行结果] 失败返回 [False, 失败原因]
    """
    try:
        conn = sqlite3.connect("Bot.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        sql_return_result = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return True, sql_return_result
    except sqlite3.OperationalError:
        return False, "无法连接至数据库"


class GetInfo:
    """
    获取服务器基础信息(ID, Ip, Port, Token)
    """

    @staticmethod
    def all():
        """
        获取所有服务器基础信息
        :return: 获取结果 成功返回[True, 获取结果], 失败返回[False, 失败原因]
        """
        result, sql_return_result = execute_sql("select * from server")
        if result:
            return True, sql_return_result
        else:
            return False, sql_return_result

    @staticmethod
    def by_id(id: int):
        """
        以ID获取服务器信息
        :param id: 服务器ID
        :return: 获取结果 成功返回[True, 获取结果], 失败返回[False, 失败原因]
        """
        result, sql_return_result = execute_sql("select * from server where ID = '%s'" % id)
        if result:
            if not sql_return_result:
                return False, "不存在此服务器"
            else:
                return True, sql_return_result[0]
        else:
            return False, sql_return_result

    @staticmethod
    def by_name(name: str):
        """
        以服务器名称获取服务器信息
        :param name: 服务器名称
        :return: 获取结果 成功返回[True, 获取结果], 失败返回[False, 失败原因]
        """
        result, sql_return_result = execute_sql("select * from server where Name = '%s'" % name)
        if result:
            if not sql_return_result:
                return False, "不存在此服务器"
            else:
                return True, sql_return_result[0]
        else:
            return False, sql_return_result

    @staticmethod
    def by_ip(ip: str):
        """
        以服务器ip获取服务器信息
        :param ip: 服务器ip
        :return: 获取结果 成功返回[True, 获取结果], 失败返回[False, 失败原因]
        """
        result, sql_return_result = execute_sql("select * from server where IP = '%s'" % ip)
        if result:
            if not sql_return_result:
                return False, "不存在此服务器"
            else:
                return True, sql_return_result[0]
        else:
            return False, sql_return_result

    @staticmethod
    def by_port(port: int):
        """
        以服务器端口获取服务器信息
        :param port: 服务器端口
        :return: 获取结果 成功返回[True, 获取结果], 失败返回[False, 失败原因]
        """
        result, sql_return_result = execute_sql("select * from server where Port = '%s'" % port)
        if result:
            if not sql_return_result:
                return False, "不存在此服务器"
            else:
                return True, sql_return_result[0]
        else:
            return False, sql_return_result

    @staticmethod
    def by_token(token: str):
        """
        以服务器令牌(token)获取服务器信息
        :param token: 服务器令牌(token)
        :return: 获取结果 成功返回[True, 获取结果], 失败返回[False, 失败原因]
        """
        result, sql_return_result = execute_sql("select * from server where Token = '%s'" % token)
        if result:
            if not sql_return_result:
                return False, "不存在此服务器"
            else:
                return True, sql_return_result[0]
        else:
            return False, sql_return_result


def add(name: str, ip: str, port: str, token: str):
    """
    添加服务器至数据库
    :param name: 服务器名称
    :param ip: 服务器IP
    :param port: 服务器端口
    :param token: 服务器令牌
    :return: 添加服务器结果 成功返回[True, None] 失败返回[False, 失败原因]
    """
    result, server_info = GetInfo.by_name(name)
    if result:
        return False, "已经存在同名服务器"
    else:
        result, sql_return_result = execute_sql(
            "insert into server (Name, IP, Port, Token) values ('%s', '%s', '%s', '%s')" % (name, ip, port, token))
        if result:
            result, server_info_list = GetInfo.all()
            num = 1
            for i in server_info_list:
                execute_sql("update server set ID = '%s' where Name = '%s'" % (num, i[1]))
                num += 1
            execute_sql("update sqlite_sequence set seq = '%s' where name = '%s'" % (len(server_info_list), "server"))
            return True, None
        else:
            return False, sql_return_result


def delete(name: str):
    """
    删除数据库中指定的服务器
    :param name: 服务器名称
    :return: 删除服务器结果 成功返回[True, None] 失败返回[False, 失败原因]
    """
    result, server_info = GetInfo.by_name(name)
    if result:
        result, sql_return_result = execute_sql("delete from server where name = '%s'" % name)
        if result:
            result, server_info_list = GetInfo.all()
            num = 1
            for i in server_info_list:
                execute_sql("update server set ID = '%s' where Name = '%s'" % (num, i[1]))
                num += 1
            execute_sql("update sqlite_sequence set seq = '%s' where name = '%s'" % (len(server_info_list), "server"))
            return True, None
        else:
            return False, sql_return_result
    else:
        return False, server_info


def reset():
    """
    重置服务器列表
    :return: 重置服务器列表结果 成功返回[True, None] 失败返回[False, 失败原因]
    """
    result, sql_return_result = execute_sql("update sqlite_sequence set seq = 0 where name = 'server'")
    if result:
        execute_sql("delete from server")
        return True, None
    else:
        return False, sql_return_result
