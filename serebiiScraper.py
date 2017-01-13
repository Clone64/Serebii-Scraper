from lxml import html
import requests
import re
import xlwt
import os

urls = ['http://serebii.net/events/serialcode.shtml',
        'http://serebii.net/events/wifi.shtml',
        'http://serebii.net/events/globallink.shtml',
        'http://serebii.net/events/ingame.shtml',
        'http://serebii.net/events/effects.shtml']

if not os.path.exists('Serebii_scrapes'):
    os.makedirs('Serebii_scrapes', 755)
for url in urls:
    page = requests.get(url)

    ##FILE NAMER
    url_name = url.split("/", 4)
    file_name = 'Serebii_%s' % (url_name[-1])
    file_name = file_name.replace(".shtml", "")

    tree = html.fromstring(page.content)
    name =[]
    bulk_data =[]
    seconds=[]
    months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'No', 'Dec', ]
    dates=[]
    start_dates=[]
    end_dates=[]
    def remove_img_tags(data):
        p = re.compile(r'<img.*?/>')
        return p.sub('', data)
        
        


    date_table = tree.xpath('//table[@class="date"]/tr/td/text()')
    for a in date_table:
        bulk_data.append(a)


    for i in bulk_data:
        for j in months:
            if j in i:
                dates.append(i)
    start_dates= dates[0::2]
    end_dates= dates[1::2]

    pokemon = tree.xpath('//td[@class="label"]/text()')
    for i in pokemon:
        text = i.replace(' ', '')
        poke = i.strip()
        poke1 = remove_img_tags(poke)       
        name.append(poke1)

        
    for a in name:
        if name.index(a)% 2 ==0 :
            seconds.append(a)
    seconds = [item for item in seconds if item.isalpha()]


    while len(start_dates)>len(seconds):
        start_dates.pop(-1)

    while len(end_dates)>len(seconds):
        end_dates.pop(-1)


    file_name = "%s.xls" %(file_name)
    book = xlwt.Workbook(encoding="utf-8")

    sheet1 = book.add_sheet("Sheet 1")
    sheet1.write(0,0, "name")
    sheet1.write(1,0,"start date")
    sheet1.write(2,0,"end date")
    i = 1
    j = 1
    k = 1
    for n in seconds:
       
        sheet1.write(0,i,n) 
        i+=1

    for m in start_dates:
        
        sheet1.write(1,j,m)
        j+=1
        
    for o in end_dates:
        sheet1.write(2,k,o)
        k+=1
    book.save('Serebii_scrapes/%s'%(file_name))

    print "book saved"

