import time ,json,requests,datetime
from pyecharts import options as opts
from pyecharts.charts import Map
from faker import Faker
class model:
        listmodel = list()
        def _init_(self,confirm,Province,city,dead,healm,addmun):
            self.confirm=confirm #确诊人数
            self.Province = Province    #省
            self.city = city    #市
            self.dead=dead  #死亡人数
            self.heal = heal    #治愈人数
            self.addmun=addmun  #新增病例

        def __str__(self):
            return ' 省：%s  市：%s 确诊人数：%d  死亡人数：%d  治愈人数：%d  新增病例：%d ' % (self.Province, self.city,self.confirm,  self.dead, self.heal, self.addmun)



updatetime=''
Faker = Faker(locale='zh_CN')

def getProvince():
            url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
            data=json.loads(requests.get(url=url).json()['data'])
            listpro =[]
            global updatetime
            updatetime=data['lastUpdateTime']
            for item in data['areaTree']:
                if item in data['areaTree']:
                    if (item['name'] == '中国'):
                        for item1 in item['children']:
                            if item1 in item['children']:
                                listpro.append(item1)
                        return listpro



def getCity():
        data= getProvince()

        listpro =[]
        for item in data:
            listpro.append(item)
        return  listpro

def setdata():

        listmodel =[]
        data = getCity();
        for item in data:
            for ite in item['children']:
                datamodel = model()
                datamodel.Province = item['name']
                datamodel.city=ite['name']
                datamodel.confirm=ite['total']['confirm']
                datamodel.dead = ite['total']['dead']
                datamodel.heal = ite['total']['heal']
                datamodel.addmun  = ite['today']['confirm']
                listmodel.append(datamodel)

        return listmodel

def setprovalue():
    model1 = model()
    listpro = dict()
    value= getCity()
    for item in value:
        listpro[item['name']]=item['total']['confirm']
        #model1.Province=item['name']
    return listpro

def chinaMap(value):
    province_distribution = {'河南': 45.23, '北京': 37.56, '河北': 21, '辽宁': 12, '江西': 6, '上海': 20, '安徽': 10, '江苏': 16,
                             '湖南': 9,
                             '浙江': 13, '海南': 2, '广东': 22, '湖北': 8, '黑龙江': 11, '澳门': 1, '陕西': 11, '四川': 7,
                             '内蒙古': 3, '重庆': 3, '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 11, '福建': 4, '青海': 1,
                             '天津': 1, '其他': 1}
    #provice = list(province_distribution.keys())
    #values = list(province_distribution.values())
    provice = list()
    values = list()
    for item in value:
        values.append(item['total']['confirm'])
        provice.append(item['name'])
    #print(provice)
   # print(values)
    map = Map("疫情地图", width=1200, height=600)
    map.add("疫情", provice, values, visual_range=[0, 500],maptype='china', is_visualmap=True,
            visual_text_color='#000', is_label_show=True)
    map.render(path="中国地图.html")

def map_visualmap(value) -> Map:
    c = (
        Map()
            .add("确诊人数", [list(z) for z in zip(value.keys(),value.values())], "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="实时疫情地图"),
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True,pieces=[
                 {"min": "1", "max": "9", "label": "1-9人", "color": "#FFA07A"},
                 {"min": "10", "max": "99", "label": "10-99人", "color": "#FA8072"},
                 {"min": "100", "max": "999", "label": "100-999人", "color": "#EE2C2C"},
                 {"min": "1000", "max": "","label": ">1000人", "color": "#8B1A1A"},
             ]),
        )
    )

    return c
def getpromap()->Map:
    c=(
        Map()
            .add("确诊人数",[list(z) for z in zip(Faker.providers, Faker.random_digit())] ,"广东")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="广东疫情"),
            visualmap_opts=opts.VisualMapOpts(max_='200',  is_piecewise=True),
        )
    )


def promap():
    # attr, value要显示的数值
    value = [20, 100]
    attr = ['余杭区', '萧山区']

    # 图框的基本特性
    m = Map('杭州地图示例图', width=600, height=400)

    # 添加数据到图框中
    m.add('', attr, value, maptype=u'杭州', visual_range=[0, 100], is_visualmap=True, visual_text_color='#000')

    # show_config() 打印输出图表的所有配置项
    m.show_config()

    # render() 生成 .html 文件
    m.render()

if __name__=='__main__':
    data= setdata()
    data1 = getCity()
    data2=setprovalue()
    #print(data2.keys())
    #print(data2.values())
    #zipp = zip(data2.keys(),data2.values())
    #promap()
    #data2=setprovalue()
    #print(list(zipp))
    #print(len(data1.keys()))
    #print(len(data1.values()))
    #chinaMap(data1)
    for ite in Faker.province():
        print(ite)

    #getpromap()

    #map= map_visualmap(data2)
   # map.render(path='snapshot.html')




