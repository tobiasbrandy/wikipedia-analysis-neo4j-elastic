from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union, Optional

from pydantic.main import BaseModel

@dataclass
class ImportArticleNode:
    id: int
    title: str
    links: List[str] = field(default_factory=list)

class ImportSummary(BaseModel):
    total_nodes: int
    total_relationships: int
    seconds_elapsed: int

class ArticleLink(BaseModel):
    article_id: int
    title: str

class ArticleNode(BaseModel):
    id: int
    title: str
    categories: List[str]
    links: List[ArticleLink]
    content: Optional[str] = None

class ArticleCount(BaseModel):
    count: int

# Return Types
class QueryReturnTypes(str, Enum):
    COUNT = 'COUNT'
    TITLE = 'TITLE'
    ID = 'ID'
    NODE = 'NODE'
    NODE_WITH_CONTENT = 'NODE_WITH_CONTENT'

# Elastic Filters
class TextSearchField(str, Enum):
    TITLE = 'TITLE'
    CONTENT = 'CONTENT'

class BoolOp(str, Enum):
    OR = 'OR'
    AND = 'AND'

class ElasticTextSearchFilter(BaseModel):
    field: TextSearchField
    fuzzy: bool = False
    bool_op: BoolOp = BoolOp.AND
    matches: List[str]

# Node Filters
class DistanceFilterStrategy(str, Enum):
    AT_DIST = 'AT_DIST'
    UP_TO_DIST = 'UP_TO_DIST'

class RelationDirection(str, Enum):
    INGOING = 'INGOING'
    OUTGOING = 'OUTGOING'

class NeoDistanceFilter(BaseModel):
    source_node: str
    dist: int
    strategy: DistanceFilterStrategy = DistanceFilterStrategy.UP_TO_DIST
    direction: Optional[RelationDirection] = RelationDirection.OUTGOING

class NeoLinksFilter(BaseModel):
    min_count: int = 0
    max_count: Optional[int] = None
    categories: Optional[List[str]] = None
    direction: Optional[RelationDirection] = RelationDirection.OUTGOING

# General Filters
class IdsFilter(BaseModel):
    ids: List[int]

class TitlesFilter(BaseModel):
    titles: List[str]

class CategoriesFilter(BaseModel):
    categories: List[str]

# Sort Fields
class SortByEnum(str, Enum):
    ID = 'ID'
    TITLE = 'TITLE'
    LINK_COUNT = 'LINK_COUNT'
    # elastic score ??

class SortType(str, Enum):
    ASC = 'ASC'
    DESC = 'DESC'

class QuerySort(BaseModel):
    sort_by: SortByEnum
    type: SortType = SortType.ASC


GeneralFilter = Union[IdsFilter, TitlesFilter, CategoriesFilter]
ElasticFilter = Union[ElasticTextSearchFilter]
NeoFilter = Union[NeoDistanceFilter, NeoLinksFilter]

# Primero se ejecuta elastic siempre - No hay ors
class ArticleQuery(BaseModel):
    return_type: QueryReturnTypes = QueryReturnTypes.NODE
    elastic_filter: Optional[List[ElasticFilter]] = None
    neo_filter: Optional[List[NeoFilter]] = None
    general_filters: Optional[List[GeneralFilter]] = None
    sort: Optional[QuerySort] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


SearchResult = Union[List[Union[ArticleNode, int, str]], ArticleCount]

class SearchResponse(BaseModel):
    result: SearchResult
