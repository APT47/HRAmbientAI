"""Simple CLI to test HiBob API connectivity — no Claude involved.

Usage:
    python -m hr_ambient_ai.hibob_cli list_ids
    python -m hr_ambient_ai.hibob_cli get_employee <id>
    python -m hr_ambient_ai.hibob_cli search <name_or_email>
    python -m hr_ambient_ai.hibob_cli list_fields
    python -m hr_ambient_ai.hibob_cli update <employee_id> <field_path> <value>
"""

import argparse
import json
import sys

from hr_ambient_ai.hibob.client import HiBobClient


def cmd_list_ids(client: HiBobClient, _args: argparse.Namespace) -> None:
    employees = client.search_employees()
    if not employees:
        print("No employees found.")
        return
    print(f"{'ID':<30} {'Display Name':<30} Email")
    print("-" * 80)
    for emp in employees:
        print(
            f"{emp.get('id', ''):<30} "
            f"{emp.get('displayName', ''):<30} "
            f"{emp.get('email', '')}"
        )


def cmd_get_employee(client: HiBobClient, args: argparse.Namespace) -> None:
    data = client.get_employee(args.employee_id)
    print(json.dumps(data, indent=2))


def cmd_search(client: HiBobClient, args: argparse.Namespace) -> None:
    results = client.search_employees(email=args.query)
    if not results:
        print("No results.")
        return
    print(json.dumps(results, indent=2))


def cmd_list_fields(client: HiBobClient, _args: argparse.Namespace) -> None:
    fields = client.list_fields()
    print(f"{'Path':<40} {'Name':<35} Type")
    print("-" * 90)
    for f in fields:
        print(
            f"{f.get('path', ''):<40} "
            f"{f.get('name', ''):<35} "
            f"{f.get('type', '')}"
        )


def cmd_update(client: HiBobClient, args: argparse.Namespace) -> None:
    confirm = input(
        f"Update employee '{args.employee_id}' — set '{args.field_path}' = '{args.value}'? [y/N] "
    ).strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return
    result = client.update_field(args.employee_id, args.field_path, args.value)
    print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="HiBob API test CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list_ids", help="List all employees (ID, name, email)")

    p_get = sub.add_parser("get_employee", help="Get full employee profile")
    p_get.add_argument("employee_id")

    p_search = sub.add_parser("search", help="Search by name or email")
    p_search.add_argument("query")

    sub.add_parser("list_fields", help="List all HiBob field paths")

    p_update = sub.add_parser("update", help="Update an employee field")
    p_update.add_argument("employee_id")
    p_update.add_argument("field_path", help="e.g. work.title")
    p_update.add_argument("value")

    args = parser.parse_args()

    try:
        client = HiBobClient()
    except KeyError as e:
        print(f"Missing environment variable: {e}. Check your .env file.")
        sys.exit(1)

    dispatch = {
        "list_ids": cmd_list_ids,
        "get_employee": cmd_get_employee,
        "search": cmd_search,
        "list_fields": cmd_list_fields,
        "update": cmd_update,
    }

    try:
        dispatch[args.command](client, args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
