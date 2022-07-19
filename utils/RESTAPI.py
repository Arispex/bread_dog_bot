import requests


class V2:
    class Server:
        @staticmethod
        def status(ip: str, port: str, token: str):
            """
            返回有关服务器状态的基本信息。
            :param ip: 服务器ip
            :param port: 服务器端口
            :param token: 服务器令牌
            :return: 执行结果 成功返回[True, 执行结果] 失败返回[False, 执行结果/失败原因]
            """
            url = f"http://{ip}:{port}/v2/server/status?players=true&rules=false&token={token}"
            headers = {"Accept": "application/json"}
            try:
                response = requests.get(url, headers=headers, timeout=3)
                if response.status_code == 200:
                    if response.json()["status"] == "200":
                        return True, response.json()
                    else:
                        try:
                            return False, response.json()["error"]
                        except IndexError:
                            return False, "\n".join(response.json()["response"])
                elif response.status_code == 401:
                    return False, "没有令牌，无法访问指定的API端点"
                elif response.status_code == 403:
                    return False, "令牌错误，无法访问指定的API端点"
                elif response.status_code == 404:
                    return False, "指定的API端点不存在"
                elif response.status_code == 400:
                    return False, "请求参数错误"
                elif response.status_code == 500:
                    return False, "服务器错误"
                else:
                    return False, "无法连接至服务器"
            except requests.exceptions.RequestException:
                return False, "无法连接至服务器"


class V3:
    class Server:
        @staticmethod
        def rawcmd(ip: str, port: str, token: str, cmd: str):
            """
            在服务器上执行远程命令，并返回命令的输出。
            :param ip: 服务器ip
            :param port: 服务器端口
            :param token: 服务器令牌
            :param cmd: 要执行的远程命令
            :return: 执行结果 成功返回[True, 执行结果] 失败返回[False, 执行结果/失败原因]
            """
            url = f"http://{ip}:{port}/v3/server/rawcmd?cmd={cmd}&token={token}"
            headers = {"Accept": "application/json"}
            try:
                response = requests.get(url, headers=headers, timeout=3)
                if response.status_code == 200:
                    if response.json()["status"] == "200":
                        return True, response.json()
                    else:
                        try:
                            return False, response.json()["error"]
                        except IndexError:
                            return False, "\n".join(response.json()["response"])
                elif response.status_code == 401:
                    return False, "没有令牌，无法访问指定的API端点"
                elif response.status_code == 403:
                    return False, "令牌错误，无法访问指定的API端点"
                elif response.status_code == 404:
                    return False, "指定的API端点不存在"
                elif response.status_code == 400:
                    return False, "请求参数错误"
                elif response.status_code == 500:
                    return False, "服务器错误"
                else:
                    return False, "无法连接至服务器"
            except requests.exceptions.RequestException:
                return False, "无法连接至服务器"


class Player:
    @staticmethod
    def inventory(ip: str, port: str, token: str, name: str):
        """
        获取指定玩家的库存
        该功能需要服务器插件 REST API Extensions 否则无法使用
        :param ip: 服务器ip
        :param port: 服务器端口
        :param token: 服务器令牌
        :param name: 玩家名称
        :return: 执行结果 成功返回[True, 执行结果] 失败返回[False, 执行结果/失败原因]
        """
        url = f"http://{ip}:{port}/player/inventory?player={name}&token={token}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=3)
        try:
            if response.status_code == 200:
                if response.json()["status"] == "200":
                    return True, response.json()
                else:
                    try:
                        return False, response.json()["error"]
                    except IndexError:
                        return False, "\n".join(response.json()["response"])
            elif response.status_code == 401:
                return False, "没有令牌，无法访问指定的API端点"
            elif response.status_code == 403:
                return False, "令牌错误，无法访问指定的API端点"
            elif response.status_code == 404:
                return False, "未安装服务器插件 REST API Extensions"
            elif response.status_code == 400:
                return False, "请求参数错误"
            elif response.status_code == 500:
                return False, response.json()["errormsg"]
            else:
                return False, "无法连接至服务器"
        except requests.exceptions.RequestException:
            return False, "无法连接至服务器"


class World:
    @staticmethod
    def progress(ip: str, port: str, token: str):
        """
        获取服务器的进度
        该功能需要服务器插件 REST API Extensions 否则无法使用
        :param ip: 服务器ip
        :param port: 服务器端口
        :param token: 服务器令牌
        :return: 执行结果 成功返回[True, 执行结果] 失败返回[False, 执行结果/失败原因]
        """
        url = f"http://{ip}:{port}/world/progress?&token={token}"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers, timeout=3)
        try:
            if response.status_code == 200:
                if response.json()["status"] == "200":
                    return True, response.json()
                else:
                    try:
                        return False, response.json()["error"]
                    except IndexError:
                        return False, "\n".join(response.json()["response"])
            elif response.status_code == 401:
                return False, "没有令牌，无法访问指定的API端点"
            elif response.status_code == 403:
                return False, "令牌错误，无法访问指定的API端点"
            elif response.status_code == 404:
                return False, "未安装服务器插件 REST API Extensions"
            elif response.status_code == 400:
                return False, "请求参数错误"
            elif response.status_code == 500:
                return False, response.json()["errormsg"]
            else:
                return False, "无法连接至服务器"
        except requests.exceptions.RequestException:
            return False, "无法连接至服务器"
