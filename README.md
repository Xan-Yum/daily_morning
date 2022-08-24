# daily_morning
微信测试号每日提醒
在我刚想构思这个教程怎么让不懂编程的朋友很快入门的时候，我考虑到：避免服务器搭建，避免定时任务，避免接触代码。在经历过各种思考后，觉得可以用 Github Actions 来白嫖。。

效果如图。当然，文字是可以修改的。 

首先，按图搜索，测试号，进来之后微信扫码登录！ 

按图点击 Fork，创建到自己的仓库下！ image

按下图，创建模板，设置变量，把微信公众平台上的各种字符串按说明创建到 GitHub -> Settings -> Secrets -> Actions 中。

启用自己项目下的 Action！ 

如果运行出现错误，按以下方法可以看到错误，在这里 issue 提问也可以

启用后可以直接运行，看看女朋友的手机有没有收到推送吧！ 这个定时任务是每天早晨8点推送，如果会编程的同学可以自己自定义一些东西～

图中的操作，除了各种英文字符串不一样，模板消息中的中文不一样，其他的应该都是一样的，不然程序跑不通的～

Github 的右上角可以点击 star 给我点鼓励吧亲

有什么好玩的东西可以at我，我来教你们做

ps. 有一些注意事项在此补充

第一次登录微信公众平台测试号给的 app secret 是错误的，刷新一下页面即可
生日的日期格式是：05-20，纪念日的格式是 2022-08-09，请注意区分。城市请写到地级市，比如：北京，广州，承德
变量中粘贴的各种英文字符串不要有空格，不要有换行，除了模板之外都没有换行
Github Actions 的定时任务，在 workflow 的定义是 0 0 * * *，是 UTC 时间的零点，北京时间的八点。但是由于 Github 同一时间任务太多，因此会有延迟
我会偶尔优化一下代码，emm 但现在我自己在做一个完整的平台项目，想让大家更加便捷地上手

示例模板：

日期：{{ date.DATA }}
城市：{{ city.DATA }}
天气：{{ weather.DATA }}
当前温度：{{ temperature.DATA }}℃
气温：{{ lowest.DATA }}℃ ~ {{ highest.DATA }}℃
城市：{{ city1.DATA }}
天气：{{ weather1.DATA }}
当前温度：{{ temperature1.DATA }}℃
气温：{{ lowest1.DATA }}℃ ~ {{ highest1.DATA }}℃
距离考试还有：{{ exam_date.DATA }} 天
距离我的生日还有：{{ birthday.DATA }} 天
距离你的生日还有：{{ birthday1.DATA }} 天
{{ words.DATA }}

需定义字段：
APP_ID
APP_SECRET
USER_ID
TEMPLATE_ID
CITY
CITY1
BIRTHDAY
BIRTHDAY1
START_DATE
EXAM_DATE
