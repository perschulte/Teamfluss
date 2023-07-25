import random
import argparse
from termcolor import colored
import heapq

from enum import Enum

class Activity(Enum):
    WORK = "work"
    REVIEW = "review"
    TEST = "test"

class TaskQueue:
    def __init__(self):
        self._queue = []

    def add_task(self, task):
        heapq.heappush(self._queue, (task.priority, task))
        
    def get_task(self):
        return heapq.heappop(self._queue)[1]

    def is_empty(self):
        return len(self._queue) == 0
        
class Task:
    def __init__(self, id, priority, ramp_up_time, ramp_down_time, work_time):
        self.id = id
        self.priority = priority
        self.ramp_up_time = ramp_up_time
        self.ramp_down_time = ramp_down_time
        self.work_time = work_time
        self.color = random.choice(['red', 'green', 'yellow', 'blue', 'magenta', 'cyan'])
        self.activity_log = []  # List to store activity log entries

    def work(self, members, timestamp):
        for member in members:
            self.activity_log.append({
                'member_id': member.id,
                'activity': Activity.WORK,
                'timestamp': timestamp
            }) 
        
    def review(self, members, timestamp):
         for member in members:
            self.activity_log.append({
                'member_id': member.id,
                'activity': Activity.REVIEW,
                'timestamp': timestamp
            })
    
    def test(self, members, timestamp):
        for member in members:
            self.activity_log.append({
                'member_id': member.id,
                'activity': Activity.TEST,
                'timestamp': timestamp
            })
    def tested(self):
        return any(log['activity'] == Activity.TEST for log in self.activity_log)
    
    def reviewed(self):
        return any(log['activity'] == Activity.REVIEW for log in self.activity_log)
    
    def is_done(self):
        total_progress = sum(log['activity'] == Activity.WORK for log in self.activity_log)
        return total_progress == self.work_time and self.tested() and self.reviewed()
    
class Member:
    def __init__(self, id, interruptible):
        self.id = id
        self.current_task = None
        self.interruptible = interruptible

    def work(self, task_Queue):
        
        if not self.current_task and not task_Queue.is_empty():
            self.current_task = task_Queue.get_task()
            
        if self.current_task:
            print(colored(f"Member {self.id} is working on task {self.current_task.id}", self.current_task.color))
            self.current_task.work()
            if self.current_task.progress == self.current_task.work_time:
                print(colored(f"Member {self.id} completed task {self.current_task.id}", self.current_task.color))
                self.current_task = None
        else:
            print(colored(f"Task queue is empty"))
                      
class Scenario:
    def __init__(self, num_members, num_tasks, interruptible):
        self.num_members = num_members
        self.num_tasks = num_tasks
        self.interruptible = interruptible
 
def simulate(scenario):
    # Create a set of tasks
    tasks = [Task(i, i, args.ramp_up, args.ramp_down, 15) for i in range(scenario.num_tasks)]
    
    task_Queue = TaskQueue()
    
    for task in tasks:
        task_Queue.add_task(task)

   # Create members
    members = [Member(i,scenario.interruptible) for i in range(scenario.num_members)]

    # The members work until all tasks are done
    while tasks or any(member.current_task for member in members):
        for member in members:
            member.work(task_Queue)
            
    
    total_durations = []
    for member in members:
        print(f"\nSummary for member {member.id} (interruptible: {member.interruptible}):")
        print(f"Total ramp-up time: {member.ramp_up_time} minutes")
        print(f"Total work time: {member.work_time} minutes")
        print(f"Total ramp-down time: {member.ramp_down_time} minutes")
        total_duration = member.ramp_up_time + member.work_time + member.ramp_down_time
        print(f"Total duration: {total_duration} minutes")
        total_duration = sum(member.ramp_up_time + member.work_time + member.ramp_down_time for member in members)
    return {
        'num_members': scenario.num_members,
        'num_tasks': scenario.num_tasks,
        'interruptible': scenario.interruptible,
        'total_duration': total_duration
    }
        
# Parse command line arguments for ramp-up and ramp-down times
parser = argparse.ArgumentParser()
parser.add_argument("--ramp_up", help="Ramp-up time for tasks", type=int, default=5)
parser.add_argument("--ramp_down", help="Ramp-down time for tasks", type=int, default=5)
args = parser.parse_args()

# Define scenarios
scenarios = [
    Scenario(1, 10, False),  # One member, 10 tasks, not interruptible
    Scenario(1, 10, True),   # One member, 10 tasks, interruptible
    Scenario(2, 10, False),  # Two members, 10 tasks, not interruptible
    Scenario(2, 10, True),   # Two members, 10 tasks, interruptible
]

# Simulate each scenario and store total durations
results = []
for scenario in scenarios:
    print(f"\nSimulating scenario: {scenario.num_members} member(s), {scenario.num_tasks} tasks, interruptible: {scenario.interruptible}")
    result = simulate(scenario)
    results.append(result)

# After all scenarios are done, print total durations along with scenario properties
print("\nTotal durations for all scenarios:")
for result in results:
    print(f"Scenario with {result['num_members']} member(s), {result['num_tasks']} tasks, interruptible: {result['interruptible']}: {result['total_duration']} minutes")