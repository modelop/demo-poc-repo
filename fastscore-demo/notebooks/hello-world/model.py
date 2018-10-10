# fastscore.input: hello_input
# fastscore.output: hello_output

def begin():
    global counter
    counter = 1

def action(datum):
    global counter
    counter = counter + datum
    yield 'hello world: ' + str(counter)
