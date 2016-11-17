# DMSpider

一个为在动漫之家动漫网下载漫画的爬虫。

## 用法

crawl chapter [ -p PATH -z ] URL

crawl chapter [ -p PATH -z ] -f FILE

crawl comic [ -p PATH -z ] URL

crawl comic [ -p PATH -z ] -f FILE

### 选项

chapter				输入的地址是单话地址

comic				输入的是漫画目录地址

-h --help			显示帮助

-f FILE				输入文件

-p PATH				漫画保存位置

-z                  压缩下载文件

<pre>
<code>
./crawl chapter http://manhua.dmzj.com/grandblue/28907.shtml  # 下载一话

./crawl comic -z -f links.txt  # 下载整本漫画
</code>
</pre>

注意：如果一次要下载多个地址，即使用文件输入的话，文件内要每个下载地址独立占用一行。
