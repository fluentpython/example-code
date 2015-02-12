
"""
Taxi simulator

Sample run with two cars, random seed = 4::

    >>> main(num_taxis=2, seed=10)
    taxi: 0  Event(time=0, proc=0, action='leave garage')
    taxi: 0  Event(time=4, proc=0, action='pick up passenger')
    taxi: 0  Event(time=10, proc=0, action='drop off passenger')
    taxi: 1     Event(time=10, proc=1, action='leave garage')
    taxi: 1     Event(time=11, proc=1, action='pick up passenger')
    taxi: 0  Event(time=14, proc=0, action='pick up passenger')
    taxi: 1     Event(time=28, proc=1, action='drop off passenger')
    taxi: 0  Event(time=32, proc=0, action='drop off passenger')
    taxi: 0  Event(time=33, proc=0, action='going home')
    taxi: 1     Event(time=33, proc=1, action='pick up passenger')
    taxi: 1     Event(time=35, proc=1, action='drop off passenger')
    taxi: 1     Event(time=38, proc=1, action='pick up passenger')
    taxi: 1     Event(time=42, proc=1, action='drop off passenger')
    taxi: 1     Event(time=44, proc=1, action='pick up passenger')
    taxi: 1     Event(time=75, proc=1, action='drop off passenger')
    taxi: 1     Event(time=76, proc=1, action='going home')
    *** end of events ***

"""

import sys
import random
import collections
import queue
import argparse

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 80
SEARCH_INTERVAL = 4
TRIP_DURATION = 10

Event = collections.namedtuple('Event', 'time proc action')


def compute_delay(interval):
    """Compute action delay using exponential distribution"""
    return int(random.expovariate(1/interval)) + 1


def taxi_process(ident, trips, start_time=0):
    """Yield to simulator issuing event at each state change"""
    time = yield Event(start_time, ident, 'leave garage')
    for i in range(trips):
        prowling_ends = time + compute_delay(SEARCH_INTERVAL)
        time = yield Event(prowling_ends, ident, 'pick up passenger')

        trip_ends = time + compute_delay(TRIP_DURATION)
        time = yield Event(trip_ends, ident, 'drop off passenger')

    yield Event(trip_ends + 1, ident, 'going home')

# BEGIN TAXI_SIMULATOR
class Simulator:

    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()
        self.procs = dict(procs_map)


    def run(self, end_time):  # <1>
        """Schedule and display events until time is up"""
        # schedule the first event for each cab
        for _, proc in sorted(self.procs.items()):  # <2>
            first_event = next(proc)  # <3>
            self.events.put(first_event)  # <4>

        # main loop of the simulation
        time = 0
        while time < end_time:  # <5>
            if self.events.empty():  # <6>
                print('*** end of events ***')
                break

            # get and display current event
            current_event = self.events.get()  # <7>
            print('taxi:', current_event.proc,  # <8>
                  current_event.proc * '   ', current_event)

            # schedule next action for current proc
            time = current_event.time  # <9>
            proc = self.procs[current_event.proc]  # <10>
            try:
                next_event = proc.send(time)  # <11>
            except StopIteration:
                del self.procs[current_event.proc]  # <12>
            else:
                self.events.put(next_event)  # <13>
        else:  # <14>
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))
# END TAXI_SIMULATOR

def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS,
         seed=None):
    """Initialize random generator, build procs and run simulation"""
    if seed is not None:
        random.seed(seed)  # get reproducible results

    taxis = {i: taxi_process(i, (i+1)*2, i*10)
             for i in range(num_taxis)}
    sim = Simulator(taxis)
    sim.run(end_time)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                        description='Taxi fleet simulator.')
    parser.add_argument('-e', '--end-time', type=int,
                        default=DEFAULT_END_TIME,
                        help='simulation end time; default = %s'
                        % DEFAULT_END_TIME)
    parser.add_argument('-t', '--taxis', type=int,
                        default=DEFAULT_NUMBER_OF_TAXIS,
                        help='number of taxis running; default = %s'
                        % DEFAULT_NUMBER_OF_TAXIS)
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help='random generator seed (for testing)')

    args = parser.parse_args()
    main(args.end_time, args.taxis, args.seed)


"""
Sample run:

# BEGIN TAXI_SAMPLE_RUN
$ $ clear; python3 taxi_sim.py -t 3 -s 19
taxi: 0  Event(time=0, proc=0, action='leave garage')
taxi: 0  Event(time=5, proc=0, action='pick up passenger')
taxi: 1     Event(time=10, proc=1, action='leave garage')
taxi: 1     Event(time=13, proc=1, action='pick up passenger')
taxi: 2        Event(time=20, proc=2, action='leave garage')
taxi: 0  Event(time=21, proc=0, action='drop off passenger')
taxi: 1     Event(time=21, proc=1, action='drop off passenger')
taxi: 1     Event(time=23, proc=1, action='pick up passenger')
taxi: 2        Event(time=23, proc=2, action='pick up passenger')
taxi: 1     Event(time=25, proc=1, action='drop off passenger')
taxi: 1     Event(time=27, proc=1, action='pick up passenger')
taxi: 2        Event(time=27, proc=2, action='drop off passenger')
taxi: 2        Event(time=29, proc=2, action='pick up passenger')
taxi: 1     Event(time=31, proc=1, action='drop off passenger')
taxi: 2        Event(time=31, proc=2, action='drop off passenger')
taxi: 1     Event(time=33, proc=1, action='pick up passenger')
taxi: 2        Event(time=33, proc=2, action='pick up passenger')
taxi: 2        Event(time=36, proc=2, action='drop off passenger')
taxi: 2        Event(time=37, proc=2, action='pick up passenger')
taxi: 2        Event(time=40, proc=2, action='drop off passenger')
taxi: 1     Event(time=42, proc=1, action='drop off passenger')
taxi: 1     Event(time=43, proc=1, action='going home')
taxi: 0  Event(time=44, proc=0, action='pick up passenger')
taxi: 2        Event(time=44, proc=2, action='pick up passenger')
taxi: 0  Event(time=49, proc=0, action='drop off passenger')
taxi: 0  Event(time=50, proc=0, action='going home')
taxi: 2        Event(time=58, proc=2, action='drop off passenger')
taxi: 2        Event(time=65, proc=2, action='pick up passenger')
taxi: 2        Event(time=71, proc=2, action='drop off passenger')
taxi: 2        Event(time=72, proc=2, action='going home')
*** end of events ***
# END TAXI_SAMPLE_RUN

"""
