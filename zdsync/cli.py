import argparse
import sys

from .synchronizer import (
    BrandSynchronizer,
    GroupSynchronizer,
    MacroSynchronizer,
    TicketFieldSynchronizer,
    TicketFormSynchronizer
)


def main():
    parser = argparse.ArgumentParser(
        description="Sync Production Zendesk Environment to the Sandbox"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Create records in the Sandbox"
    )
    parser.add_argument(
        "--brands",
        action="store_true",
        help="Operate on Brands"
    )
    parser.add_argument(
        "--groups",
        action="store_true",
        help="Operate on Groups"
    )
    parser.add_argument(
        "--ticket-fields",
        action="store_true",
        help="Operate on TicketFields"
    )
    parser.add_argument(
        "--ticket-forms",
        action="store_true",
        help="Operate on TicketForms"
    )
    parser.add_argument(
        "--macros",
        action="store_true",
        help="Operate on Macros"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Operate on all object types"
    )
    args = parser.parse_args()

    if args.brands or args.all:
        BrandSynchronizer().run(execute=args.execute)
    if args.groups or args.all:
        GroupSynchronizer().run(execute=args.execute)
    if args.ticket_fields or args.all:
        TicketFieldSynchronizer().run(execute=args.execute)
    if args.ticket_forms or args.all:
        TicketFormSynchronizer().run(execute=args.execute)
    if args.macros or args.all:
        MacroSynchronizer().run(execute=args.execute)


if __name__ == "__main__":
    sys.exit(main())
