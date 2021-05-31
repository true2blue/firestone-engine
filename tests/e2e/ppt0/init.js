db.createCollection('users');
db.users.insert({
   username: "aqua",
   password: "e10adc3949ba59abbe56e057f20f883e",
   _id: ObjectId("5d905db9fc84d3224b0eb59c")
});
db.configmocks.insert({
    "_id" : ObjectId("5db796e4429e4baab72826a0"),
    "maxBuyNum" : 3,
    "curBuyNum" : 0,
    "ths_url" : "http://mncg.10jqka.com.cn/cgiwt/index/index",
    "cookie" : "__utma=156575163.1101180334.1557107567.1557375466.1557738304.3; __utmz=156575163.1557738304.3.3.utmcsr=yamixed.com|utmccn=(referral)|utmcmd=referral|utmcct=/fav/article/2/157; isSaveAccount=0; Hm_lvt_416c770ac83a9d996d7b3793f8c4994d=1572344617; user=MDphcXVhSVFjOjpOb25lOjUwMDo0MjUzOTk0Njc6NywxMTExMTExMTExMSw0MDs0NCwxMSw0MDs2LDEsNDA7NSwxLDQwOzEsMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOjI0Ojo6NDE1Mzk5NDY3OjE1NzI3NDcxNTc6OjoxNTA2MDQ4OTYwOjg2NDAwOjA6MWRmMGQzMDMyYzlhYzMyNTNmMjNjYjhmNDJmY2I4MGQ1OmRlZmF1bHRfMjox; userid=415399467; u_name=aquaIQc; escapename=aquaIQc; ticket=b39e2ff038a237a40bf6a2f9d37ec360; v=AtzK5ry_7VGH4pkNUVG8bGGArfGNVYBlAvmUQ7bd6EeqAXKn3mVQD1IJZMMF; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1572521197,1572588730,1572747084,1572747168; PHPSESSID=83db9bc22b6ac54cb7ccc89ca1c7f9aa; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1572756819",
    "username" : "48039195",
    "gdzh" : "0098894246",
    "sh_gdzh" : "A474614369",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c")
});
db.strategies.insertMany([{
    "_id" : ObjectId("5da19b7d181fc3600c5544c7"),
    "name" : "T0",
    "description" : "在<i>监控时间</i>范围内,买入并卖出股票",
    "op" : "buy",
    "url" : "PPT0",
    "parameters" : {
        "code" : "",
        "executeDate" : "",
        "monitorTime" : {
            "start" : "09:30",
            "end" : "15:00"
        },
        "force_sell_time" : "14:50:00",
        "pre" : {
            "high" : "0",
            "low" : "0",
            "close" : "0" 
        },
        "points" : "7",
        "approach" : "0.5",
        "stop_win" : "3.0",
        "drop_from_high" : "0.5",
        "body_length" : "3.0",
        "down_shadow_body_ratio" : "0.2",
        "down_shadow_body_ratio_min" : "0.1",
        "close_low_interval_time" : "60",
        "close_low_interval_time_max" : "600",
        "money" : {
            "time" : 1,
            "amount" : 200
        },
        "volume" : 1000
    }
}]);
db.mocktrades.insertMany([{
    "_id" : ObjectId("5db7e0a555609bb27252edb9"),
    "code" : "300448",
    "state" : "运行中",
    "result" : "无",
    "userId" : ObjectId("5d905db9fc84d3224b0eb59c"),
    "strategyId" : ObjectId("5da19b7d181fc3600c5544c7"),
    "createDate" : ISODate("2019-12-19T00:00:00.000Z"),
    "deleted" : false,
    "params" : {
        "code" : "300448",
        "executeDate" : "2019-12-19",
        "monitorTime" : {
            "start" : "09:30",
            "end" : "15:00"
        },
        "force_sell_time" : "14:50:00",
        "pre" : {
            "high" : "7.98",
            "low" : "7.61",
            "close" : "7.86"
        },
        "points" : "7",
        "approach" : "0.5",
        "stop_win" : "1.3",
        "drop_from_high" : "0.2",
        "body_length" : "0.62",
        "down_shadow_body_ratio" : "1.5",
        "down_shadow_body_ratio_min" : "0.1",
        "close_low_interval_time" : "60",
        "close_low_interval_time_max" : "600",
        "money" : {
            "time" : 1,
            "amount" : 15
        },
        "volume" : 1000
    }
}]);