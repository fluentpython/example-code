
"""
Taxi simulator

Sample run with two cars, random seed 10. This is a valid doctest.

    >>> main(num_taxis=2, seed=10)
    taxi: 0  Event(time=0, proc=0, action='leave garage')
    taxi: 0  Event(time=4, proc=0, action='pick up passenger')
    taxi: 1     Event(time=5, proc=1, action='leave garage')
    taxi: 1     Event(time=9, proc=1, action='pick up passenger')
    taxi: 0  Event(time=10, proc=0, action='drop off passenger')
    taxi: 1     Event(time=12, proc=1, action='drop off passenger')
    taxi: 0  Event(time=17, proc=0, action='pick up passenger')
    taxi: 1     Event(time=19, proc=1, action='pick up passenger')
    taxi: 1     Event(time=21, proc=1, action='drop off passenger')
    taxi: 1     Event(time=24, proc=1, action='pick up passenger')
    taxi: 0  Event(time=28, proc=0, action='drop off passenger')
    taxi: 1     Event(time=28, proc=1, action='drop off passenger')
    taxi: 0  Event(time=29, proc=0, action='going home')
    taxi: 1     Event(time=30, proc=1, action='pick up passenger')
    taxi: 1     Event(time=61, proc=1, action='drop off passenger')
    taxi: 1     Event(time=62, proc=1, action='going home')
    *** end of events ***

See explanation and longer sample run at the end of this module.

"""

import sys
import random
import collections
import queue
import argparse

DEFAULT_NUMBER_OF_TAXIS = 3
DEFAULT_END_TIME = 80
SEARCH_DURATION = 4
TRIP_DURATION = 10
DEPARTURE_INTERVAL = 5

Event = collections.namedtuple('Event', 'time proc action')


def compute_delay(interval):
    """Compute action delay using exponential distribution"""
    return int(random.expovariate(1/interval)) + 1

# BEGIN TAXI_PROCESS
def taxi_process(ident, trips, start_time=0):  # <1>
    """Yield to simulator issuing event at each state change"""
    time = yield Event(start_time, ident, 'leave garage')  # <2>
    for i in range(trips):  # <3>
        prowling_ends = time + compute_delay(SEARCH_DURATION)  # <4>
        time = yield Event(prowling_ends, ident, 'pick up passenger')  # <5>

        trip_ends = time + compute_delay(TRIP_DURATION)  # <6>
        time = yield Event(trip_ends, ident, 'drop off passenger')  # <7>

    yield Event(time + 1, ident, 'going home')  # <8>
    # end of taxi process # <9>
