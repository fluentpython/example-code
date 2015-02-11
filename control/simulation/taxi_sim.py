import sys
import random
import collections
import queue

FIND_PASSENGER_INTERVAL = 4
TRIP_DURATION = 10

Event = collections.namedtuple('Event', 'time actor description')


def compute_delay(interval):
    return int(random.expovariate(1/interval)) + 1


def taxi_process(ident, trips):
    trip_ends = 0
    for i in range(trips):
        prowling_ends = trip_ends + compute_delay(FIND_PASSENGER_INTERVAL)
        yield Event(prowling_ends, ident, 'passenger picked up')

        trip_ends = prowling_ends + compute_delay(TRIP_DURATION)
        yield Event(trip_ends, ident, 'passenger dropped off')

    yield Event(trip_ends + 1, ident, 'going home')


class Simulator:

    def __init__(self, actors):
        self.events = queue.PriorityQueue()
        self.actors = list(actors)
        self.time = 0

    def schedule_events(self, end_time):
        for index, actor in enumerate(list(self.actors)):
            try:
                future_event = next(actor)
            except StopIteration:
                self.actors.remove(actor)  # remove exhausted actor
            else:
                self.events.put(future_event)

    def run(self, end_time):
        while self.time < end_time:
            self.schedule_events(end_time)
            if self.events.empty():
                print('*** end of events ***')
                break
            event = self.events.get()
            self.time = event.time
            print('taxi:', event.actor, event.actor * '   ', event)
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))


def extract_seed(args):
    """Set random seed if given in command line"""
    for index, arg in enumerate(list(args)):
        if arg.startswith('seed='):  # for testing...
            seed = int(arg.split('=')[1])
            random.seed(seed)  # get reproducible results
            del args[index]
            return


def main(args):
    extract_seed(args)
    if args:
        end_time = int(args[0])
    else:
        end_time = 100
    taxis = [taxi_process(i, (i+1)*2) for i in range(3)]
    sim = Simulator(taxis)
    sim.run(end_time)

if __name__ == '__main__':
    main(sys.argv[1:])


"""
Sample run:

$ clear; python3 taxi_sim.py seed=5 110
taxi: 0  Event(time=4, actor=0, description='passenger picked up')
taxi: 1     Event(time=6, actor=1, description='passenger picked up')
taxi: 2        Event(time=7, actor=2, description='passenger picked up')
taxi: 1     Event(time=20, actor=1, description='passenger dropped off')
taxi: 1     Event(time=23, actor=1, description='passenger picked up')
taxi: 0  Event(time=33, actor=0, description='passenger dropped off')
taxi: 2        Event(time=33, actor=2, description='passenger dropped off')
taxi: 0  Event(time=34, actor=0, description='passenger picked up')
taxi: 0  Event(time=45, actor=0, description='passenger dropped off')
taxi: 2        Event(time=45, actor=2, description='passenger picked up')
taxi: 0  Event(time=46, actor=0, description='going home')
taxi: 1     Event(time=47, actor=1, description='passenger dropped off')
taxi: 2        Event(time=47, actor=2, description='passenger dropped off')
taxi: 2        Event(time=49, actor=2, description='passenger picked up')
taxi: 1     Event(time=50, actor=1, description='passenger picked up')
taxi: 1     Event(time=58, actor=1, description='passenger dropped off')
taxi: 2        Event(time=58, actor=2, description='passenger dropped off')
taxi: 1     Event(time=59, actor=1, description='passenger picked up')
taxi: 2        Event(time=59, actor=2, description='passenger picked up')
taxi: 1     Event(time=63, actor=1, description='passenger dropped off')
taxi: 1     Event(time=64, actor=1, description='going home')
taxi: 2        Event(time=84, actor=2, description='passenger dropped off')
taxi: 2        Event(time=90, actor=2, description='passenger picked up')
taxi: 2        Event(time=92, actor=2, description='passenger dropped off')
taxi: 2        Event(time=99, actor=2, description='passenger picked up')
taxi: 2        Event(time=101, actor=2, description='passenger dropped off')
taxi: 2        Event(time=102, actor=2, description='going home')
*** end of events ***

"""
