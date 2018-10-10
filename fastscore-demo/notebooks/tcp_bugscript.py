from fastscore import Model, Schema, Stream
from fastscore.suite import Connect

# update this to change the location of the proxy

PROXY = "https://devel:8000"

print("Creating schema, model, and stream objects")

sch_in = Schema(name="sch_double",
source = {"type" : "double"})

sch_out = Schema(name="sch_array_double",
source = { "type": "array", "items": "double"})

model = Model(name="tcp_test_model", mtype="python",
source='''# fastscore.schema.0:  sch_double
# fastscore.schema.1: sch_array_double

def action(x):
    yield [x]
''')

stream_in = Stream(name="rest_input",
desc={
    "Transport": {
        "Type": "REST"
    },
    "Encoding": "json"
})

stream_out = Stream(name = "tcp_output",
desc = {
    "Description": "Output TCP stream",
    "Encoding": "json",
    "Envelope": "delimited",
    "Transport": {
        "Type": "TCP",
        "Host": "127.0.0.1", # or change to host IP of container
        "Port": 8100
    }
})

print("Connecting to FastScore Fleet")

connect = Connect(PROXY)
engine = connect.get('engine-1')
mm = connect.lookup('model-manage')

print("Saving objects to Model Manage")

model.update(model_manage = mm)
sch_in.update(model_manage = mm)
sch_out.update(model_manage = mm)
stream_in.update(model_manage = mm)
stream_out.update(model_manage = mm)

print("Deploying to engine")
engine.reset()

model.deploy(engine)
stream_in.attach(engine, 0)
stream_out.attach(engine, 1)

print("If you've gotten this far, it must have worked.")