# END TAXI_PROCESS

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

    taxis = {i: taxi_process(i, (i+1)*2, i*DEPARTURE_INTERVAL)
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
Notes for the ``taxi_process`` coroutine::

<1> `taxi_process` will be called once per taxi, creating a generator
    object to represent its operations. `ident` is the number of the taxi
    (eg. 0, 1, 2 in the sample run); `trips` is the number of trips this
    taxi will make before going home; `start_time` is when the taxi
    leaves the garage.

<2> The first `Event` yielded is `'leave garage'`. This suspends the
    coroutine, and lets the simulation main loop proceed to the next
    scheduled event. When it's time to reactivate this process, the main
    loop will `send` the current simulation time, which is assigned to
    `time`.

<3> This block will be repeated once for each trip.

<4> The ending time of the search for a passenger is computed.

<5> An `Event` signaling passenger pick up is yielded. The coroutine
    pauses here. When the time comes to reactivate this coroutine,
    the main loop will again `send` the current time.

<6> The ending time of the trip is computed, taking into account the
    current `time`.

<7> An `Event` signaling passenger drop off is yielded. Coroutine
    suspended again, waiting for the main loop to send the time of when
    it's time to continue.

<8> The `for` loop ends after the given number of trips, and a final
    `'going home'` event is yielded, to happen 1 minute after the current
    time. The coroutine will suspend for the last time. When reactivated,
    it will be sent the time from the simulation main loop, but here I
    don't assign it to any variable because it will not be useful.

<9> When the coroutine falls off the end, the coroutine object raises
    `StopIteration`.


Notes for the ``Simulator.run`` method::

<1> The simulation `end_time` is the only required argument for `run`.

<2> Use `sorted` to retrieve the `self.procs` items ordered by the
    integer key; we don't care about the key, so assign it to `_`.

<3> `next(proc)` primes each coroutine by advancing it to the first
    yield, so it's ready to be sent data. An `Event` is yielded.

<4> Add each event to the `self.events` `PriorityQueue`. The first
    event for each taxi is `'leave garage'`, as seen in the sample run
    (ex_taxi_process>>).

<5> Main loop of the simulation: run until the current `time` equals
    or exceeds the `end_time`.

<6> The main loop may also exit if there are no pending events in the
    queue.

<7> Get `Event` with the smallest `time` in the queue; this is the
    `current_event`.

<8> Display the `Event`, identifying the taxi and adding indentation
    according to the taxi id.

<9> Update the simulation time with the time of the `current_event`.

<10> Retrieve the coroutine for this taxi from the `self.procs`
     dictionary.

<11> Send the `time` to the coroutine. The coroutine will yield the
     `next_event` or raise `StopIteration` it's finished.

<12> If `StopIteration` was raised, delete the coroutine from the
     `self.procs` dictionary.

<13> Otherwise, put the `next_event` in the queue.

<14> If the loop exits because the simulation time passed, display the
     number of events pending (which may be zero by coincidence,
     sometimes).


Sample run from the command line, seed=24, total elapsed time=160::

# BEGIN TAXI_SAMPLE_RUN
$ python3 taxi_sim.py -s 24 -e 160
taxi: 0  Event(time=0, proc=0, action='leave garage')
taxi: 0  Event(time=5, proc=0, action='pick up passenger')
taxi: 1     Event(time=5, proc=1, action='leave garage')
taxi: 1     Event(time=6, proc=1, action='pick up passenger')
taxi: 2        Event(time=10, proc=2, action='leave garage')
taxi: 2        Event(time=11, proc=2, action='pick up passenger')
taxi: 2        Event(time=23, proc=2, action='drop off passenger')
taxi: 0  Event(time=24, proc=0, action='drop off passenger')
taxi: 2        Event(time=24, proc=2, action='pick up passenger')
taxi: 2        Event(time=26, proc=2, action='drop off passenger')
taxi: 0  Event(time=30, proc=0, action='pick up passenger')
taxi: 2        Event(time=31, proc=2, action='pick up passenger')
taxi: 0  Event(time=43, proc=0, action='drop off passenger')
taxi: 0  Event(time=44, proc=0, action='going home')
taxi: 2        Event(time=46, proc=2, action='drop off passenger')
taxi: 2        Event(time=49, proc=2, action='pick up passenger')
taxi: 1     Event(time=70, proc=1, action='drop off passenger')
taxi: 2        Event(time=70, proc=2, action='drop off passenger')
taxi: 2        Event(time=71, proc=2, action='pick up passenger')
taxi: 2        Event(time=79, proc=2, action='drop off passenger')
taxi: 1     Event(time=88, proc=1, action='pick up passenger')
taxi: 2        Event(time=92, proc=2, action='pick up passenger')
taxi: 2        Event(time=98, proc=2, action='drop off passenger')
taxi: 2        Event(time=99, proc=2, action='going home')
taxi: 1     Event(time=102, proc=1, action='drop off passenger')
taxi: 1     Event(time=104, proc=1, action='pick up passenger')
taxi: 1     Event(time=135, proc=1, action='drop off passenger')
taxi: 1     Event(time=136, proc=1, action='pick up passenger')
taxi: 1     Event(time=151, proc=1, action='drop off passenger')
taxi: 1     Event(time=152, proc=1, action='going home')
*** end of events ***
# END TAXI_SAMPLE_RUN

"""
