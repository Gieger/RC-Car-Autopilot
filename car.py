from threading import Thread
import random
import time

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
    
    
    def start(self, rate_hz=50, max_loop_count=None):
            self.on = True

            for entry in self.parts:
                if entry.get('thread'):
                    entry.get('thread').start()

            print('Starting vehicle...')
            time.sleep(1)

            loop_count = 0

            while self.on:
                start_time = time.time()
                loop_count += 1

                self.update_parts()

                sleep_time = 1.0 / rate_hz - (time.time() - start_time)

                if sleep_time > 0.0:
                    time.sleep(sleep_time)

                if max_loop_count and loop_count > max_loop_count:
                    self.on = False

            self.stop()


    def update_parts(self):
        for entry in self.parts:
            
            run = True
            
            if entry.get('run_condition'):
                run_condition = entry.get('run_condition')
                run = self.mem.get([run_condition])[0]
                #print('run_condition', entry['part'], entry.get('run_condition'), run)
            
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
            entry['part'].shutdown()


class PrintPart():
    name = "PrintPart"

    def run(self, *args):
        print('PrintPart printing: ', end = ' ')
        print(*args)




