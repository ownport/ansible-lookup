from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
import json
import argparse

from lookups.lookup import LOOKUP_ACTIONS


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='actions', help='Loolup actions handler')

    parsers = {}
    for action in LOOKUP_ACTIONS:
        parsers[action] = subparsers.add_parser(action, help='Action: %s' % action)
        parsers[action].add_argument('--terms', help='lookup terms as JSON string')
        parsers[action].set_defaults(action=action)

    args = parser.parse_args()

    action_module_name = LOOKUP_ACTIONS.get(args.action)
    if not action_module_name:
        print('[ERROR] Unknown action, %s' % args.action)
        sys.exit(1)

    try:
        action_module = __import__(action_module_name, globals(), locals(), 'LookupModule')
    except ImportError as err:
        print('[ERROR] Cannot import action module, %s' % action_module_name)
        sys.exit(1)

    if not args.terms:
        parsers[args.action].print_help()
        sys.exit(1)

    try:
        terms = json.loads(args.terms)
    except ValueError as err:
        print('[ERROR] Cannot parse the terms in JSON format: %s' % args.terms)
        sys.exit(1)

    print(json.dumps(action_module.LookupModule().run(terms=terms)))

cli()