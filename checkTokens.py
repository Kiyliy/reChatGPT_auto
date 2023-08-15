import requests
import json
import threading
import openpyxl
from multiprocessing import Value
from writeExcle import GetXlsxData
import config
from getAccessToken import GetAccessTokenThread
import pooltoken
import os
           

def main():
    #修改工作区
    filedir = os.path.abspath(__file__)#获取当前文件路径
    fatherdir = os.path.dirname(__file__)#获取父目录
    os.chdir(fatherdir)#修改工作区到父目录

    """
    自动读取文件夹账号密码, 使用faketoken取token,refresh token,然后使用token 和 name,取fake token, 最后将信息保存到工作表中
    
    """
    cnt = Value("i",0)
    #新建工作表
    AccessTokensWorkbook = openpyxl.Workbook()
    AccessTokensWorksheet = AccessTokensWorkbook.active
    errorWorkBook = openpyxl.Workbook()
    errorWorksheet = errorWorkBook.active
    #写入表头
    AccessTokensWorksheet.append(["用户名", "密码", "AccessToken","有效期","id_token","refresh_token","fake_token","unique_name"])
    errorWorksheet.append(["用户名", "密码", "错误信息"])
    #创建队列对象和锁对象
    xlsxQueue = GetXlsxData(config.work_book_name,config.work_sheets_n)
    lock = threading.Lock()

    try:
        threads = []
        for i in range(config.thread_num):
            #创建线程
            thread = GetAccessTokenThread(lock, xlsxQueue, AccessTokensWorksheet, cnt = cnt,errorWorksheet=errorWorksheet)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
    except:
        print("Error: 无法启动线程")

    # 保存工作簿到新的Excel文件
    AccessTokensWorkbook.save(config.new_excle_name)
    errorWorkBook.save(config.work_book_name[:-5]+"错误文件.xlsx")
    print("有效值已写入新的Excel文件！")

    if(input("是否要更新token池？(y/n)") == "y"):
        pooltoken.main()


if __name__ == "__main__":
    main()

