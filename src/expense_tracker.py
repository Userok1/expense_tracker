from datetime import datetime
from argparse import ArgumentParser, Namespace
import csv
import os
from tabulate import tabulate
from typing import Any

from src.parser import create_parser


class Expense:
    def __init__(self, date: datetime | str | None, 
                 description: str,
                 amount: str,
                 expns_id: int | None = None
    ):
        self.id = expns_id
        self.date = date
        self.description = description
        self.amount = amount


class ExpenseTracker:
    _fieldnames = ['id', 'date', 'description', 'amount']


    def run(self, file_path: str) -> None:
        self._ensure_file_exists(file_path)
        try:
            while True:
                try:
                    user_input = input(">> ")
                    command = user_input.strip()
                    ExpenseTracker.__handle_command(command)
                except SystemExit as se:
                    print(f"{se}")
                    continue
        except (KeyboardInterrupt, ValueError):
            print("\nEnd of program")


    @classmethod
    def _export_to_csv(cls, filename: str) -> None:
        data = cls._read_from_csv()

        if not os.path.exists(filename):
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, ['id', 'date', 'description', 'amount'])
                writer.writerows(data)
            print("Data exported successfully")
        else:
            print("File already exists")


    @classmethod
    def __handle_command(cls, command: str) -> None:
        from src.utils import is_positive

        args: Namespace = cls.__parse_command(command)
        
        if args.command == "end":
            raise ValueError
        elif args.command == "et":

            if args.et_command == "add":
                description, amount = args.description, args.amount
                if is_positive(amount):
                    cls._add(description, amount)
                else:
                    raise SystemExit("Number should not be negative")
            
            elif args.et_command == "list":
                cls._print_list()
            
            elif args.et_command == "update":
                expns_id = args.id
                description = args.description
                amount = args.amount
                if is_positive(amount):
                    cls._update(expns_id, description, amount)
                else:
                    raise SystemExit("Number should not be negative")

            elif args.et_command == "delete":
                expns_id = args.id
                cls._delete(expns_id)

            elif args.et_command == "summary":
                if args.month is not None:
                    cls._summary(args.month)
                else:
                    cls._summary()
            
            elif args.et_command == "export":
                cls._export_to_csv(args.filename)

        else:
            raise SystemExit("No such command")


    @classmethod
    def _add(cls, description: str, amount: str) -> None:
        data: list[dict[str, Any]] = cls._read_from_csv()
        
        expense = Expense(
            datetime.now().strftime("%Y-%d-%m"),
            description,
            "$" + amount,
            expns_id=cls.__increment_id(),
        )
        
        cls._save_to_csv(data, expense)
        print(f"Expense added successfully (ID: {expense.id})")


    @classmethod
    def _update(cls, expns_id: int, description: str, amount: str) -> None:
        data: list[dict[str, Any]] = cls._read_from_csv()
        expense = cls.__find_expense(data, expns_id)
        data.remove(expense)
        
        expense['description'] = description
        expense['amount'] = amount

        expense = Expense(
            expns_id=int(expense['id']),
            date=expense['date'],
            description=expense['description'],
            amount="$" + expense['amount'],
        )
        cls._save_to_csv(data, expense)
        print(f"Expense updated successfully (ID: {expense.id})")


    @classmethod
    def _delete(cls, expns_id: int) -> None:
        data: list[dict[str, Any]] = cls._read_from_csv()

        expense = cls.__find_expense(data, expns_id=expns_id)
        data.remove(expense)
        cls._save_to_csv(data)
        print(f"Expense deleted successfully (ID: {expns_id})")


    @classmethod
    def __find_expense(cls, data: dict[str, Any], expns_id: int) -> dict[str, Any]:
        for d in data[1:]:
            if d.get("id") == str(expns_id):
                return d
        raise SystemExit("Expense not found")
    

    @classmethod
    def _summary(cls, month: str | None = None) -> None:
        
        months = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December"
        }

        data: list[dict[str, Any]] = cls._read_from_csv()
        amounts: list[int] | int = 0
        if month is not None:
            amounts = [int(d["amount"][1:]) for d in data[1:] if d["date"][-2:] == month]
            total = sum(amounts)
            print(f"Total expenses for {months[month]}: {total}$")
            return
        else:
            amounts = [int(d["amount"][1:]) for d in data[1:]]
            total = sum(amounts)
            print(f"Total expenses: {total}$")
            return


    @classmethod
    def _print_list(cls) -> None:
        data: list[dict[str, Any]] = cls._read_from_csv()

        # tabulate for pretty printing
        pp = tabulate(data, headers="firstrow")
        print("\n\n" + pp + "\n\n")


    @classmethod
    def __increment_id(cls) -> int:
        data: list[dict[str, Any]] = cls._read_from_csv()
        # Searching for biggest id to increment one for new expense
        if len(data) <= 1:
            return 1
        biggest_id = max(data[1:], key=lambda expns: expns["id"])
        expense_id = int(biggest_id.get("id", 0)) + 1
        return expense_id


    @classmethod
    def _ensure_file_exists(cls, file_path: str) -> None:
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, cls._fieldnames)
                writer.writeheader()


    @classmethod
    def _save_to_csv(cls, expense_lst: list[dict[str, Any]], 
                     expense: Expense | None = None) -> None:
        with open("expenses.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, cls._fieldnames)
            if len(expense_lst) == 0:
                writer.writeheader()
            if expense is not None:
                expense_lst.insert(expense.id, vars(expense))
            writer.writerows(expense_lst)


    @classmethod
    def _read_from_csv(cls) -> list[dict[str, Any]]:
        with open("expenses.csv", 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, fieldnames=cls._fieldnames)
            result_list = [expense for expense in reader]

            return result_list


    @classmethod
    def __parse_command(cls, command) -> Namespace:
        import shlex

        parser: ArgumentParser = create_parser() 
        command = shlex.split(command)
        args = parser.parse_args(command)

        return args