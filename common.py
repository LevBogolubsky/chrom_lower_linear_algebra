#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

DEFAULT_PRIME_POWERS_FILENAME = 'prime_powers.tsv'
DEFAULT_LOWEST_SPACE_DIMENSIONALITY = 4
DEFAULT_HIGHEST_SPACE_DIMENSIONALITY = 69


class ChromaticNumberLowerEstimate(object):
    def __init__(self):
        self.estimate = 1
        self.params = None

    def update(self, outer_estimate, outer_params):
        self.estimate = outer_estimate
        self.params = outer_params


def load_prime_powers(filename):
    return [int(line.strip('\n')) for line in open(filename)]


def format_max(a, b, c):
    best = max(a, b, c)

    def mark(x):
        if x == best:
            return '\\textbf{' + str(x) + '}'
        else:
            return x

    return mark(a), mark(b), mark(c)


def get_command_line_args():
    parser = ArgumentParser()

    parser.add_argument(
        '-p',
        '--prime-powers',
        help='File with prime powers, one prime power per line',
        default=DEFAULT_PRIME_POWERS_FILENAME
    )
    parser.add_argument(
        '-lo',
        '--lowest',
        help='Lowest space dimensionality',
        type=int,
        default=DEFAULT_LOWEST_SPACE_DIMENSIONALITY
    )
    parser.add_argument(
        '-hi',
        '--highest',
        help='Highest space dimensionality',
        type=int,
        default=DEFAULT_HIGHEST_SPACE_DIMENSIONALITY
    )
    args = parser.parse_args()
    return args


def do_calc(find_chi_best_lower_estimate_fixed, find_chi_best_lower_estimate_free):
    args = get_command_line_args()
    prime_powers = load_prime_powers(args.prime_powers)

    for n in range(args.lowest, args.highest + 1):
        columns = []

        columns.append(find_chi_best_lower_estimate_fixed(n, 3, prime_powers, throw_out_monoms=False))
        columns.append(find_chi_best_lower_estimate_free(n, 3, prime_powers, throw_out_monoms=False))
        columns.append(find_chi_best_lower_estimate_free(n, 2, prime_powers, throw_out_monoms=False))

        columns.append(find_chi_best_lower_estimate_fixed(n, 3, prime_powers, throw_out_monoms=True))
        columns.append(find_chi_best_lower_estimate_free(n, 3, prime_powers, throw_out_monoms=True))
        columns.append(find_chi_best_lower_estimate_free(n, 2, prime_powers, throw_out_monoms=True))

        template = '{0} & {1} & {2} & {3} & {4} & {5} & {6} & {7} & {8} & {9} & {10} & {11} & {12}\\\ \\hline'

        chi_0, chi_1, chi_2 = format_max(columns[0].estimate, columns[1].estimate, columns[2].estimate)
        chi_3, chi_4, chi_5 = format_max(columns[3].estimate, columns[4].estimate, columns[5].estimate)

        row = [
            n,
            chi_0,
            columns[0].params,
            chi_1,
            columns[1].params,
            chi_2,
            columns[2].params,
            chi_3,
            columns[3].params,
            chi_4,
            columns[4].params,
            chi_5,
            columns[5].params
        ]

        print(template.format(*row))
