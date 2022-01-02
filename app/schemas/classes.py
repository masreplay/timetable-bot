from enum import Enum

from sqlmodel import SQLModel


class ShiftType(Enum, str):
    evening = "evening"
    morning = "morning"


class BranchBase(SQLModel):
    """
    like software
    """
    name: str


class Branch(BranchBase, table=True):
    pass


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BranchBase):
    pass
