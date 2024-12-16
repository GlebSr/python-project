import uuid
from typing import Optional, List
from backend.app.database import MongoDB
from backend.app.models.money import CreateCategory, CreateIncome, Income, UpdateIncome, CreateExpense, Expense, UpdateExpense, Category


class FinanceCRUD:
    def __init__(self, db: MongoDB):
        self.income_collection = db.get_collection("incomes")
        self.expense_collection = db.get_collection("expenses")
        self.category_collection = db.get_collection("categories")

    # ------------------- Доходы -------------------

    async def create_income(self, user_id: str, income: CreateIncome) -> Optional[str]:
        income_data = income.dict()
        income_data["id"] = str(uuid.uuid4())
        income_data["user_id"] = user_id
        result = await self.income_collection.insert_one(income_data)
        return income_data["id"] if result.inserted_id else None

    async def get_income_by_id(self, user_id: str, income_id: str) -> Optional[Income]:
        income_data = await self.income_collection.find_one({"user_id": user_id, "id": income_id})
        if income_data:
            return Income.parse_obj(income_data)
        return None

    async def get_all_incomes(self, user_id: str) -> List[Income]:
        incomes = await self.income_collection.find({"user_id": user_id}).to_list(length=100)
        return [Income.parse_obj(income) for income in incomes]

    async def update_income(self, user_id: str, update_income: UpdateIncome) -> bool:
        update_data = update_income.dict(exclude_unset=True)
        result = await self.income_collection.update_one(
            {"user_id": user_id, "id": update_income.id},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_income(self, user_id: str, income_id: str) -> bool:
        result = await self.income_collection.delete_one({"user_id": user_id, "id": income_id})
        return result.deleted_count > 0

    # ------------------- Расходы -------------------

    async def create_expense(self, user_id: str, expense: CreateExpense) -> Optional[str]:
        expense_data = expense.dict()
        expense_data["id"] = str(uuid.uuid4())
        expense_data["user_id"] = user_id
        result = await self.expense_collection.insert_one(expense_data)
        return expense_data["id"] if result.inserted_id else None

    async def get_expense_by_id(self, user_id: str, expense_id: str) -> Optional[Expense]:
        expense_data = await self.expense_collection.find_one({"user_id": user_id, "id": expense_id})
        if expense_data:
            return Expense.parse_obj(expense_data)
        return None

    async def get_all_expenses(self, user_id: str) -> List[Expense]:
        expenses = await self.expense_collection.find({"user_id": user_id}).to_list(length=100)
        return [Expense.parse_obj(expense) for expense in expenses]

    async def update_expense(self, user_id: str, update_expense: UpdateExpense) -> bool:
        update_data = update_expense.dict(exclude_unset=True)
        result = await self.expense_collection.update_one(
            {"user_id": user_id, "id": update_expense.id},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_expense(self, user_id: str, expense_id: str) -> bool:
        result = await self.expense_collection.delete_one({"user_id": user_id, "id": expense_id})
        return result.deleted_count > 0

    # ------------------- Категории -------------------

    async def create_category(self, user_id: str, new_category: CreateCategory) -> Optional[str]:
        category_data = new_category.dict()
        category_data["id"] = str(uuid.uuid4())
        result = await self.category_collection.update_one(
            {"user_id": user_id},
            {"$push": {"categories": category_data}},
            upsert=True
        )
        return category_data["id"] if result.modified_count else None

    async def get_all_categories(self, user_id: str) -> List[Category]:
        categories = await self.category_collection.find_one({"user_id": user_id})
        return [Category.parse_obj(dict(category)) for category in categories["categories"]]
