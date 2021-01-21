import multiprocessing
import random
import requests
from bs4 import BeautifulSoup


def try_pls(command, index):
    try:
        return command[index]
    except Exception:
        return '-'


def req(data):
    try:
        return requests.get(data[1], proxies={'https': 'http://' + data[0]})
    except Exception:
        pass

def search_by_articul(link):
    proxies = ['GswZhB:JC7NHX@194.67.207.2:8000', 'GswZhB:JC7NHX@194.67.206.83:8000', 'GswZhB:JC7NHX@194.67.207.208:8000', 'GswZhB:JC7NHX@194.67.206.135:8000', 'GswZhB:JC7NHX@194.67.207.71:8000', 'GswZhB:JC7NHX@185.5.248.100:8000', 'GswZhB:JC7NHX@194.67.205.23:8000', 'GswZhB:JC7NHX@185.5.248.108:8000', 'GswZhB:JC7NHX@185.238.139.211:8000', 'GswZhB:JC7NHX@194.67.207.0:8000', 'GswZhB:JC7NHX@185.238.136.65:8000', 'GswZhB:JC7NHX@194.67.207.4:8000', 'GswZhB:JC7NHX@194.67.207.193:8000', 'GswZhB:JC7NHX@194.67.205.62:8000', 'GswZhB:JC7NHX@194.67.204.241:8000', 'GswZhB:JC7NHX@194.67.207.167:8000', 'GswZhB:JC7NHX@185.5.248.72:8000', 'GswZhB:JC7NHX@185.5.248.2:8000', 'GswZhB:JC7NHX@194.67.206.59:8000', 'GswZhB:JC7NHX@194.67.207.254:8000', 'GswZhB:JC7NHX@194.67.207.202:8000', 'GswZhB:JC7NHX@194.67.207.155:8000', 'GswZhB:JC7NHX@194.67.206.132:8000', 'GswZhB:JC7NHX@185.238.139.147:8000', 'GswZhB:JC7NHX@194.67.206.158:8000', 'GswZhB:JC7NHX@194.67.207.74:8000', 'GswZhB:JC7NHX@194.67.206.137:8000', 'GswZhB:JC7NHX@194.67.207.248:8000', 'GswZhB:JC7NHX@194.67.205.245:8000', 'GswZhB:JC7NHX@194.67.206.236:8000']
    #proxies = open('n_p.txt', 'r').read().split('\n')

    ans = [False]
    while True:
        p_x = []
        for i in range(1):
            proxy = proxies[random.randint(0, len(proxies) - 1)]
            p_x.append([proxy, link])
        with multiprocessing.Pool(1) as p:
            ans = p.map(req, p_x)
        fl = False
        for i in ans:
            if str(i) != 'None':
                fl = True
                break
        if fl:
            break
    for a in ans:
        if a != 'None':
            r = a
            break
    data_c = str(BeautifulSoup(r.text, features='lxml'))
    try:
        idx = data_c.index('{"widgets":{"@marketplace/SkuBreadcrumbs":')
    except Exception:
        return search_by_articul(link)
    data_c = data_c[idx::]
    idx_end = data_c.index('</script>')
    information = (eval(data_c[:idx_end].replace('null', '').replace('false', '').replace('true', '').replace(':,', ': "",').replace(':}', ': ""}')))
    id_tovar = list(information['collections']['sku'].keys())[0]
    name = information['collections']['sku'][id_tovar]['titles']['raw']
    description = information['collections']['sku'][id_tovar]['description']
    pictures = []
    for i in information['collections']['sku'][id_tovar]['pictures']:
        pictures.append(f'https://avatars.mds.yandex.net/get-mpic/{i["original"]["groupId"]}/{i["original"]["key"]}/orig')

    pictures_count = len(pictures)
    category_data = information['collections']['category']
    category_idx = list(category_data.keys())
    category_name = '-'
    category_link = '-'
    for i in category_idx:
        try:
            category_name = category_data[category_idx]['fullName']
            category_link = f'https://pokupki.market.yandex.ru/catalog/{category_data[category_idx]["slug"]}/' \
                            f'{category_data[category_idx]["nid"]}/list'
            break
        except Exception:
            pass

    brend_data = information['collections']['vendor']
    brend_idx = list(brend_data.keys())[0]
    brend_link = category_link + '?glfilter=' + brend_data[brend_idx]['filter']
    brend_name = brend_data[brend_idx]['name']
    info_2 = (eval(data_c.split("data-zone-data='")[1].split("'")[0].replace('null', '').replace('false', '').replace('true', '').replace(':,', ': "",').replace(':}', ': ""}')))
    raiting = try_pls(info_2, 'rate')
    price = try_pls(info_2, 'price')
    old_price = try_pls(info_2, 'oldPrice')
    price_sale = '-'
    if old_price != '-':
        price_sale = str(float(old_price) - float(price))
    sklad = data_c.split('<div>Склад  </div>')[1].split('<div')[0]
    shop_info = (eval(data_c.split('data-zone-name="skuSupplierOperationalRating">')[0].split("data-zone-data=")[-1].replace("'", '')))
    shop_link = 'https://pokupki.market.yandex.ru/supplier/' + str(shop_info['shopId'])
    shop_name = shop_info['sellerName']
    try:
        otzv = data_c.split('data-tid="829cc048">')[1].split('</span>')[0]
    except Exception:
        otzv = '-'
    green_like = 'Нравится '
    fl = False
    green_stat_from_month = ''
    green_percent_recommended = ''
    gren_info = eval(data_c.split('"reasonsToBuy":')[1].split(']')[0] + ']')
    for i in gren_info:
        if 'factor_name' in i.keys():
            if fl:
                green_like = green_like + ', ' + i['factor_name'].lower()
            else:
                fl = True
                green_like += i['factor_name'].lower()
        elif 'id' in i.keys():
            if i['id'] == 'bought_n_times':
                green_stat_from_month = str(i['value']) + ' покупок за 2 месяца'
            elif i['id'] == 'viewed_n_times':
                green_stat_from_month = str(i['value']) + ' просмотр(ов) за 2 месяца'
            elif i['id'] == 'customers_choice':
                green_percent_recommended = str(float(i['value']) * 100) + '% рекомендуют'
    return {'name': name, 'description': description, 'pictures': pictures, 'pictures_count': pictures_count,
            'category_name': category_name, 'category_link': category_link, 'brend_name': brend_name,
            'brend_link': brend_link, 'raiting': raiting, 'price': price, 'old_price': old_price, 'sale': price_sale,
            'sklad': sklad, 'shop_link': shop_link, 'shop_name': shop_name, 'otzivi': otzv, 'green_1': green_like,
            'green_2': green_percent_recommended, 'green_3': green_stat_from_month, 'link_articul': link}


