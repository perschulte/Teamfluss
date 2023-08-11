import random
import argparse
from faker import Faker
from termcolor import colored
from enum import Enum

class ActivityType(Enum):
    WORK = "work"
    REVIEW = "review"
    TEST = "test"
    RAMP_UP = "ramp_up"
    RAMP_DOWN = "ramp_down"
    
class CollaborationMode(Enum):
    ALONE = "alone"
    MOB = "mob"
    
class State(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Activity:
    def __init__(self, members, type: ActivityType, progress_step):
        self.members = members
        self.type = type
        self.progress_step = progress_step
    

class Task:
    # This class represents a single task to be performed by one or more team members.

    def __init__(self, id, priority, time_to_complete_ramp_up_time, time_to_complete_ramp_down_time, review_ramp_up_time, review_ramp_down_time, test_ramp_up_time, test_ramp_down_time, time_to_complete):
        # The constructor initializes the task with an ID, priority, ramp-up time, ramp-down time, and work time.
        # The color of the task is randomly chosen from a list of colors.
        # An activity log is initialized to store the activities performed on this task.
        
        self.id = id
        self.priority = priority
        self.state = State.OPEN
        
        self.time_to_complete_progress = 0
        self.time_to_complete = time_to_complete
        self.time_to_complete_ramp_up_remaining = time_to_complete_ramp_up_time
        self.time_to_complete_ramp_up_time = time_to_complete_ramp_up_time
        self.time_to_complete_ramp_down_remaining = time_to_complete_ramp_down_time
        self.time_to_complete_ramp_down_time = time_to_complete_ramp_down_time
        
        self.review_progress = 0
        self.review_ramp_up_remaining = review_ramp_up_time
        self.review_ramp_up_time = review_ramp_up_time
        self.review_ramp_down_remaining = review_ramp_down_time
        self.review_ramp_down_time = review_ramp_down_time
        
        self.test_progress = 0
        self.test_ramp_up_remaining = test_ramp_up_time
        self.test_ramp_up_time = test_ramp_up_time
        self.test_ramp_down_remaining = test_ramp_down_time
        self.test_ramp_down_time = test_ramp_down_time

        self.color = random.choice(['red', 'green', 'yellow', 'blue', 'magenta', 'cyan'])
        self.activity_log = []
          
    def start_working(self):
        if self.state == State.OPEN:
            self.time_to_complete_ramp_up_remaining = self.time_to_complete_ramp_up_time
            self.state = State.IN_PROGRESS  
            
    def work(self, members, factor):
        # The 'work' method adds a 'WORK' activity for each member working on this task to the activity log.
        if self.time_to_complete_ramp_up_remaining > 0:
            self.time_to_complete_ramp_up_remaining -= 1*factor
            self.activity_log.append(Activity(members,ActivityType.RAMP_UP, -1*factor))
        elif self.time_to_complete_ramp_down_remaining > 0:
            self.time_to_complete_ramp_down_remaining -= 1*factor
            self.activity_log.append(Activity(members,ActivityType.RAMP_DOWN, -1*factor))
            if self.time_to_complete_ramp_down_remaining <=0:
                for member in members:
                    member.current_task = None
        else:
            self.time_to_complete_progress += 1*factor
            self.activity_log.append(Activity(members,ActivityType.WORK, 1*factor))

    def stop_working(self):
        if self.state == State.IN_PROGRESS:
            self.time_to_complete_ramp_down_remaining = self.time_to_complete_ramp_down_time
            self.state = State.OPEN    
    def start_reviewing(self):
        if self.state == State.OPEN:
            self.review_ramp_up_remaining = self.review_ramp_up_time
            self.state = State.IN_PROGRESS
        
    def review(self, members, factor):
        # The 'review' method adds a 'REVIEW' activity for each member reviewing this task to the activity log.
        if self.review_ramp_up_remaining > 0:
            self.review_ramp_up_remaining -= 1*factor
            self.activity_log.append(Activity(members,ActivityType.RAMP_UP, -1*factor))
        elif self.review_ramp_down_remaining > 0:
            self.review_ramp_down_remaining -= 1*factor
            self.activity_log.append(Activity(members,ActivityType.RAMP_DOWN, -1*factor))
            if self.review_ramp_down_remaining <=0:
                for member in members:
                    member.current_task = None
        else:
            self.review_progress += 1*factor
            self.activity_log.append(Activity(members,ActivityType.REVIEW, 1*factor))

    def stop_reviewing(self):
        if self.state == State.IN_PROGRESS:
            self.review_ramp_down_remaining = self.review_ramp_down_time
            self.state = State.OPEN
            
    def start_testing(self):
        if self.state == State.OPEN:
            self.test_ramp_up_remaining = self.test_ramp_up_time
            self.state = State.IN_PROGRESS
            
    def test(self, members, factor):
        # The 'test' method adds a 'TEST' activity for each member testing this task to the activity log.
        if self.test_ramp_up_remaining > 0:
            self.test_ramp_up_remaining -= 1*factor
            self.activity_log.append(Activity(members,ActivityType.RAMP_UP, -1*factor))
        elif self.test_ramp_down_remaining > 0:
            self.test_ramp_down_remaining -= 1*factor
            self.activity_log.append(Activity(members,ActivityType.RAMP_DOWN, -1*factor))
            if self.test_ramp_down_remaining <=0:
                for member in members:
                    member.current_task = None
        else:
            self.test_progress += 1*factor
            self.activity_log.append(Activity(members,ActivityType.TEST, self.test))
    
    def stop_testing(self):
        if self.state == State.IN_PROGRESS:
            self.test_ramp_down_remaining = self.test_ramp_down_time
            self.state = State.OPEN
        
    def work_completed(self):
        return self.time_to_complete_progress >= self.time_to_complete
    
    def tested(self):
        return self.test_progress > 0.1 * self.time_to_complete

    def reviewed(self):
        review_Factor = 0.05
        return self.review_progress > review_Factor * self.time_to_complete
    
    def is_done(self):
        # The 'is_done' method checks if the task is completed.
        # A task is considered completed if its total progress time equals its work time and it has been both tested and reviewed.
        return self.time_to_complete_progress >= self.time_to_complete and self.tested() and self.reviewed()
    
    def assign_members(self, members):
        for member in members:
            member.current_task = self
        
            
    def get_ramp_times(self):
        ramp_up_time = 0
        for activity in self.activity_log:
            if activity.type == ActivityType.RAMP_UP:
                ramp_up_time -= activity.progress_step
        
        ramp_down_time = 0
        for activity in self.activity_log:
            if activity.type == ActivityType.RAMP_DOWN:
                ramp_down_time -= activity.progress_step
        
        return ramp_up_time, ramp_down_time
 
class Member:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.current_task = None
        
    def is_idle(self) -> bool:
        return self.current_task is None

class Team:
    def __init__(self, id, name, size:int, tasks, interruptible, collaborationMode:CollaborationMode) -> None:
        self.id = id
        self.size = size
        self.tasks = tasks
        self.collaborationMode = collaborationMode
        self.interruptible = interruptible
        fake = Faker('de_DE')
        
        #create members
        self.members = [Member(i, fake.first_name()) for i in range(size)]
    
    #find all idle team members and organize new work for them
    def pull_new_work(self) -> None:
        idle_members = filter(lambda member: member.is_idle(), self.members)
        if CollaborationMode.ALONE:
            for member in idle_members:
                # Find the most important task with no other team member assigned
                available_tasks = list(filter(lambda task: not task.is_done() and not any(not m.is_idle() and m.current_task == task for m in self.members), self.tasks))
                if available_tasks:
                    most_important_task = min(available_tasks, key=lambda task: task.priority)
                    member.current_task = most_important_task
                    #print(f'Member {member.name} is assigned to task {most_important_task.id}')
                else:
                    member.current_task = None
        else:
            pass
        
    #teamworks adds one progress tick to assigned tasks
    def teamwork(self)-> None:
        for task in self.tasks:
            # Find members that work on this task
            working_members = [member for member in self.members if member.current_task == task]
            member_names = [member.name for member in working_members]
            #the assigned members decide what to do next (work, test, review)
            #Work: Check for is work_completed
            #Test: Needs to be done after all work is completed
            #Review: Needs to be done after all work is completed and tested
            if working_members:    
                if not task.work_completed():
                    
                    task.start_working()
                    task.work(working_members, 1.0)
                    #print(f'Members {member_names} worked on task {task.id}')
                    
                    if task.work_completed():
                        #print(f'Members {member_names} completed the work on task {task.id}')
                        task.stop_working()

                elif not task.tested() and task.work_completed():
                    # If work is completed but not tested, start testing
                    task.start_testing()
                    task.test(working_members, 1.0)
                    #print(f'Members {member_names} tested task {task.id}')
                    # Unassign the task on all members
                    if task.tested():
                        task.stop_testing()
                    
                elif not task.reviewed() and task.tested():

                    task.review(working_members, 1.0)
                    #print(f'Members {member_names} reviewed task {task.id}')
                    
                    if task.reviewed():
                        task.stop_reviewing()
                    
class Scenario:
    def __init__(self,id, num_members, num_tasks, duration, interruptible, description):
        self.id = id
        self.num_members = num_members
        self.num_tasks = num_tasks
        self.duration = duration
        self.interruptible = interruptible
        self.description = description
    
# Assuming you have a list of tasks
def count_completed_tasks(tasks):
    return sum(task.is_done() for task in tasks)

def count_incomplete_tasks(tasks):
    return sum(not task.is_done() for task in tasks)

def calculate_total_ramp_times(tasks):
        total_ramp_up_time = 0
        total_ramp_down_time = 0
        for task in tasks:
            ramp_up_time, ramp_down_time = task.get_ramp_times()
            total_ramp_up_time += ramp_up_time
            total_ramp_down_time += ramp_down_time
        return total_ramp_up_time, total_ramp_down_time
 
         
def simulate(scenario):
    print(f"=== Starting Simulation for Scenario {scenario.id} ===")
    tasks = [Task(i,i,7,4,4,1,7,4,480) for i in range(scenario.num_tasks)]
    
    team = Team(1, "Transformers", scenario.num_members, tasks, scenario.interruptible, CollaborationMode.ALONE)
    
    for tick in range(scenario.duration):
        team.pull_new_work()
        team.teamwork()
    
    # At the end of your simulate function
    completed_tasks = count_completed_tasks(tasks)
    incomplete_tasks = count_incomplete_tasks(tasks)

    print(f"\nCompleted tasks: {completed_tasks}")
    print(f"Incomplete tasks: {incomplete_tasks}")
    
    total_ramp_up_time, total_ramp_down_time = calculate_total_ramp_times(tasks)
    print(f"For scenario {scenario.id}, total ramp-up time was {total_ramp_up_time} and total ramp-down time was {total_ramp_down_time}")
    print(f"=== End of Simulation for Scenario {scenario.id} ===\n")
    
        
# Parse command line arguments for ramp-up and ramp-down times
parser = argparse.ArgumentParser()
parser.add_argument("--ramp_up", help="Ramp-up time for tasks", type=int, default=5)
parser.add_argument("--ramp_down", help="Ramp-down time for tasks", type=int, default=5)
args = parser.parse_args()

# Define scenarios
scenarios = [
    Scenario(1, 1, 10, 4800, False, "One member, 10 tasks, not interruptible"),  # One member, 10 tasks, not interruptible
    Scenario(2, 1, 10, 4800, True, "One member, 10 tasks, interruptible"),   # One member, 10 tasks, interruptible
    Scenario(3, 2, 10, 4800, False, "Two members, 10 tasks, not interruptible"),  # Two members, 10 tasks, not interruptible
    Scenario(4, 1, 10, 4800, True, "Two members, 10 tasks, interruptible"),   # Two members, 10 tasks, interruptible
]


for scenario in scenarios:
    simulate(scenario)

