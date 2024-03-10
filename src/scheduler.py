import json
from datetime import datetime

# Linked List Node
class PriorityQueueNode: 
      
    def __init__(self, value, pr): 
        self.data = value 
        self.priority = pr 
        self.next = None
          
# Implementation of Priority Queue 
class PriorityQueue: 
      
    def __init__(self): 
        self.front = None
          
    # Method to check if the Priority Queue is Empty  
    def isEmpty(self): 
        return True if self.front == None else False
      
    # Method to add items in Priority Queue  
    # According to their priority value 
    def push(self, value, priority): 
        if self.isEmpty(): 
            self.front = PriorityQueueNode(value, priority) 
            return 1 
        else: 
            if self.front.priority > priority: 
                newNode = PriorityQueueNode(value, priority) 
                newNode.next = self.front 
                self.front = newNode 
                return 1
            else: 
                temp = self.front 
                while temp.next: 
                    if priority <= temp.next.priority: 
                        break
                    temp = temp.next
                newNode = PriorityQueueNode(value, priority) 
                newNode.next = temp.next
                temp.next = newNode 
                return 1 
      
    # Method to remove a node with a specific value from the Priority Queue 
    def remove(self, time, name): 
        if self.isEmpty(): 
            return "Queue is Empty!"
        else:   
            temp = self.front
            # If the node to be removed is the first node
            if temp.data ==(time, name):
                self.front = temp.next
                temp = None
                return 1
                
            while temp.next:
                if temp.next.data == (time, name):
                    temp.next = temp.next.next
                    return 1
                temp = temp.next
            return "Value not found in the queue"
      
    # Method to remove high priority item 
    def pop(self): 
        if self.isEmpty(): 
            return "Queue is Empty!"
        else:   
            self.front = self.front.next
            return 1
              
    # Method to return high priority node  
    def peek(self): 
        if self.isEmpty(): 
            return "Queue is Empty!"
        else: 
            return self.front.data
    def clear(self):
        self.front = None 
              
    # Method to Traverse through Priority Queue 
    def traverse(self): 
        if self.isEmpty(): 
            return "Queue is Empty!"
        else: 
            temp = self.front 
            while temp: 
                print(temp.data, end=" ") 
                temp = temp.next
            print()



class AppointmentScheduler:
    def __init__(self):
        self.appointments = PriorityQueue()

    def schedule_appointment(self, appointment_time, patient_name):
        self.appointments.push(
            (appointment_time, patient_name), appointment_time)

    def cancel_appointment(self, appointment_time, patient_name):
        self.appointments.remove(appointment_time, patient_name)

    def next_appointment(self):
        return self.appointments.peek()
    

