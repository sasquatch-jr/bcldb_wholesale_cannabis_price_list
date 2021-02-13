import csv
import time
import jinja2
import requests

from datetime import datetime


template = """<html>
<head><title>BCLDB Wholesale Cannabis Price List</title></head>
<body>
<h1>BCLDB Wholesale Cannabis Price List</h1>
<h2><a href="https://github.com/sasquatch-jr/bcldb_wholesale_cannabis_price_list/blob/main/README.md">FAQ</a>
<a href="https://github.com/sasquatch-jr/bcldb_wholesale_cannabis_price_list/blob/main/bccs_dump.py">Source Code</a>
<a href="https://github.com/sasquatch-jr/bcldb_wholesale_cannabis_price_list/blob/main/dump.csv">CSV</a>
</h2>
<h3>Generated {{now}} UTC</h3>
<table>
{% for item in products %}
<tr>
   <td><img src={{item['thumb']}} width=150/></td>
   <td><a href={{item['url']}}>{{item['name']}}</a></td>
   <td>{{item['brand']}} - {{item['lp']}}</td>
   <td><table>{% for size in item['sizes'] %}
    <tr>
        <td>{{size['name']}}
        ${{size['price']}}
        (${{'%0.2f' % size['price_per_item']}} each) -
        {{size['in_stock']}}
        {% if size['retail_price'] %}
        <br />
        <a href=https://www.bccannabisstores.com/products/{{item['id']}}>Retail price ${{size['retail_price']}} ({{size['retail_markup']}}% markup)</a>
        {% endif %}
        {% if size['order_limit'] %}
        <br />
        Retailers may only purchase {{size['order_limit']}} of this item!
        {% endif %}
        <br />
        LP cut: ${{size['lp_cut']}}, BCLDB Cut: ${{size['bcldb_cut']}}
        </td>
    </tr>
    {% endfor %}
    </table></td>
</tr>
{% endfor %}
</table>
</body>
</html>"""


def fetch_products_from_base_url(base_url):
    """Fetch all product definitions from the products.json endpoint
    """
    page_number = 1
    products = []
    prods = []
    more_pages = True

    while more_pages:
        req = requests.get(base_url + "/products.json?limit=250&page=" + str(page_number))
        if req.status_code == 200:
            new_products = req.json()['products']
            if len(new_products) == 0:
                more_pages = False
            else:
                products += req.json()['products']
                page_number += 1
                time.sleep(0.5)
        else:
            time.sleep(5)

    # Parse combined products.json into more usable data structure
    for p in products:
        if p['title'] == "Container Deposit Fee":
            continue
        try:
            thumb =  p['images'][0]['src']
        except IndexError:
            thumb = None

        sku_order_limits = {}
        for tag in p['tags']:
            if tag.startswith('brand::'):
                brand = tag.split('::')[-1]
            elif tag.startswith('b2b_order_limit'):
                for sku_limit in tag.split('::')[-1].split('|'):
                    sku, limit = sku_limit.split('=')
                    sku_order_limits[sku] = limit

        sizes = []
        for v in p['variants']:
            if v['available']:
                in_stock = "In Stock"
            else:
                in_stock = "Out of Stock"

            try:
                items_per_pack = int(v['title'].split(' ')[-1].split(')')[0])
                price_per_item = round(float(v['price']) / items_per_pack, 2)
            except:
                items_per_pack = None
                price_per_item = None

            lp_cut = '%0.2f' % round(float(v['price']) * 0.85, 2)
            bcldb_cut = '%0.2f' % round(float(v['price']) * 0.15, 2)

            sizes.append({'name': v['title'],
                          'price': v['price'],
                          'in_stock':in_stock,
                          'price_per_item': price_per_item,
                          'order_limit': sku_order_limits.get(v['sku']),
                          'lp_cut': lp_cut,
                          'bcldb_cut': bcldb_cut})

        prods.append({'name': p['title'],
                      'lp': p['vendor'],
                      'brand': brand,
                      'thumb': thumb,
                      'url': base_url + '/products/' + p['handle'],
                      'created': p['created_at'],
                      'sizes': sizes,
                      'id': p['handle']})

    return prods


def main():
    products = fetch_products_from_base_url('https://www.bccannabiswholesale.com')
    retail_products = fetch_products_from_base_url('https://www.bccannabisstores.com')

    # Attempt to find the same products in the retail list to compare
    for i, prod in enumerate(products):
        retail = [x for x in filter(lambda x: x['id'] == prod['id'], retail_products)]

        for s_idx, s in enumerate(prod['sizes']):
            retail_name = s['name'].split(' (')[0]
            retail_price = None
            retail_markup = None

            for r in retail:
                retail_var = [x for x in filter(lambda x: x['name'] == retail_name, r['sizes'])]
                
                # Sometimes the retail version has or does not have a space before the g
                if len(retail_var) == 0:
                    if retail_name.find(' g') != -1:
                        retail_name = retail_name.replace(' g', 'g')
                    elif retail_name.find('g'):
                        retail_name = retail_name.replace('g', ' g')
                    retail_var = [x for x in filter(lambda x: x['name'] == retail_name, r['sizes'])]

                if len(retail_var) != 0:
                    retail_price = float(retail_var[0]['price'])
                    retail_markup = round(((float(retail_price) / s['price_per_item']) - 1) * 100)

            prod['sizes'][s_idx]['retail_price'] = retail_price
            prod['sizes'][s_idx]['retail_markup'] = retail_markup

        products[i] = prod

    prods = sorted(products, key=lambda k: k['created'], reverse=True)
    t = jinja2.Template(template)
    open('index' + '.html', 'w').write(t.render(products=prods, now=datetime.now()))
    with open('dump.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(["name", "lp", "brand", "size", "price", "price_per_item", "in_stock", "retail_price", "retail_markup", "order_limit", "lp_cut", "bcldb_cut"])
        for p in prods:
            for s in p['sizes']:
                csvwriter.writerow([p["name"], p["lp"], p["brand"], s["name"], s["price"], s["price_per_item"], s["in_stock"], s["retail_price"], s["retail_markup"], s["order_limit"], s["lp_cut"], s["bcldb_cut"]])


if __name__ == '__main__':
    main()
