from typing import Optional, List
from pydantic import BaseModel
from db.elasticsearch import elasticSearch, ElasticSearchQuery

class SearchQuery(BaseModel):
  tags: Optional[List[str]] = []
  keywords: Optional[List[str]] = []
  in_title: Optional[str] = None
  in_summary: Optional[str] = None
  after_date: Optional[str] = "00000000"
  before_date: Optional[str] = "90000000"
  judges: Optional[List[str]] = []
  parties: Optional[List[str]] = []
  language: Optional[str] = None
  type: Optional[str] = None
  format: Optional[str] = None

def query_to_elastic_query(search_query: SearchQuery) -> ElasticSearchQuery:
    elastic_query = ElasticSearchQuery()
    for t in search_query.tags:
        elastic_query.add_term_search("tags", t)
    for kw in search_query.keywords:
        elastic_query.add_term_search("summary", kw)
    for j in search_query.judges:
        elastic_query.add_term_search("judges", j)
    for p in search_query.parties:
        elastic_query.add_term_search("parties", p)
    if search_query.language is not None:
        elastic_query.add_term_search("language", search_query.language)
    if search_query.type:
        elastic_query.add_term_search("type", search_query.type)
    if search_query.format:
        elastic_query.add_term_search("format", search_query.format)
    if search_query.in_title:
        elastic_query.add_term_search("title", search_query.in_title)
    if search_query.in_summary:
        elastic_query.add_term_search("summary", search_query.in_summary)
    elastic_query.add_date_range(search_query.after_date, search_query.before_date)
    return elastic_query


# Set the database controller so that you can easily change it for all
# controllers in case you want to migrate to another Database
# TODO: define interface
database = elasticSearch