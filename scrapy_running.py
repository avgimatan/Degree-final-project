import subprocess


def scrapy_running_by_user(user_or_keyword, value, user='Dwider', password='qwerty123', username='Admin'):
    subprocess.call("curl -XDELETE localhost:9200/dnmavengerss", shell=True)
    subprocess.call(['scrapy', 'crawl', 'crawl_type', '-a', 'user_or_keyword=' + user_or_keyword, '-a', 'value=' + value ,
                     '-a', 'user=' + user, '-a', 'password=' + password, '-a', 'username=' + username],
                    shell=True,
                    cwd=r'C:\Users\Administrator\PycharmProjects\darkNet\ScrapyCrawl')
    return subprocess.Popen("node run.js", shell=True, cwd=r'C:\Users\Administrator\PycharmProjects\darkNet')


def scrapy_running_all_forums():
    subprocess.call("curl -XDELETE localhost:9200/dnmavengerss", shell=True)
    subprocess.call(['scrapy', 'crawl', 'crawler'],
                    shell=True,
                    cwd=r'C:\Users\Administrator\PycharmProjects\darkNet\ScrapyCrawl')
    subprocess.call("node run.js", shell=True, cwd=r'C:\Users\Administrator')


# user = author
# keyword = keywords
if __name__ == '__main__':
    # scrapy_running_by_user('author', 'Anglo','Dwider', 'qwerty123')
    scrapy_running_all_forums()
