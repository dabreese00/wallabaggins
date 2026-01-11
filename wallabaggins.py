import argparse
import api
import entry
import json
import os
from wallabag_list import print_entries
from wallabag_show import html2text
from conf import Configs, do_conf

DEFAULT_CONFIG_PATH = ".wallabaggins.conf"

def handle_add(args):
    """
    Handler function for the 'add' subcommand.
    """
    if args.verbose:
        print("Verbose: Adding {}".format(args.url))
    api.api_add_entry(args.url)
    if args.verbose:
        print("Verbose: Finished adding.")

def handle_list(args):
    """
    Handler function for the 'list' subcommand.
    """
    if args.verbose:
        print("Verbose: Listing {} entries".format(args.count))
    res = api.api_list_entries(args.count)
    res_dict = json.loads(res.response)
    entries = entry.entrylist(res_dict["_embedded"]["items"])
    print_entries(entries, False, False)
    if args.verbose:
        print("Verbose: Finished listing entries.")


def handle_show(args):
    """
    Handler function for the 'show' subcommand.
    """
    if args.verbose:
        print("Verbose: Showing entry {}.".format(args.entry_id))
    res = api.api_get_entry(args.entry_id)
    ent = entry.Entry(json.loads(res.response))
    title = ent.title
    article = ent.content
    article = html2text(article, True)
    try:
        delimiter = "".ljust(os.get_terminal_size().columns, '=')
    # piped output to file or other process
    except OSError:
        delimiter = "\n"
    output = "{0}\n{1}\n{2}".format(title, delimiter, article)
    print(output)
    if args.verbose:
        print("Verbose: Finished showing entry.")


def main():
    do_conf(DEFAULT_CONFIG_PATH)
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
    subparsers = parser.add_subparsers(title="subcommands", help="available subcommands")

    parser_add = subparsers.add_parser("add", help="Add an entry")
    parser_add.add_argument("url", help="the url to add")
    parser_add.set_defaults(func=handle_add)

    parser_list = subparsers.add_parser("list", help="List entries")
    parser_list.add_argument("count", help="how many entries to list")
    parser_list.set_defaults(func=handle_list)

    parser_show = subparsers.add_parser("show", help="Show an entry")
    parser_show.add_argument("entry_id", help="id of the entry")
    parser_show.set_defaults(func=handle_show)

    args = parser.parse_args()
    
    # If no subcommand is given, print help (or handle differently)
    if not hasattr(args, 'func'):
        parser.print_help()
        exit(1)

    # Call the appropriate handler function
    args.func(args)

if __name__ == "__main__":
    main()
