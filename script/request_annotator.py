#!/usr/bin/env python3

import sys, argparse, re
import requests
import urllib.request, urllib.error, urllib.parse
from lxml import etree
import json
from pprint import pprint

URL = "http://data.bioontology.org/annotator?"
DEBUG = False

def arg_parser():
    parser = argparse.ArgumentParser(description = "Execute REST request to annotator ( https://bioportal.bioontology.org/annotator ) pubmed abstract.")
    semanticGroup = parser.add_argument_group()
    parser.add_argument("input", help = "input file name from pubmed (XML format)")
    parser.add_argument("-o", "--output", help = "output file name", default = "output.arff")
    parser.add_argument("apikey", help = "mandatory key to access and use the REST API")
    parser.add_argument("--ontologies", help = "ontologies ID(s)", nargs = "+")
    semanticGroup.add_argument("--semantic-types", help = "semantic type(s)", nargs = "+")
    semanticGroup.add_argument("--semantic-type-hierarchy", help = 'true means to use the semantic types passed in the "semantic_types" parameter as well as all their immediate children. false means to use ONLY the semantic types passed in the "semantic_types" parameter -- [default: False]', action = "store_true", default = False)
    parser.add_argument("--expand-class-hierarchy", help = 'used only in conjunction with "class_hierarchy_max_level" parameter; determines whether or not to include ancestors of the given class when performing an annotation -- [default: False]', action = "store_true",default = False)
    parser.add_argument("--class-hierarchy-max-level", type = int, help = 'the depth of the hierarchy to use when performing an annotation, class_hierarchy_max_level = {0..N} -- [default: 0]', default = 0)
    parser.add_argument("--expand-mappings", help = 'true means that the following manual mappings will be used in annotation: UMLS, REST, CUI, OBOXREF -- [default: False]', action = "store_true", default = False)
    parser.add_argument("--stop-words", help = 'list of stop words (case sensitive)', type = str, nargs = "+")
    parser.add_argument("--minimum-match-length", help = "minimum match length {0..N}", type = int)
    parser.add_argument("--exclude-numbers", help = "exclude numbers -- [default: False]", action = "store_true", default = False)
    parser.add_argument("--whole-word-only", help = "whole word only -- [default: True]", action = "store_false", default = True)
    parser.add_argument("--exlcude-synonyms", help = "exclude synonyms-- [default: False]", action = "store_true", default = False)
    parser.add_argument("--longest_only", help = "true means that only the longest match for a given phrase will be returned -- [default: False]", action = "store_true", default = False)
    parser.add_argument("-d", "--debug", help = "execute the script in DEBUG mode", action = "store_true")
    return parser.parse_args()

def request(apikey, text, format = 'json', **options):
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
    return json.loads(response.text)

def get_request_list(filename):
    tree = etree.parse(filename)
    xpath = "//Article"
    title_xpath = "ArticleTitle"
    abstract_xpath = "Abstract/AbstractText"
    request_list = []

    for article in tree.xpath(xpath):
        req = ""
        req += article.findtext(title_xpath)
        try:
            req += article.findtext(abstract_xpath)
        except TypeError:
            request_list.append(req)
            continue
        request_list.append(req)            

    return request_list

def print_annotations(annotations, apikey, get_class=True):
    for result in annotations:
        class_details = result["annotatedClass"]
        if get_class:
            try:
                class_details = get_json(result["annotatedClass"]["links"]["self"], apikey)
            except urllib.error.HTTPError:
                print(f"Error retrieving {result['annotatedClass']['@id']}")
                continue
        print("Class details")
        print("\tid: " + class_details["@id"])
        print("\tprefLabel: " + class_details["prefLabel"])
        print("\tontology: " + class_details["links"]["ontology"])

        print("Annotation details")
        for annotation in result["annotations"]:
            print("\tfrom: " + str(annotation["from"]))
            print("\tto: " + str(annotation["to"]))
            print("\tmatch type: " + annotation["matchType"])

        if result["hierarchy"]:
            print("\n\tHierarchy annotations")
            for annotation in result["hierarchy"]:
                try:
                    class_details = get_json(annotation["annotatedClass"]["links"]["self"], apikey)
                except urllib.error.HTTPError:
                    print(f"Error retrieving {annotation['annotatedClass']['@id']}")
                    continue
                pref_label = class_details["prefLabel"] or "no label"
                print("\t\tClass details")
                print("\t\t\tid: " + class_details["@id"])
                print("\t\t\tprefLabel: " + class_details["prefLabel"])
                print("\t\t\tontology: " + class_details["links"]["ontology"])
                print("\t\t\tdistance from originally annotated class: " + str(annotation["distance"]))
        print("\n\n")

