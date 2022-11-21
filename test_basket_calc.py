import unittest

from busket_calc import (
    price_str_to_float, price_float_to_str, prepare_items_dict, get_items_cost,
    calculate_discounts, prepare_result_str
)


class Testing(unittest.TestCase):

    def test_transfom_price(self):
        test_cases_str = [
            ('£1.5', 1.5),
            ('£1.50', 1.5),
            ('£1', 1.0),
            ('£0.8', 0.8)
        ]
        for test_val, result_val in test_cases_str:
            self.assertEqual(price_str_to_float(test_val), result_val)

        test_cases_val = ['1.5', '0.5', '1', '1p5', '£1.5p', '0.5p']
        for test_val in test_cases_val:
            self.assertRaises(ValueError, price_str_to_float, test_val)

        test_cases_float = [
            (0.65, '65p'),
            (1.0, '£1.00')
        ]
        for test_val, result_val in test_cases_float:
            self.assertEqual(price_float_to_str(test_val), result_val)

    def test_prepare_items_dict(self):
        test_cases = (
            (['Apples', 'BreadX3', 'SoupX6'], {'Apples': 1, 'Bread': 3, 'Soup': 6}),
            (['Apples', 'BreadX3', 'ApplesX3'], {'Apples': 4, 'Bread': 3})
        )
        for test_str, result in test_cases:
            self.assertEqual(prepare_items_dict(test_str), result)

    def test_get_items_cost(self):
        test_cases = (
            ({'Apples': 1}, ('£1.00', '90p', {'Apples': '10p'}, 0)),
            ({'Bread': 1, 'Soup': 4}, ('£3.40', '£3.00', {'Bread': '40p'}, 2)),
            ({'Bread': 2, 'Soup': 4}, ('£4.20', '£3.40', {'Bread': '80p'}, 2)),
            ({'Bread': 2, 'Soup': 3}, ('£3.55', '£3.15', {'Bread': '40p'}, 1)),
            ({'Bread': 2, 'Soup': 4}, ('£4.20', '£3.40', {'Bread': '80p'}, 2)),
            ({'Bread': 3, 'Soup': 4}, ('£5.00', '£4.20', {'Bread': '80p'}, 2)),
            ({'Milk': 1, 'Soup': 2}, ('£2.60', '£2.60', {}, 1))
        )
        for test_dict, results in test_cases:
            res_subtotal, res_total, res_disc, res_num_disc_breads = results
            subtotal, total, disc, num_disc_breads = get_items_cost(test_dict)
            self.assertEqual(res_subtotal, subtotal)
            self.assertEqual(res_total, total)
            self.assertEqual(res_disc, disc)
            self.assertEqual(res_num_disc_breads, num_disc_breads)

    def test_calculate_discounts(self):
        test_cases = (
            (('Apples', 1.0, 2, 0), 1.8),
            (('Bread', 0.8, 2, 1), 1.2),
            (('Bread', 0.8, 2, 2), 0.8),
            (('Bread', 0.8, 2, 0), 1.6)
        )
        for test_val, result_val in test_cases:
            self.assertEqual(calculate_discounts(*test_val), result_val)

    def test_prepare_result_str(self):
        test_cases = (
            (('£5.00', '£4.20', {'Bread': '80p'}, 2),
             'Subtotal: £5.00\nBread 50% off for 2 loaf(s): 80p\nTotal: £4.20'),
            (('£1.00', '90p', {'Apples': '10p'}, 0),
             'Subtotal: £1.00\nApples 10% off: 10p\nTotal: 90p'),
            (('£3.10', '£2.60', {'Apples': '10p', 'Bread': '40p'}, 1),
             ('Subtotal: £3.10\nApples 10% off: 10p\n'
              'Bread 50% off for 1 loaf(s): 40p\nTotal: £2.60')),
            (('£1.95', '£1.95', {}, 0),
             'Subtotal: £1.95 (No offers available)\nTotal price: £1.95')
        )
        for test_val, result_val in test_cases:
            self.assertEqual(prepare_result_str(*test_val), result_val)


if __name__ == '__main__':
    unittest.main()
