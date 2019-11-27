import re
import socket
def get_table_name(obj):
    """

    :return: 返回值为表名(str)
    """

    str1 = str(obj.__class__)
    pattern = r"(?<=\.)\w+(?=')"
    res = re.search(pattern, str1).group()
    return res


def get_colunm(obj):
    """

    :return: 返回值为1.字段名[list]
                    2.字段数据[list]
                    3.需要传输的[list]返回('%s','%d'...)
    """
    colunm_name = []
    colunm_value = []
    res_value = []
    for k, v in obj.__dict__.items():
        #非空字段则不用插入
        if v:
            colunm_name.append(k)

            if type(v) == int:
                res_value.append("%d")
            else:
                res_value.append("%s")
            colunm_value.append(v)
    return colunm_name,colunm_value,res_value

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def check_none(*args):
    """

    :param args: 需要校验的信息
    :return: 如果所有信息不为空则返回1,否则返回0
    """
    for i in args:
        if not i:
            return 0
    return 1

def check_password(pwd,pwd_confirm):
    """

    :param pwd:密码
    :param pwd_confirm:确认密码
    :return:密码和确认密码相同则返回1.否则返回0
    """
    if pwd == pwd_confirm:
        return 1
    return 0

"""
squeue.py 队列的顺序存储
思路:
1.基于列表完成数据存储
2.对列表进行封装
3.列表的头部作为队头,尾部作为队尾
功能:入队(enqueue),出队(dequeue)判断为空,删除

"""
class QueueException(Exception):
    pass

class SSqueue:
    def __init__(self):
        self.__elem = []
    #空
    def is_empty(self):
        return self.__elem == []
    #入队
    def enqueue(self,val):
        self.__elem.append(val)
    #出队
    def dequeue(self):
        if self.is_empty():
           raise QueueException("空")
        return self.__elem.pop(0)
    #删除
    def remove(self,val):
        self.__elem.remove(val)