def get_json(url, apikey):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + apikey)]
    return json.loads(opener.open(url).read())

def request_list(args, requests):
    annotations = []

    for req in requests:
        annotation = request(args.apikey, req, longest_only = 'true')
        # print(annotation)
        # print_annotations(annotation, args.apikey)
        annotations.append(annotation)

    return annotations

def get_words_list(annotations, apikey, get_class = True):
    words_list = []

    for annotation in annotations:
        words = []
        for result in annotation:
            for anno in result["annotations"]:
                word = anno["text"].lower()
                word = "-".join(re.split("[' ]", word))
                if word not in words:
                    words.append(word)
        words_list.append(words)

    return words_list

def write_arff(words_list, sep = ",", eol = "\n", filename = "output.arff"):
    arff_to_write = "@relation annotator{}".format(eol)
    flatten_unique_words_list = list(set([y for x in words_list for y in x]))
    
    print("Writing file")
    arff_to_write += "@attribute class {{{}}}".format(sep.join(str(x) for x in range(1, len(words_list) + 1)))
    arff_to_write += eol
    arff_to_write += "@attribute annot {{{}}}".format(sep.join(x for x in flatten_unique_words_list))
    arff_to_write += eol
    arff_to_write += "@attribute bool {{true{} false}}{}".format(sep, eol)
    arff_to_write += "@data{}".format(sep)

    ind = 1
    for x in words_list:
        for word in flatten_unique_words_list:
            arff_to_write += "{}{}{}{}".format(ind, sep, word, sep)
            if word in x:
                arff_to_write += "true{}".format(eol)
            else:
                arff_to_write += "false{}".format(eol)
        ind += 1
    arff_to_write += eol

    fd = open(filename, "w")
    fd.write(arff_to_write)
    fd.close()
    print(" file wrote : {}".format(filename))

def main():
    global DEBUG
    args = arg_parser()
    DEBUG = args.debug

    print("Formatting requests")
    requests = get_request_list(args.input)
    print("Requesting Annotator")
    annotations = request_list(args, requests)
    print("Formatting Annotator results")
    words_list = get_words_list(annotations, args.apikey)
    write_arff(words_list, filename = args.output)

    # answer = request(args.apikey, "Amyotrophic lateral sclerosis (ALS) is a progressive and fatal neurodegenerative disorder of the human motor system. Neuroinflammation appears to be an important modulator of disease progression in ALS. Specifically, reduction of regulatory T cell (Treg) levels, along with an increase in pro-inflammatory effector T cells, macrophage activation and upregulation of co-stimulatory pathways have all been associated with a rapid disease course in ALS. Autologous infusion of expanded Tregs into sporadic ALS patients, resulted in greater suppressive function, slowing of disease progression and stabilization of respiratory function. Tecfidera (dimethyl fumarate) increases the ratio of anti-inflammatory (Treg) to proinflammatory T-cells in patients with relapsing remitting multiple sclerosis and rebalances the regulatory: inflammatory axis towards a neuroprotective phenotype. Consequently, the aim of this study was to assess the efficacy, safety, and tolerability of Tecfidera in sporadic ALS.", ontologies = 'MESH', longest_only = 'true')
    # print(answer)

if __name__ == "__main__":
    main()
