import feedparser
import re
import notify

#删除多余html标签
def delhtml(t):
    pattern = re.compile(r'<[^>]+>',re.S)
    nohtml = pattern.sub('', t)
    
    #无视字数发送
    #return nohtml
    return nohtml[:100]+"......"


def GetNewRSS(url):
    f=feedparser.parse(url)
    #按每篇文章进行操作
    for post in f.entries:
        #读取之前的rss 作为对比文件
        with open("oldrss",errors='ignore') as file:
            old = file.read()
            
        #检查文章链接是否存在如果不存在则推送
        if not post.link in old:
            """
            f.feed.title     媒体名称
            post.title       文章标题
            post.description 文章内容
            post.link        文章链接
            post.published   文章时间
            <a href="url">   超链接
            """

            #特殊渠道需要传 link 参数 比如 feishu fcm     notify.feishu(post.title,delhtml(post.description),post.link)
            #默认渠道不需要send                        notify.send(f.feed.title+'  '+post.title, delhtml(post.description)+post.link)
            notify.feishu(post.title,delhtml(post.description),post.link)
            

            #打印文章标题
            print(f.feed.title,post.title)
            #写入oldrss记录
            oldrss=open('oldrss',mode='a+',errors='ignore')
            oldrss.writelines([f.feed.title,'  ',post.link,'  ',post.title,'\n'])
            oldrss.close

if __name__ == '__main__':
    #防止ACTION同步失败
    oldrss=open('oldrss',mode='a+',errors='ignore')
    oldrss.writelines('Update Start')
    oldrss.close
            
    #订阅地址在rss_sub文件，每行填一个网址。    
    for line in open("rss_sub",errors='ignore'):
        GetNewRSS(line)
