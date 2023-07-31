import random
import argparse
from faker import Faker
from termcolor import colored
from enum import Enum

class ActivityType(Enum):
    WORK = "work"
    REVIEW = "review"
    TEST = "test"
    
class CollaborationMode(Enum):
    ALONE = "alone"
    MOB = "mob"

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
        
    def review(self, members, factor):
        # The 'review' method adds a 'REVIEW' activity for each member reviewing this task to the activity log.
        self.review += 1*factor
        self.activity_log.append(Activity(members,ActivityType.REVIEW, self.review))

    def test(self, members, factor):
        # The 'test' method adds a 'TEST' activity for each member testing this task to the activity log.
        self.test += 1*factor
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
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.current_task = None

class Team:
    def __init__(self, id, name, size:int, interruptible) -> None:
        self.id = id
        self.size = size
        fake = Faker('de_DE')
        
        #create members
        self.members = [Member(i, fake.name()) for i in range(size)]
        
    #teamworks adds one progress tick to open tasks
    def teamwork(self)-> None:
        pass
        
          
class Scenario:
    def __init__(self, num_members, num_tasks, duration, interruptible):
        self.num_members = num_members
        self.num_tasks = num_tasks
        self.duration = duration
        self.interruptible = interruptible
        
 
def simulate(scenario):
    team = Team(1, "Transformers", scenario.num_members, scenario.interruptible)
    
    for tick in range(scenario.duration):
        team.teamwork()
        
# Parse command line arguments for ramp-up and ramp-down times
parser = argparse.ArgumentParser()
parser.add_argument("--ramp_up", help="Ramp-up time for tasks", type=int, default=5)
parser.add_argument("--ramp_down", help="Ramp-down time for tasks", type=int, default=5)
args = parser.parse_args()

# Define scenarios
scenarios = [
    Scenario(1, 10, 10, False),  # One member, 10 tasks, not interruptible
    Scenario(1, 10, 10, True),   # One member, 10 tasks, interruptible
    Scenario(2, 10, 10, False),  # Two members, 10 tasks, not interruptible
    Scenario(2, 10, 10, True),   # Two members, 10 tasks, interruptible
]

simulate(scenarios[0])

