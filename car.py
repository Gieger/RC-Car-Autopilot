from threading import Thread

class Memory():
    def __init__(self):
        self.dict = {}
        pass
    
    def put(self, keys, inputs):
        for i, key in enumerate(keys):
            #self.dict[key] = inputs[i]
            self.dict[keys[0]] = inputs
            
    def get(self, keys):
        result = [self.dict.get(k) for k in keys]

        return result
        

import random
import time

class Vehicle():
    def __init__(self, mem=None):
        
        if not mem:
            mem = Memory()
        self.mem = mem
        
        self.parts = [] 
        self.on = True
        threads = []
        
    def add(self, part, inputs=[], outputs=[], threaded=False):    
        p = part
        print('Adding part {}.'.format(p.name))
        entry={}
        entry['part'] = p
        entry['inputs'] = inputs
        entry['outputs'] = outputs
        
        if threaded:
            t = Thread(target=part.update, args=())
            t.daemon = True
            entry['thread'] = t
            
        self.parts.append(entry)
    
    
    def start(self, delay=.1):
        for entry in self.parts:
            if entry.get('thread'):
                entry.get('thread').start()
        
        print('Starting vehicle...')
        time.sleep(1)
        count = 0
        while self.on:

            count = count + 1
            for entry in self.parts:
                p = entry['part']

                inputs = self.mem.get(entry['inputs'])
                
                if entry.get('thread'):
                    outputs = p.run_threaded(*inputs)
                else:
                    outputs = p.run(*inputs)
                
                self.mem.put(entry['outputs'], outputs)
                
                time.sleep(delay)
                
            if count > 1:
                self.on = False


    def update_parts(self):
        print('Started vehicle...')
        while True:
            for entry in self.parts:
                
                run = True
                
                if entry.get('run_condition'):
                    run_condition = entry.get('run_condition')
                    run = self.mem.get([run_condition])[0]
                
                if run:
                    p = entry['part']

                    inputs = self.mem.get(entry['inputs'])

                    if entry.get('thread'):
                        outputs = p.run_threaded(*inputs)

                    else:
                        outputs = p.run(*inputs)

                    if outputs is not None:
                        self.mem.put(entry['outputs'], outputs)



    def stop(self):
        for entry in self.parts:
            try:
                entry['part'].shutdown()
            except Exception as e:
                print(e)


class PrintPart():    
    name = "PrintPart"
    
    def run(self, *args):
        print('PrintPart printing: ', end = ' ')
        print(*args)




