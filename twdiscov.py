"""A module for dicovering raw two-level rules from a set of carefully chosen examples

Examples, contexts and rules are treated in terms of strings without any
finite-state machinery or rule compilation.  Examples and contexts are
space separated sequences of pair-symbols. 

© Kimmo Koskenniemi, 2017-2018. Free software under the GPL 3 or later.
"""

import sys
import re
import cfg
import twexamp

pair_symbols_for_input = {}   # key: input symbol, value: set of pair symbols
pair_symbols_for_output = {}

def relevant_contexts(pair_symbol):
    """Select positive and negative contexts for a given pair-symbol
    
    pair_symbol -- the pair-symbol for which the contexts are selected
    
    returns a tuple of:
    
    pos_context_set -- a set of contexts in the examples where the
    pair_symbol occurs
    
    neg_context_set -- a set of contexts where the input-symbol of the
    pair_symbol occurs with another output-symbol but so that there is
    no example in the example_set where the pair_symbol occurs in such a
    context
    """
    input_symbol, output_symbol = cfg.pairsym2sympair(pair_symbol)
    positive_context_set = set()
    negative_context_set = set()
    pairsymlist = [re.sub(r"([}{])", r"\\\1", psym)
                   for psym
                   in pair_symbols_for_input[input_symbol]]
    # print("pairsymlist:", pairsymlist) ##
    pattern = re.compile("|".join(pairsymlist))
    for example in cfg.example_set:
        for m in pattern.finditer(example):
            i1 = m.start()
            i2 = m.end()
            # print('"' + example[0:i1] +'"', '"' + example[i2:] + '"') ##
            left_context = ".#. " + example[0:i1-1]
            centre = example[i1:i2]
            if i2 >= len(example):
                right_context = ".#."
            else:
                right_context = example[i2+1:] + " .#."
            context = (left_context, right_context)
            # print(centre, context) ##
            if centre == pair_symbol:
                positive_context_set.add(context)
            else:
                negative_context_set.add(context)
    negative_context_set = negative_context_set - positive_context_set
    return positive_context_set, negative_context_set
    
def ppcontexts(ctxs, title):
    """Print a list of context for tracing and debugging"""
    print(title)
    for lc, rc in sorted(ctxs):
        print(lc, "_", rc)

def shorten_contexts(contexts, left_length, right_length):
    if cfg.verbosity >= 25:
        print("left and right length:", left_length, right_length)
        ppcontexts(contexts, "contexts as given to shorten_contexts()")
    new_contexts = set()
    for left_context, right_context in contexts:
        left_lst = left_context.split(" ")
        start = max(0, len(left_lst) - left_length)
        new_lc = " ".join(left_lst[start:])
        # print("start:", start, "new_lc:", new_lc)
        right_lst = right_context.split(" ")
        new_rc = " ".join(right_lst[0:right_length])
        new_contexts.add((new_lc, new_rc))
    return(new_contexts)

