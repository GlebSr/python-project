from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, Query
from backend.app.models.money import (
    Income,
    CreateIncome,
    UpdateIncome,
    Expense,
    CreateExpense,
    UpdateExpense,
    Category,
    CreateCategory
)
from backend.app.crud.money import FinanceCRUD
from backend.app.database import get_db

router = APIRouter()


@router.get("/incomes/{user_id}", response_model=List[Income])
async def get_all_incomes(user_id: str, db=Depends(get_db)) -> List[Income]:
    finance_crud = FinanceCRUD(db)
    incomes = await finance_crud.get_all_incomes(user_id)
    return incomes


@router.get("/incomes/{user_id}/{income_id}", response_model=Optional[Income])
async def get_income(user_id: str, income_id: str, db=Depends(get_db)) -> Optional[Income]:
    finance_crud = FinanceCRUD(db)
    income = await finance_crud.get_income_by_id(user_id, income_id)
    return income


@router.post("/incomes/{user_id}", response_model=str)
async def create_income(user_id: str, income: CreateIncome, db=Depends(get_db)) -> Optional[str]:
    finance_crud = FinanceCRUD(db)
    income_id = await finance_crud.create_income(user_id, income)
    return income_id


@router.put("/incomes/{user_id}")
async def update_income(user_id: str, income: UpdateIncome, db=Depends(get_db)):
    finance_crud = FinanceCRUD(db)
    success = await finance_crud.update_income(user_id, income)
    return {"success": success}


@router.delete("/incomes/{user_id}/{income_id}")
async def delete_income(user_id: str, income_id: str, db=Depends(get_db)):
    finance_crud = FinanceCRUD(db)
    success = await finance_crud.delete_income(user_id, income_id)
    return {"success": success}



@router.get("/expenses/{user_id}", response_model=List[Expense])
async def get_all_expenses(user_id: str, db=Depends(get_db)) -> List[Expense]:
    finance_crud = FinanceCRUD(db)
    expenses = await finance_crud.get_all_expenses(user_id)
    return expenses


@router.get("/expenses/{user_id}/{expense_id}", response_model=Optional[Expense])
async def get_expense(user_id: str, expense_id: str, db=Depends(get_db)) -> Optional[Expense]:
    finance_crud = FinanceCRUD(db)
    expense = await finance_crud.get_expense_by_id(user_id, expense_id)
    return expense


@router.post("/expenses/{user_id}", response_model=str)
async def create_expense(user_id: str, expense: CreateExpense, db=Depends(get_db)) -> str:
    finance_crud = FinanceCRUD(db)
    expense_id = await finance_crud.create_expense(user_id, expense)
    return expense_id


@router.put("/expenses/{user_id}")
async def update_expense(user_id: str, expense: UpdateExpense, db=Depends(get_db)):
    finance_crud = FinanceCRUD(db)
    success = await finance_crud.update_expense(user_id, expense)
    return {"success": success}


@router.delete("/expenses/{user_id}/{expense_id}")
async def delete_expense(user_id: str, expense_id: str, db=Depends(get_db)):
    finance_crud = FinanceCRUD(db)
    success = await finance_crud.delete_expense(user_id, expense_id)
    return {"success": success}



@router.get("/categories/{user_id}", response_model=List[Category])
async def get_all_categories(user_id: str, db=Depends(get_db)) -> List[Category]:
    finance_crud = FinanceCRUD(db)
    categories = await finance_crud.get_all_categories(user_id)
    return categories


@router.post("/categories/{user_id}", response_model=str)
async def create_category(user_id: str, new_category: CreateCategory, db=Depends(get_db)) -> str:
    finance_crud = FinanceCRUD(db)
    category_id = await finance_crud.create_category(user_id, new_category)
    return category_id


@router.get("/analytics/{user_id}", response_model=Dict[str, Any])
async def get_analytics(
        user_id: str,
        start_date: datetime = Query(None),
        end_date: datetime = Query(None),
        category_id: Optional[str] = Query(None),
        db=Depends(get_db)
) -> Dict[str, Any]:
    """
    Возвращает агрегированную статистику:
    - total_income: общий доход
    - total_expense: общий расход
    - balance: разница доход-расход
    - incomes_over_time: список {date, total_income за день/месяц}
    - expenses_over_time: список {date, total_expense за день/месяц}
    - expense_by_category: {category_name: total_amount} за период
    """

    finance_crud = FinanceCRUD(db)

    incomes = await finance_crud.get_all_incomes(user_id)
    expenses = await finance_crud.get_all_expenses(user_id)

    # Фильтруем по датам и категориям
    def in_date_range(dt: datetime) -> bool:
        if start_date and dt < start_date:
            return False
        if end_date and dt > end_date:
            return False
        return True

    filtered_incomes = [
        inc for inc in incomes
        if in_date_range(inc.date) and (not category_id or inc.category_id == category_id)
    ]
    filtered_expenses = [
        exp for exp in expenses
        if in_date_range(exp.date) and (not category_id or exp.category_id == category_id)
    ]


    total_income = sum(i.amount for i in filtered_incomes)
    total_expense = sum(e.amount for e in filtered_expenses)
    balance = total_income - total_expense


    from collections import defaultdict
    income_time_map = defaultdict(float)
    expense_time_map = defaultdict(float)

    for i in filtered_incomes:
        date_str = i.date.strftime("%Y-%m-%d")
        income_time_map[date_str] += i.amount

    for e in filtered_expenses:
        date_str = e.date.strftime("%Y-%m-%d")
        expense_time_map[date_str] += e.amount

    incomes_over_time = [{"date": d, "total_income": amt} for d, amt in income_time_map.items()]
    expenses_over_time = [{"date": d, "total_expense": amt} for d, amt in expense_time_map.items()]


    categories = await finance_crud.get_all_categories(user_id)
    category_map = {cat.id: cat.name for cat in categories}
    expense_by_category = defaultdict(float)
    for e in filtered_expenses:
        cat_name = category_map.get(e.category_id, "Uncategorized")
        expense_by_category[cat_name] += e.amount

    expense_by_category_res = [{"category": c, "total": amt} for c, amt in expense_by_category.items()]

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "incomes_over_time": incomes_over_time,
        "expenses_over_time": expenses_over_time,
        "expense_by_category": expense_by_category_res
    }
    return None