# README

## /post

接收传入数据，添加至数据库中。

若数据保存成功，返回`upload completed`，若失败返回错误信息。

合法接收数据样例：

```json
{ "ID":1,"Algorithm":"Elastic","Time":"2021-05-10 22:22:24","Cardinality":2,"Entropy":0.618,"heavypart":[[3232235777,2001,3232235778,2002,"TCP",1000,1], [3232235777,2001,3232235779,2003,"TCP",2000,1]],"lightpart":[[523064338,99],[486786338,5],],"distribute":[[99,1],[1000,1],[2000,1]] }
```

## /clean

清空数据库（删除通过/post生成的全部数据表）。

## sessions.dbquery

查询指定数据表中记录（按主键倒序排列）。

以JSON格式返回查询内容。若查询失败，返回空列表。

### 参数：

table：指定查询的数据表
option：指定最大返回行数

如访问`/query?table=attribute&option=1`，则返回`attribute`数据表中ID最大的一行。

## sessions.dbcommand

直接在MySQL数据库中执行`<cmd>`指令。

若有查询内容，以JSON格式返回。