def minimal_contexts(pair_symbol):
    """Shortens the left and right contexts step by step
    
    Finds shortest contexts which accept correct occurrences of
    pair_symbol and still reject the incorrect occurrences of it.
    
    pair_symbol -- a pair-symbol, e.g. '{aä}:a' for which the optimal
    contexts are computed
    
    returns a tuple: (positive_context, negative_contexts)
    """
    pos_contexts, neg_contexts = relevant_contexts(pair_symbol)
    if cfg.verbosity >= 25:
        ppcontexts(pos_contexts, "positive contexts for " + pair_symbol)
        ppcontexts(neg_contexts, "negative contexts for " + pair_symbol)
    # find maximum lengths (in psyms) of left and right contexts
    left_len = 0
    right_len = 0
    for left_context, right_context in pos_contexts:
        lcount = left_context.count(" ")
        if lcount >= left_len: left_len = lcount + 1
        rcount = right_context.count(" ")
        if rcount >= right_len: right_len = rcount + 1
    for left_context, right_context in neg_contexts:
        lcount = left_context.count(" ")
        if lcount >= left_len: left_len = lcount + 1
        rcount = right_context.count(" ")
        if rcount >= right_len: right_len = rcount + 1

    # shorten the contexts stepwise while the positive and
    # the negative contexts stay disjoint
    p_contexts = pos_contexts.copy()
    n_contexts = neg_contexts.copy()
    left_incomplete = True
    right_incomplete = True
    while left_incomplete or right_incomplete:
        # print(left_len, right_len) ##
        if left_incomplete and left_len > 0:
            new_p_contexts = shorten_contexts(p_contexts, left_len-1, right_len)
            new_n_contexts = shorten_contexts(n_contexts, left_len-1, right_len)
            if new_p_contexts.isdisjoint(new_n_contexts):
                # print("still disjoint") ##
                p_contexts = new_p_contexts
                n_contexts = new_n_contexts
                left_len = left_len - 1
            else:
                if cfg.verbosity >= 25:
                    print("left side now complete") ##
                    ppcontexts(new_p_contexts & new_n_contexts,
                               "intersection of new pos and neg contexts")
                left_incomplete = False
        elif right_incomplete and right_len > 0:
            new_p_contexts = shorten_contexts(p_contexts, left_len, right_len-1)
            new_n_contexts = shorten_contexts(n_contexts, left_len, right_len-1)
            if new_p_contexts.isdisjoint(new_n_contexts):
                # print("still disjoint") ##
                p_contexts = new_p_contexts
                n_contexts = new_n_contexts
                right_len = right_len - 1
            else:
                # print("left side now complete") ##
                right_incomplete = False
        else:
            break
    if cfg.verbosity >= 25:
        ppcontexts(p_contexts, "positive contexts")
        ppcontexts(n_contexts, "negative contexts")
    return p_contexts, n_contexts

def print_rule(pair_symbol, operator, contexts):
    """Prints one rule"""
    print(pair_symbol, operator)
    for lc, rc in contexts:
        print("   ", lc, "_", rc, ";")

if __name__ == "__main__":
    import argparse
    arpar = argparse.ArgumentParser("python3 twdiscov.py")
    arpar.add_argument("examples", help="example pair strings file",
                       default="test.pstr")
    arpar.add_argument("-s", "--symbol",
                        help="input symbol for which to find rules",
                        default="")
    arpar.add_argument("-v", "--verbosity",
                       help="level of  diagnostic output",
                       type=int, default=0)
    args = arpar.parse_args()

    cfg.verbosity = args.verbosity
    
    twexamp.read_examples(filename=args.examples, build_fsts=False)
    print("--- all examples read in ---")
    
    for insym in cfg.input_symbol_set:
        pair_symbols_for_input[insym] = set()
    for insym, outsym in cfg.symbol_pair_set:
        pair_symbol = cfg.sympair2pairsym(insym, outsym)
        pair_symbols_for_input[insym].add(pair_symbol)

    if args.symbol:
        pair_set = pair_symbols_for_input[args.symbol]
        pair_lst = []
        for pairsym in pair_set:
            insym, outsym = cfg.pairsym2sympair(pairsym)
            pair_lst.append((insym, outsym))
        if cfg.verbosity >= 10:
            print("pair_lst:", pair_lst)
    else:
        pair_lst = sorted(cfg.symbol_pair_set)

    for insym, outsym in pair_lst:
        if len(pair_symbols_for_input[insym]) <= 1:
            continue
        pair_symbol = cfg.sympair2pairsym(insym, outsym)
        pos_contexts, neg_contexts = minimal_contexts(pair_symbol)
        if len(pos_contexts) <= len(neg_contexts):
            print_rule(pair_symbol, "=>", pos_contexts)
        else:
            print_rule(pair_symbol, "/<=", neg_contexts)
