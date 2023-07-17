from enum import StrEnum

from pydantic import BaseModel


class FaberlicLanguages(StrEnum):
    RU = "ru"
    EN = "en"


class FaberlicParams(BaseModel):
    option: str = "com_catalog"
    view: str = "listgoods"
    idcategory: int = 1000175334845
    Itemid: int = 2075
    lang: FaberlicLanguages = FaberlicLanguages.RU
