from db.elasticsearch import elasticSearch

# Set the database controller so that you can easily change it for all
# controllers in case you want to migrate to another Database
# TODO: define interface
database = elasticSearch