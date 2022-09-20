# 介绍
通过ayaka编写的插件游戏库，本仓库的插件需要自行下载，手动添加到你的nonebot机器人运行目录下

通过pip安装、无需手动添加到nonebot目录下的ayaka插件合集请移步[ayaka-games](https://github.com/bridgeL/nonebot-plugin-ayaka-games)

# 使用方法

## nonebot2 

安装[nonebot-plugin-ayaka](https://github.com/bridgeL/nonebot-plugin-ayaka)插件（具体安装方法参看其仓库首页的readme.md）

下载本库中的所有插件（一个文档/文件夹就是一个插件），将其放到你的nonebot2机器人所在的地址中的某个文件夹下，例如`<你的nonebot地址>/ayaka_plugins`

然后在`bot.py`中增加如下代码`nonebot.load_plugins("ayaka_plugins")`

注1：动手能力强的同学如果想单独用某个插件的功能，可以自行看源码拆了（反正也不复杂

注2：一些插件间存在依赖关系，例如一些插件需要修改用户财富，则它们会调用bag.py中的一些方法。


