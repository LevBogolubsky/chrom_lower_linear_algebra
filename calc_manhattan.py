#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from scipy.special import binom
from math import ceil

from common import ChromaticNumberLowerEstimate, do_calc


# Lemma 9
def max_fixed_distance(k_m1, k_0, k_1):
    if k_1 < k_m1 - k_0:
        return 4 * k_1 + 2 * k_0
    elif k_m1 - k_0 <= k_1 < k_m1 + k_0:
        return 2 * k_1 + 2 * k_m1
    elif k_m1 + k_0 <= k_1:
        return 4 * k_m1 + 2 * k_0


# Lemmas 10 and 11
def max_free_distance(n, d, digits):
    if digits == 3:
        return 2 * d
    elif digits == 2:
        if 2 * d <= n:
            return 2 * d
        else:
            return 2 * (n - d)


# Subsection 4.2
def least_suitable_prime_power(max_distance, prime_powers):
    for p in prime_powers:
        if 4 * p > max_distance:
            return p
    raise Exception('The least suitable prime power was not found')


def calculate_alpha_upper_estimate(n, q, d, digits, throw_out_monoms):
    result = 0

    if throw_out_monoms:
        # Theorem 3
        if digits == 3:
            result = binom(n, q - 1) * (2 ** (q - 1)) 
        elif digits == 2:
            result = binom(n, q - 1)
    else:
        # Theorem 1
        if digits == 3:
            for m in range(q):
                result += binom(n, m) * (2 ** m)
        elif digits == 2:
            for m in range(q):
                result += binom(n, m)

    return int(result)


# For graphs of types G_2, G_3
def find_chi_best_lower_estimate_free(n, digits, prime_powers, throw_out_monoms):
    best_answer = ChromaticNumberLowerEstimate()

    for d in range(n + 1):
        # Calculating the number of vertices
        if digits == 3:
            size = int(binom(n, d)) * (2 ** d)
        elif digits == 2:
            size = int(binom(n, d))

        max_distance = max_free_distance(n, d, digits)
        q = least_suitable_prime_power(max_distance, prime_powers)
        
        if d >= q - 1:

            alpha_upper = calculate_alpha_upper_estimate(n, q, d, digits, throw_out_monoms)
            chi_lower = int(ceil(float(size) / alpha_upper))

            if best_answer.estimate <= chi_lower:
                best_answer.update(chi_lower, d)

    return best_answer


# For graphs of type G_1
def find_chi_best_lower_estimate_fixed(n, digits, prime_powers, throw_out_monoms):
    best_answer = ChromaticNumberLowerEstimate()

    for k_m1 in range(1, n + 1):
        for k_1 in range(1, n - k_m1 + 1):
            k_0 = n - k_1 - k_m1

            # The number of vertices
            size = int(binom(n, k_0) * binom(n - k_0, k_1))
            max_distance = max_fixed_distance(k_m1, k_0, k_1)
            q = least_suitable_prime_power(max_distance, prime_powers)
            
            if k_m1 + k_1 >= q - 1:
                alpha_upper = calculate_alpha_upper_estimate(n, q, k_m1 + k_1, digits, throw_out_monoms)
                chi_lower = int(ceil(float(size) / alpha_upper))

                if best_answer.estimate <= chi_lower:
                    best_answer.update(chi_lower, (k_m1, k_0, k_1))

    return best_answer


if __name__ == '__main__':
    do_calc(find_chi_best_lower_estimate_fixed, find_chi_best_lower_estimate_free)
