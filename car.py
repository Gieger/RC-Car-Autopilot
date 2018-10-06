from threading import Thread
import random
import time


class Memory():
    def __init__(self):
        self.d = {}
        pass
    
    def put(self, keys, inputs):
        if len(keys) > 1:
            for i, key in enumerate(keys):
                try:
                    self.d[key] = inputs[i]
                except IndexError as e:
                    error = str(e) + ' issue with keys: ' + str(key)
                    raise IndexError(error)
        else:
            self.d[keys[0]] = inputs

    def get(self, keys):
        result = [self.d.get(k) for k in keys]
        return result


        

class Herbie():
    def __init__(self, mem=None):
        mem = Memory()
        self.mem = mem
        self.on = True
        self.parts = []
        threads = []
        
    def add(self, part, inputs=[], outputs=[], threaded=False):    
        p = part
        print('Komponente hinzufügen {}.'.format(p.name))
        entry={}
        entry['part'] = p
        entry['inputs'] = inputs
        entry['outputs'] = outputs
        
        if threaded:
            t = Thread(target=part.update, args=())
            t.daemon = True
            entry['thread'] = t
        
        self.parts.append(entry)
    
    def start(self, rate_hz=10, max_loop_count=None):
        self.on = True

        for entry in self.parts:
            if entry.get('thread'):
                entry.get('thread').start()

        print('Fahrzeug wird gestartet...')
        time.sleep(1)

        loop_count = 0

        while self.on:
            loop_count += 1

            self.update_parts()
            #time.sleep(rate_hz)

            if max_loop_count and loop_count > max_loop_count:
                self.on = False
                self.stop()
     
    def update_parts(self):
        for entry in self.parts:
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
            entry['part'].shutdown()




