from argparse import ArgumentParser


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="The CLI expense tracker")
    subparsers = parser.add_subparsers(dest="command")

    et_parser = subparsers.add_parser("et", help="Expenses tracker")
    et_subparsers = et_parser.add_subparsers(dest="et_command")

    # END command
    end_command = subparsers.add_parser("end", help="Ends the session")

    # ADD command
    add_parser = et_subparsers.add_parser("add", 
                                            help="Adds the expense to expenses list "\
                                            "with description and amount")
    add_parser.add_argument("--description", type=str,
                            help="description of expense")
    add_parser.add_argument("--amount", type=str,
                            help="Amount of money to spand on expense")
    
    # UPDATE command
    update_parser = et_subparsers.add_parser("update", help="Updates the expense by ID")
    update_parser.add_argument("id", help="Expense ID")
    update_parser.add_argument("--description", help="New description for expense")
    update_parser.add_argument("--amount", help="New amount for expense")

    # DELETE command
    delete_parser = et_subparsers.add_parser("delete", help="Deletes expense by id")
    delete_parser.add_argument("id", type=int,
                                help="Id of deleted expense")
    
    # PRINT command
    prnt_parser = et_subparsers.add_parser("list", help="prints all expense list")

    # SUMMARY command
    summary_parser = et_subparsers.add_parser("summary",
                                                help="Summary of all expenses")
    summary_parser.add_argument("--month", help="Month to return summary for")

    # EXPORT command
    export_parser = et_subparsers.add_parser("export",
                                                help="Exports data to csv file")
    export_parser.add_argument("filename",
                                help="Filename of csv file to export data")
    
    return parser