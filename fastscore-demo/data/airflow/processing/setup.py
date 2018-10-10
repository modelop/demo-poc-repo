from arango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(protocol='http', host='arangodb', port=8529)

try:
    db = client.create_database('aops_database', username=None, password=None)
except:
    client.delete_database('aops_database')
    db = client.create_database('aops_database', username=None, password=None)

# Define a new graph
metadata = db.create_graph('operational_metadata')
fs_engines = metadata.create_vertex_collection('fs_engines')
er_models = metadata.create_vertex_collection('er_models')
model_code = metadata.create_vertex_collection('model_code')
datasets = metadata.create_vertex_collection('datasets')
edges = metadata.create_edge_definition(
    name='edges',
    from_collections=['fs_engines','er_models','model_code','datasets'],
    to_collections=['fs_engines','er_models','model_code','datasets']
)
# Insert vertices into the graph
fs_engines.insert({'_key': 'engine-1'})
fs_engines.insert({'_key': 'engine-2'})
fs_engines.insert({'_key': 'engine-3'})
er_models.insert({'_key': 'lr-1'})
datasets.insert({'_key': 'lr-training-1'})
datasets.insert({'_key': 'lr-scoring'})
datasets.insert({'_key': 'lr-results-1'})
model_code.insert({'_key': 'linear-regression'})

# Insert edges into the graph
edges.insert({'_from': 'model_code/linear-regression', '_to': 'er_models/lr-1'})
edges.insert({'_from': 'fs_engines/engine-1', '_to': 'er_models/lr-1'})
edges.insert({'_from': 'er_models/lr-1', '_to': 'datasets/lr-training-1'})
edges.insert({'_from': 'er_models/lr-1', '_to': 'datasets/lr-scoring'})
edges.insert({'_from': 'er_models/lr-1', '_to': 'datasets/lr-results-1'})
