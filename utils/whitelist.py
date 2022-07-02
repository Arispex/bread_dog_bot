import utils.server
import utils.RESTAPI


class GetInfo:
    """
    获取数据库中白名单玩家信息
    """

    @staticmethod
    def all():
        """
        获取所有白名单玩家信息
        :return:获取结果 成功返回[True, 白名单玩家信息] 失败返回[False, 失败原因]
        """
        result, sql_return_result = utils.server.execute_sql("select * from whitelist")
        if result:
            return True, sql_return_result
        else:
            return False, sql_return_result

    @staticmethod
    def by_id(id: int):
        """
        以ID获取白名单玩家信息
        :return:获取结果 成功返回[True, 白名单玩家信息] 失败返回[False, 失败原因]
        """
        result, sql_return_result = utils.server.execute_sql("select * from whitelist where ID = '%s'" % id)
        if result:
            if not sql_return_result:
                return False, "不存在此玩家"
            else:
                return True, sql_return_result[0]
        else:
            return False, sql_return_result

    @staticmethod
    def by_qq(qq: str):
        """
        以QQ获取白名单玩家信息
        :return:获取结果 成功返回[True, 白名单玩家信息] 失败返回[False, 失败原因]
        """
        result, sql_return_result = utils.server.execute_sql("select * from whitelist where QQ = '%s'" % qq)
        if result:
            if not sql_return_result:
                return False, "不存在此玩家"
            else:
                return True, sql_return_result[0]
        else:
            return False, sql_return_result

    @staticmethod
    def by_name(name: str):
        """
        以游戏名称获取白名单玩家信息
        :return:获取结果 成功返回[True, 白名单玩家信息] 失败返回[False, 失败原因]
        """
        result, sql_return_result = utils.server.execute_sql("select * from whitelist where Name = '%s'" % name)
        if result:
            if not sql_return_result:
                return False, "不存在此玩家"
            else:
                return True, sql_return_result[0]
        else:
            return False, sql_return_result


def add_to_server(ip: str, port: str, token: str, name: str):
    """
    添加白名单至服务器 需要Better Whitelist插件
    :param ip: 服务器ip
    :param port: 服务器端口
    :param token: 服务器令牌
    :param name: 玩家名称
    :return: 添加结果 成功返回[True, None] 失败返回[True, 失败原因]
    """
    command = f"/bwl add {name}"
    result, command_output = utils.RESTAPI.V3.Server.rawcmd(ip, port, token, command)
    if result:
        if command_output["response"][0] == "添加成功!":
            return True, None
        else:
            return False, command_output["response"][0]
    else:
        try:
            return False, command_output["error"]
        except TypeError:
            return False, command_output


def add_to_db(qq: str, name: str):
    """
    添加白名单至数据库
    :param qq: 玩家QQ
    :param name: 玩家昵称
    :return: 添加结果 成功返回[True, None] 失败返回[False, 失败原因]
    """
    result, sql_return_result = utils.server.execute_sql("insert into whitelist(QQ, Name) values ('%s', '%s')" % (qq, name))
    if result:
        return True, None
    else:
        return False, sql_return_result


def delete_from_server(ip: str, port: str, token: str, name: str):
    """
    从服务器中删除白名单 需要Better Whitelist插件
    :param ip: 服务器ip
    :param port: 服务器端口
    :param token: 服务器令牌
    :param name: 玩家名称
    :return: 删除结果 成功返回[True, None] 失败返回[False, 失败原因]
    """
    command = f"/bwl del {name}"
    result, command_output = utils.RESTAPI.V3.Server.rawcmd(ip, port, token, command)
    if result:
        if command_output["response"][0] == "删除成功！":
            return True, None
        else:
            return False, command_output["response"][0]
    else:
        try:
            return False, command_output["error"]
        except TypeError:
            return False, command_output


def delete_from_db(qq: str):
    """
    从数据库中删除白名单
    :param qq: 玩家QQ
    :return: 添加结果 成功返回[True, None] 失败返回[False, 失败原因]
    """
    result, sql_return_result = utils.server.execute_sql("delete from whitelist where QQ = '%s'" % qq)
    if result:
        return True, None
    else:
        return False, sql_return_result


def reset():
    """
    重置数据库白名单
    :return: 重置结果 成功返回[True, None] 失败返回[False, 失败原因]
    """
    result, sql_return_result = utils.server.execute_sql("update sqlite_sequence set seq = 0 where name = 'whitelist'")
    if result:
        utils.server.execute_sql("delete from whitelist")
        return True, None
    else:
        return False, sql_return_result
