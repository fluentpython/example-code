import sys
import random
import collections
import queue

FIND_CUSTOMER_INTERVAL = 4
TRIP_DURATION = 10

Event = collections.namedtuple('Event', 'time actor description')

def compute_delay(interval):
    return int(random.expovariate(1/interval)) + 1


def taxi_process(sim, ident):
    trips = 3
    for i in range(trips):
        prowling_time = compute_delay(FIND_CUSTOMER_INTERVAL)
        yield Event(sim.time + prowling_time, ident, 'customer picked up')

        trip_time = compute_delay(TRIP_DURATION)
        yield Event(sim.time + trip_time, ident, 'customer dropped off')


class Simulator:

    def __init__(self):
        self.events = queue.PriorityQueue()
        self.time = 0

    def run(self, end_time):
        #import pdb; pdb.set_trace()
        taxis = [taxi_process(self, i) for i in range(3)]
        while self.time < end_time:
            for index, taxi in enumerate(taxis):
                try:
                    future_event = next(taxi)
                except StopIteration:
                    del taxis[index]  # remove taxi not in service
                else:
                    self.events.put(future_event)
            if self.events.empty():
                print('*** end of events ***')
                break
            event = self.events.get()
            self.time = event.time
            print('taxi:', event.actor, event)
        else:
            print('*** end of simulation time ***')


def main(args):
    if 'debug' in args:  # for testing...
        random.seed(0)  # get reproducible results
        args.remove('debug')
    if args:
        end_time = int(args[0])
    else:
        end_time = 10
    sim = Simulator()
    sim.run(end_time)

if __name__ == '__main__':
    main(sys.argv[1:])
