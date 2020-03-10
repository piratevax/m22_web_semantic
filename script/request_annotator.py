#!/usr/bin/env python3

import sys, argparse
import requests

URL = "http://data.bioontology.org/annotator?"
DEBUG = False

def arg_parser():
    parser = argparse.ArgumentParser(description = "Execute REST request to annotator (https://bioportal.bioontology.org/annotator) pubmed abstract.")
    parser.add_argument("input", help = "input file name from pubmed (XML format)")
    parser.add_argument("output", help = "output file name")
    parser.add_argument("apikey", help = "mandatory key to acces and tuse the api")
    parser.add_argument("-d", "--debug", help = "execute the script in DEBUG mode", action = "store_true")
    return parser.parse_args()

def request(apikey, text, format = 'xml', **options):
    ''' Parameters

        Filtering & query behavior
            ontologies={ontology_id1,ontology_id2..,ontology_idN}
            semantic_types={semType1,semType2..,semTypeN}
            expand_semantic_types_hierarchy={true|false} // default = false. true means to use the semantic types passed in the "semantic_types" parameter as well as all their immediate children. false means to use ONLY the semantic types passed in the "semantic_types" parameter.
            expand_class_hierarchy={true|false} // default = false. used only in conjunction with "class_hierarchy_max_level" parameter; determines whether or not to include ancestors of the given class when performing an annotation.
            class_hierarchy_max_level={0..N} // default = 0. the depth of the hierarchy to use when performing an annotation.
            expand_mappings={true|false} // default = false. true means that the following manual mappings will be used in annotation: UMLS, REST, CUI, OBOXREF.
            stop_words={word1,word2..,wordN} (case insensitive)
            minimum_match_length={0..N}
            exclude_numbers={true|false} // default = false
            whole_word_only={true|false} // default = true
            exclude_synonyms={true|false} // default = false
            longest_only={true|false} // default = false. true means that only the longest match for a given phrase will be returned.

    Default stop words

        The following stop words are used by default:
            I, a, above, after, against, all, alone, always, am, amount, an, and, any, are, around, as, at, back, be, before, behind, below, between, bill, both, bottom, by, call, can, co, con, de, detail, do, done, down, due, during, each, eg, eight, eleven, empty, ever, every, few, fill, find, fire, first, five, for, former, four, from, front, full, further, get, give, go, had, has, hasnt, he, her, hers, him, his, i, ie, if, in, into, is, it, last, less, ltd, many, may, me, mill, mine, more, most, mostly, must, my, name, next, nine, no, none, nor, not, nothing, now, of, off, often, on, once, one, only, or, other, others, out, over, part, per, put, re, same, see, serious, several, she, show, side, since, six, so, some, sometimes, still, take, ten, the, then, third, this, thick, thin, three, through, to, together, top, toward, towards, twelve, two, un, under, until, up, upon, us, very, via, was, we, well, when, while, who, whole, will, with, within, without, you, yourself, yourselves
    '''
    data = {'apikey': apikey, 'text': text, 'format': format}
    if options is not None:
        for key, value in options.items():
            data.update({key: value})
    response = requests.post(URL, data = data)
    if DEBUG:
        print(response.text)
    return response.text


def main():
    global DEBUG
    args = arg_parser()
    DEBUG = args.debug
    request(args.apikey, "Amyotrophic lateral sclerosis (ALS) is a progressive and fatal neurodegenerative disorder of the human motor system. Neuroinflammation appears to be an important modulator of disease progression in ALS. Specifically, reduction of regulatory T cell (Treg) levels, along with an increase in pro-inflammatory effector T cells, macrophage activation and upregulation of co-stimulatory pathways have all been associated with a rapid disease course in ALS. Autologous infusion of expanded Tregs into sporadic ALS patients, resulted in greater suppressive function, slowing of disease progression and stabilization of respiratory function. Tecfidera (dimethyl fumarate) increases the ratio of anti-inflammatory (Treg) to proinflammatory T-cells in patients with relapsing remitting multiple sclerosis and rebalances the regulatory: inflammatory axis towards a neuroprotective phenotype. Consequently, the aim of this study was to assess the efficacy, safety, and tolerability of Tecfidera in sporadic ALS.", ontologies = 'MESH', longest_only = 'true')

if __name__ == "__main__":
    main()
