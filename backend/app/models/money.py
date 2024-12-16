from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class CategoryType(str, Enum):
    Income = "income"
    Expense = "expense"


class CreateCategory(BaseModel):
    name: str
    type: CategoryType  # Тип категории: доход или расход


class UpdateCategory(BaseModel):
    id: str
    name: Optional[str] = None
    type: Optional[CategoryType] = None


class Category(CreateCategory):
    id: str


class CreateIncome(BaseModel):
    source: str  # Источник дохода
    amount: float  # Сумма
    date: datetime  # Дата поступления
    category_id: Optional[str] = None  # Ссылка на категорию


class UpdateIncome(BaseModel):
    id: str
    source: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    category_id: Optional[str] = None


class Income(CreateIncome):
    id: str


class CreateExpense(BaseModel):
    description: Optional[str] = None  # Комментарий к расходу
    amount: float  # Сумма
    date: datetime  # Дата расхода
    category_id: Optional[str] = None  # Ссылка на категорию


class UpdateExpense(BaseModel):
    id: str
    description: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    category_id: Optional[str] = None


class Expense(CreateExpense):
    id: str
