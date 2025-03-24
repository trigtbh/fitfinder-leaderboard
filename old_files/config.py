cache = {}

def pre_request(worker, req):
    
    print("A")
    worker.close()