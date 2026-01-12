import argparse
import json
import os
import sys
from wallabaggins import api
from wallabaggins import entry
from wallabaggins.wallabag_list import print_entries
from wallabaggins.wallabag_show import html2text
from wallabaggins.conf import do_conf


def handle_add(args):
    """
    Handler function for the 'add' subcommand.
    """
    if args.verbose:
        print(f"Verbose: Adding {args.url}")
    api.api_add_entry(args.url)
    if args.verbose:
        print("Verbose: Finished adding.")


def handle_list(args):
    """
    Handler function for the 'list' subcommand.
    """
    if args.verbose:
        print(f"Verbose: Listing {args.count} entries")
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
        print(f"Verbose: Showing entry {args.entry_id}.")
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
    print(f"{title}\n{delimiter}\n{article}")
    if args.verbose:
        print("Verbose: Finished showing entry.")


def app():
    """
    Entrypoint for the CLI
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="enable verbose output"
    )
    parser.add_argument(
        "--configfile",
        type=str,
        help="specify the path to the config file to use (default: $HOME/.wallabaggins.conf)"
    )
    subparsers = parser.add_subparsers(
        title="subcommands",
        help="available subcommands"
    )

    parser_add = subparsers.add_parser("add", help="Add an entry")
    parser_add.add_argument("url", help="the url to add")
    parser_add.set_defaults(func=handle_add)

    parser_list = subparsers.add_parser("list", help="List entries")
    parser_list.add_argument("count", help="how many entries to list")
    parser_list.set_defaults(func=handle_list)

    parser_show = subparsers.add_parser("show", help="Show an entry")
    parser_show.add_argument("entry_id", help="id of the entry")
    parser_show.set_defaults(func=handle_show)

    passed_args = parser.parse_args()

    # If no subcommand is given, print help (or handle differently)
    if not hasattr(passed_args, 'func'):
        parser.print_help()
        sys.exit(1)

    if passed_args.configfile:
        do_conf(passed_args.configfile)
    else:
        do_conf()

    # Call the appropriate handler function
    passed_args.func(passed_args)


if __name__ == "__main__":
    app()
