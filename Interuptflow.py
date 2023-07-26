import random
import argparse
from termcolor import colored

from enum import Enum

class ActivityType(Enum):
    WORK = "work"
    REVIEW = "review"
    TEST = "test"
    
class Activity:
    def __init__(self, members, type: ActivityType, progress_tick: int):
        self.members = members
        self.type = type
        self.progress_tick = progress_tick
    
class Task:
    # This class represents a single task to be performed by one or more team members.

    def __init__(self, id, priority, ramp_up_time, ramp_down_time, work_time):
        # The constructor initializes the task with an ID, priority, ramp-up time, ramp-down time, and work time.
        # The color of the task is randomly chosen from a list of colors.
        # An activity log is initialized to store the activities performed on this task.
        
        self.id = id
        self.priority = priority
        self.ramp_up_time = ramp_up_time
        self.ramp_down_time = ramp_down_time
        self.work_time = work_time
        self.progress = 0
        self.review = 0
        self.test = 0
        self.color = random.choice(['red', 'green', 'yellow', 'blue', 'magenta', 'cyan'])
        self.activity_log = []  
 
    def work(self, members, factor):
        # The 'work' method adds a 'WORK' activity for each member working on this task to the activity log.
        self.progress += 1*factor
        self.activity_log.append(Activity(members,ActivityType.WORK, self.progress))
        
    def review(self, members, timestamp):
        # The 'review' method adds a 'REVIEW' activity for each member reviewing this task to the activity log.
        self.review += 1
        self.activity_log.append(Activity(members,ActivityType.REVIEW, self.review))

    def test(self, members, timestamp):
        # The 'test' method adds a 'TEST' activity for each member testing this task to the activity log.
        self.test += 1
        self.activity_log.append(Activity(members,ActivityType.REVIEW, self.test))

    def tested(self):
        return self.test > 0

    def reviewed(self):
        return self.review > 0
    
    def is_done(self):
        # The 'is_done' method checks if the task is completed.
        # A task is considered completed if its total progress time equals its work time and it has been both tested and reviewed.
        return self.progress >= self.work_time and self.tested() and self.reviewed()
 
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