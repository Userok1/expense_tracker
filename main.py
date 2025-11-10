# C:\Users\Gwyn\Desktop\python\learning\common_python\expense_tracker

from src.expense_tracker import ExpenseTracker


def main() -> None:
    cli_tracker = ExpenseTracker()
    cli_tracker.run("./expenses.csv")


if __name__ == "__main__":
    main()