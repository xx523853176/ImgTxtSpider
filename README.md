# ImgTxtSpider
图文相关的爬虫，从百度文库开始，慢慢来……路很长……

## 支持
- 百度文库
  - 所有PPT、PDF（含付费、不可见等……均可下载为图片格式）
  - 所有可见文字：DOC、TXT……
  
## 使用方式（BaiduWenkuSprder.py末尾）
```python
if __name__=="__main__":
    文档网址 = "https://wenku.baidu.com/view/7fa86fbb29ea81c758f5f61fb7360b4c2e3f2aca.html?from=search"
    #此处修改网址
    存储目录 = ".\\"
    #此处修改存储位置，默认当前文件夹下新建子文件夹
    测试任务 = 百度文库下载( 文档网址, 存储目录 )
    #新建下载class，加载参数开始下载。
```

## 更新日志：
#### 2019.11.18
1. 百度文库：图片类可完美下载；文字类仅下载可见部分。
1. 已知百度文字类请求为JIT HS256加密，后续摸索。
