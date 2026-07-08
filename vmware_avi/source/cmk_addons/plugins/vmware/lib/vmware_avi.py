#!/usr/bin/env python3
#-*- encoding: utf-8
#
# Author : Alexander Vogel (alexander.vogel.2305@gmail.com)
# Date   : 2026-07-07
# License: GNU General Public License v2
#
# Lib: VMware Avi Load Balancer


import ast
import itertools

from cmk.agent_based.v2 import State, Result


def parse_python_literal(string_table):
    flat = list(itertools.chain.from_iterable(string_table))

    if not flat:
        return {}

    if len(flat) == 1:
        return ast.literal_eval(flat[0])

    return [ast.literal_eval(line) for line in flat if line.strip()]


def yield_mapped_result(value, mapping, label):
    if value is None:
        yield Result(
            state=State(0),
            summary=f"{label}: N/A",
        )
        return

    if value in mapping:
        yield Result(
            state=State(mapping[value]['cmk']),
            summary=f"{label}: {mapping[value]['str']}",
        )
    else:
        yield Result(
            state=State(3),
            summary=f"{label}: {value}",
        )
