
"""
Taxi simulator

Sample run with two cars, random seed = 4::

    >>> main(num_taxis=2, seed=7)
    taxi: 0  Event(time=2, actor_id=0, action='pick up passenger')
    taxi: 1     Event(time=11, actor_id=1, action='pick up passenger')
    taxi: 1     Event(time=12, actor_id=1, action='drop off passenger')
    taxi: 0  Event(time=13, actor_id=0, action='drop off passenger')
    taxi: 0  Event(time=15, actor_id=0, action='pick up passenger')
    taxi: 0  Event(time=16, actor_id=0, action='drop off passenger')
    taxi: 1     Event(time=16, actor_id=1, action='pick up passenger')
    taxi: 0  Event(time=17, actor_id=0, action='going home')
    taxi: 1     Event(time=24, actor_id=1, action='drop off passenger')
    taxi: 1     Event(time=25, actor_id=1, action='pick up passenger')
    taxi: 1     Event(time=31, actor_id=1, action='drop off passenger')
    taxi: 1     Event(time=32, actor_id=1, action='pick up passenger')
    taxi: 1     Event(time=33, actor_id=1, action='drop off passenger')
    taxi: 1     Event(time=34, actor_id=1, action='going home')
    *** end of events ***

"""

import sys
import random
import collections
import queue
import argparse

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 80
FIND_PASSENGER_INTERVAL = 4
TRIP_DURATION = 10

Event = collections.namedtuple('Event', 'time actor_id action')


def compute_delay(interval):
    """Compute action delay using exponential distribution"""
    return int(random.expovariate(1/interval)) + 1


def taxi_process(ident, trips, start_time=0):
    """Yield to simulator issuing event at each state change"""
    time = start_time
    for i in range(trips):
        prowling_ends = time + compute_delay(FIND_PASSENGER_INTERVAL)
        time = yield Event(prowling_ends, ident, 'pick up passenger')

        trip_ends = time + compute_delay(TRIP_DURATION)
        time = yield Event(trip_ends, ident, 'drop off passenger')

    yield Event(trip_ends + 1, ident, 'going home')


class Simulator:

    def __init__(self, actors):
        self.events = queue.PriorityQueue()
        self.actors = dict(actors)


    def run(self, end_time):
        """Schedule and execute events until time is up"""
        for ident, actor in sorted(self.actors.items()):
            first_event = next(actor)  # prime each coroutine
            self.events.put(first_event)
        time = 0
        while time < end_time:
            if self.events.empty():
                print('*** end of events ***')
                break

            # get and display current event
            current_event = self.events.get()
            print('taxi:', current_event.actor_id,
                  current_event.actor_id * '   ', current_event)

            # schedule next action for current actor
            actor = self.actors[current_event.actor_id]
            time = current_event.time
            try:
                next_event = actor.send(time)
            except StopIteration:
                del self.actors[current_event.actor_id]
            else:
                self.events.put(next_event)
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))


def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS,
         seed=None):
    """Initialize random generator, build actors and run simulation"""
    if seed is not None:
        random.seed(seed)  # get reproducible results

    taxis = {i: taxi_process(i, (i+1)*2, i*10) for i in range(num_taxis)}
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

$ clear; python3 taxi_sim.py -s 19
taxi: 0  Event(time=5, actor_id=0, action='pick up passenger')
taxi: 0  Event(time=13, actor_id=0, action='drop off passenger')
taxi: 0  Event(time=16, actor_id=0, action='pick up passenger')
taxi: 1     Event(time=17, actor_id=1, action='pick up passenger')
taxi: 1     Event(time=21, actor_id=1, action='drop off passenger')
taxi: 1     Event(time=22, actor_id=1, action='pick up passenger')
taxi: 2        Event(time=23, actor_id=2, action='pick up passenger')
taxi: 1     Event(time=26, actor_id=1, action='drop off passenger')
taxi: 2        Event(time=27, actor_id=2, action='drop off passenger')
taxi: 1     Event(time=28, actor_id=1, action='pick up passenger')
taxi: 2        Event(time=29, actor_id=2, action='pick up passenger')
taxi: 1     Event(time=30, actor_id=1, action='drop off passenger')
taxi: 1     Event(time=32, actor_id=1, action='pick up passenger')
taxi: 2        Event(time=33, actor_id=2, action='drop off passenger')
taxi: 2        Event(time=34, actor_id=2, action='pick up passenger')
taxi: 2        Event(time=35, actor_id=2, action='drop off passenger')
taxi: 2        Event(time=36, actor_id=2, action='pick up passenger')
taxi: 1     Event(time=41, actor_id=1, action='drop off passenger')
taxi: 1     Event(time=42, actor_id=1, action='going home')
taxi: 2        Event(time=44, actor_id=2, action='drop off passenger')
taxi: 2        Event(time=46, actor_id=2, action='pick up passenger')
taxi: 2        Event(time=60, actor_id=2, action='drop off passenger')
taxi: 2        Event(time=67, actor_id=2, action='pick up passenger')
taxi: 2        Event(time=73, actor_id=2, action='drop off passenger')
taxi: 0  Event(time=74, actor_id=0, action='drop off passenger')
taxi: 2        Event(time=74, actor_id=2, action='going home')
taxi: 0  Event(time=75, actor_id=0, action='going home')
*** end of events ***

"""