def get_links_from_catalog(link):
    proxies = ['GswZhB:JC7NHX@194.67.207.2:8000', 'GswZhB:JC7NHX@194.67.206.83:8000',
               'GswZhB:JC7NHX@194.67.207.208:8000', 'GswZhB:JC7NHX@194.67.206.135:8000',
               'GswZhB:JC7NHX@194.67.207.71:8000', 'GswZhB:JC7NHX@185.5.248.100:8000',
               'GswZhB:JC7NHX@194.67.205.23:8000', 'GswZhB:JC7NHX@185.5.248.108:8000',
               'GswZhB:JC7NHX@185.238.139.211:8000', 'GswZhB:JC7NHX@194.67.207.0:8000',
               'GswZhB:JC7NHX@185.238.136.65:8000', 'GswZhB:JC7NHX@194.67.207.4:8000',
               'GswZhB:JC7NHX@194.67.207.193:8000', 'GswZhB:JC7NHX@194.67.205.62:8000',
               'GswZhB:JC7NHX@194.67.204.241:8000', 'GswZhB:JC7NHX@194.67.207.167:8000',
               'GswZhB:JC7NHX@185.5.248.72:8000', 'GswZhB:JC7NHX@185.5.248.2:8000', 'GswZhB:JC7NHX@194.67.206.59:8000',
               'GswZhB:JC7NHX@194.67.207.254:8000', 'GswZhB:JC7NHX@194.67.207.202:8000',
               'GswZhB:JC7NHX@194.67.207.155:8000', 'GswZhB:JC7NHX@194.67.206.132:8000',
               'GswZhB:JC7NHX@185.238.139.147:8000', 'GswZhB:JC7NHX@194.67.206.158:8000',
               'GswZhB:JC7NHX@194.67.207.74:8000', 'GswZhB:JC7NHX@194.67.206.137:8000',
               'GswZhB:JC7NHX@194.67.207.248:8000', 'GswZhB:JC7NHX@194.67.205.245:8000',
               'GswZhB:JC7NHX@194.67.206.236:8000']
    proxy = proxies[random.randint(0, len(proxies) - 1)]
    r = requests.get(link, proxies={'https': 'http://' + proxy})
    r = r.text.split('"direct":"')
    urls = []
    for i in range(1, len(r), 2):
        urls.append(r[i].split('"}')[0])
    if len(urls) < 1:
        return get_links_from_catalog(link)
    return urls




def server(link):
    if 'https://pokupki.market.yandex.ru/catalog/' in link or 'https://pokupki.market.yandex.ru/supplier/' in link:
        links = get_links_from_catalog(link)
    elif 'https://pokupki.market.yandex.ru/product/' in link:
        links = []
        links.append(link)

    ans = []
    for i in links:
        print(i)
        ans.append(search_by_articul(i))
        print(f'Выполнено {len(ans)} из {len(links)}.')
    return ans


if __name__ == '__main__':
    multiprocessing.freeze_support()
    print(server(input("Введите ссылку: ")))