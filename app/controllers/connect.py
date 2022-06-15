# Controller to connect to external databases and perform indexing.
# Save indexing by storing the document id ; search query ; metadata genereted
# on our database

class Connect:
  # Store the details to connect with the external database.
  def __init__(self, connection_details) -> None:
    self.connection_details = connection_details
    
  def get_document(self, id: str, query: str):
    return f'getting document with id ${id} for database with query ${query}'

  def update_document(self, id: str):
    return f'updating document ${id}'

  # Save document to our Database by storing the document id and metadata.
  def save_document(self, id: str):
    return f'saving document ${id}'