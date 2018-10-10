from arango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(protocol='http', host='arangodb', port=8529)

db = client.db('aops_database')

# Define a new graph
metadata = db.graph('operational_metadata')
fs_engines = metadata.vertex_collection('fs_engines')
er_models = metadata.vertex_collection('er_models')
model_code = metadata.vertex_collection('model_code')
datasets = metadata.vertex_collection('datasets')
edges = metadata.edge_collection('edges')
# Insert vertices into the graph
datasets.insert({'_key': 'lr-results-2','uri':'s3://pricing/results/2','md5sum':'bfed12b34869cd2ce4408ac6923ddf6'})

# Insert edges into the graph
edges.insert({'_from': 'er_models/lr-2', '_to': 'datasets/lr-scoring'})
edges.insert({'_from': 'er_models/lr-2', '_to': 'datasets/lr-results-2'})
edges.insert({'_from': 'er_models/lr-2', '_to': 'fs_engines/engine-3'})
