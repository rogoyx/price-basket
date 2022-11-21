import argparse


PRICES_DICT = {
    'Apples': '£1.00',
    'Soup': '65p',
    'Bread': '80p',
    'Milk': '£1.30',
}
DISCOUNTES_ITEMS_PERC = {
    'Apples': 0.1, # per 1 bag
    'Bread': 0.5, # per 1 loaf when buy 2 Soup
}
NUM_SOUPS_FOR_DISCOUNT = 2

parser = argparse.ArgumentParser()
parser.add_argument('--price_basket', default=None, nargs='+')
args = parser.parse_args()

def prepare_items_dict(price_basket_list):
    '''Parse input string and transform it to a dict'''
    items = [x.split('X') for x in price_basket_list]
    items_dict = {}
    for pair in items:
        if len(pair) == 1:
            # case when num of items didn't provided explicitly
            items_dict[pair[0]] = items_dict.get(pair[0], 0) + 1
        else:
            items_dict[pair[0]] = items_dict.get(pair[0], 0) + int(pair[1])
    return items_dict

def price_str_to_float(price_str):
    '''Transform price in string to float'''
    if (price_str[-1] == 'p'
        and '£' not in price_str
        and not '.' in price_str
        and len(price_str) <= 3):
        # for price in pennies
        return float(price_str.rstrip('p')) / 100
    if price_str[0] == '£' and 'p' not in price_str:
        # for price in pounds
        return float(price_str.lstrip('£'))
    raise ValueError('Price in wrong format.')

def price_float_to_str(price_float):
    '''Transform price in float to string'''
    if int(price_float) == 0:
        # rounding to avoid 0.2 + 0.1 float problem
        return f'{int(round(price_float, 2)*100)}p'
    return f'£{round(price_float, 2):.2f}'

def get_items_cost(items_dict):
    '''Calculate total and subtotal cost of items with applied discounts'''
    discounts_dict = {}
    subtotal_cost = 0
    total_cost = 0

    num_soups = items_dict.get('Soup', 0)
    num_discounted_breads = num_soups // NUM_SOUPS_FOR_DISCOUNT

    for item_name, num_items in items_dict.items():
        # get item price from dict
        item_price = price_str_to_float(PRICES_DICT[item_name])

        # calculate undiscounted cost
        item_cost = item_price * num_items
        subtotal_cost += item_cost

        # calculate discounted cost
        if item_name in DISCOUNTES_ITEMS_PERC:
            item_cost_discounted = calculate_discounts(
                item_name, item_price, num_items, num_discounted_breads)
            discount_size = item_cost - item_cost_discounted
            if discount_size > 0:
                discounts_dict[item_name] = price_float_to_str(discount_size)
            item_cost = item_cost_discounted

        total_cost += item_cost

    return (price_float_to_str(subtotal_cost), price_float_to_str(total_cost),
        discounts_dict, num_discounted_breads)

def calculate_discounts(
    item_name, item_price, num_items, num_discounted_breads=0
):
    '''Apply current discounts.
       For bread apply logic:
       Buy 2 tins of soup and get a loaf of bread for half price.
    '''
    if item_name == 'Bread' and num_discounted_breads > 0:
        discounted_item_price = (1 - DISCOUNTES_ITEMS_PERC[item_name]) \
                                * item_price
        num_discounted_breads = min(num_discounted_breads, num_items)
        num_undiscounted_breads = num_items - num_discounted_breads
        # rounding to avoid 0.2 + 0.1 float problem
        return round(num_discounted_breads * discounted_item_price
                    + num_undiscounted_breads * item_price, 2)
    if item_name == 'Bread' and num_discounted_breads == 0:
        # undiscounted cost
        return num_items * item_price
    return num_items * (1 - DISCOUNTES_ITEMS_PERC[item_name]) * item_price

def prepare_result_str(subtotal, total, discounts, num_disc_breads=0):
    '''Apply required formatting for calculated result'''
    _discnt_str = '\n'
    _total_str = ''
    if discounts:
        for item_name, item_disc in discounts.items():
            if item_name == 'Apples':
                disc_size = f' {int(DISCOUNTES_ITEMS_PERC[item_name]*100)}% off'
            elif item_name == 'Bread' and num_disc_breads > 0:
                disc_size = (f' {int(DISCOUNTES_ITEMS_PERC[item_name]*100)}%'
                             f' off for {num_disc_breads} loaf(s)')
            else:
                disc_size = ''
            _discnt_str += f'{item_name}{disc_size}: {item_disc}\n'
    else:
        _discnt_str = ' (No offers available)\n'
        _total_str = ' price'
    return (
        f'Subtotal: {subtotal}'
        f'{_discnt_str}'
        f'Total{_total_str}: {total}'
    )

def main():
    items_dict = prepare_items_dict(args.price_basket)
    print(prepare_result_str(*get_items_cost(items_dict)))

if __name__ == '__main__':
    main()
