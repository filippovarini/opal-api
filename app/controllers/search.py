# Controller to perform the Client's search

from typing import List


class Search:
  def get_documents(self, tags: List[str] = []):
    return f'getting documents for tags ${tags}'

  
searchController = Search()


