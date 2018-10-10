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
er_models.insert({'_key': 'lr-2'})
datasets.insert({'_key': 'lr-training-2','uri':'hdfs://trainingsets/2','md5sum':'aaaaafd6f3e6c5e5d062dc8bfa793bf2'})

# Insert edges into the graph
edges.insert({'_from': 'er_models/lr-2', '_to': 'datasets/lr-training-2'})
edges.insert({'_from': 'model_code/linear-regression', '_to': 'er_models/lr-2'})
