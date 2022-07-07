import utils.RESTAPI
import utils.whitelist


class Connect:
    """
    连接TShock服务器
    """

    def __init__(self, ip: str, port: str, token: str):
        """
        连接TShock服务器
        :param ip: 服务器ip
        :param port: 服务器端口
        :param token: 服务器令牌
        """
        self.ip = ip
        self.port = port
        self.token = token

        self.status_code, self.status = utils.RESTAPI.V2.Server.status(self.ip, self.port, self.token)
        if self.status_code:
            self.name = self.status["name"]
            self.serverversion = self.status["serverversion"]
            self.tshockversion = self.status["tshockversion"]
            self.server_port = self.status["port"]
            self.playercount = self.status["playercount"]
            self.maxplayers = self.status["maxplayers"]
            self.world = self.status["world"]
            self.uptime = self.status["uptime"]
            self.serverpassword = self.status["serverpassword"]
            self.players = self.status["players"]
        else:
            self.error = self.status

    def online_players(self):
        """
        获取服务器的在线玩家
        :return: 执行结果 成功返回[True, 在线玩家列表] 失败返回[False, 失败原因]
        """
        if self.status_code:
            result = []
            for i in self.players:
                result.append(i["nickname"])

            return True, result
        else:
            try:
                return False, self.status["error"]
            except TypeError:
                return False, "无法连接至服务器"

    def remote_command(self, command: str):
        """
        执行远程指令
        :param command: 指令
        :return: 执行成功 成功返回[True, 执行结果] 失败返回[False, 失败原因]
        """
        if self.status_code:
            result, execute_result = utils.RESTAPI.V3.Server.rawcmd(self.ip, self.port, self.token, command)
            if result:
                return True, execute_result
            else:
                return False, execute_result
        else:
            try:
                return False, self.status["error"]
            except TypeError:
                return False, "无法连接至服务器"

    def add_whitelist(self, qq: str, name: str):
        """
        添加白名单至服务器/数据库 需要Better Whitelist插件
        :param qq: 玩家QQ
        :param name: 玩家名称
        :return: 添加结果 成功返回[True, None] 失败返回[False, 失败原因]
        """
        if self.status_code:
            result, player_info = utils.whitelist.GetInfo.by_qq(qq)
            if result:
                # 如果玩家已经存在于白名单中
                result, reason = utils.whitelist.add_to_server(self.ip, self.port, self.token, player_info[2])
                if result:
                    return True, None
                else:
                    return False, "你已经添加过白名单了"
            else:
                # 如果玩家不存在于白名单中
                result, reason = utils.whitelist.add_to_server(self.ip, self.port, self.token, name)
                if result:
                    result, reason = utils.whitelist.add_to_db(qq, name)
                    if result:
                        return True, None
                    else:
                        return False, reason
                else:
                    return False, reason
        else:
            try:
                return False, self.status["error"]
            except TypeError:
                return False, "无法连接至服务器"

    def delete_whitelist(self, qq: str):
        """
        从服务器/数据库中删除白名单 需要Better Whitelist插件
        :param qq: 玩家QQ
        :return: 删除结果 成功返回[True, None] 失败返回[False, 失败原因]
        """
        if self.status_code:
            result, player_info = utils.whitelist.GetInfo.by_qq(qq)
            if result:
                # 如果玩家已经存在于白名单中
                result, reason = utils.whitelist.delete_from_server(self.ip, self.port, self.token, player_info[2])
                if result:
                    result, reason = utils.whitelist.delete_from_db(qq)
                    if result:
                        return True, None
                    else:
                        return False, reason
                else:
                    return False, reason
            else:
                # 如果玩家不存在于白名单中
                return False, player_info
        else:
            try:
                return False, self.status["error"]
            except TypeError:
                return False, "无法连接至服务器"

    def say(self, content: str):
        """
        向服务器发送消息
        :param content:发送内容
        :return: 发送结果 成功返回[True, None] 失败返回[False, 失败原因]
        """
        if self.status_code:
            command = f"/say {content}"
            result, execute_result = utils.RESTAPI.V3.Server.rawcmd(self.ip, self.port, self.token, command)
            if result:
                return True, None
            else:
                return False, execute_result
        else:
            try:
                return False, self.status["error"]
            except TypeError:
                return False, "无法连接至服务器"
