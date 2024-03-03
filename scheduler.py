from datetime import datetime

class AppointmentScheduler:
    def __init__(self):
        self.appointments = []

    def schedule_appointment(self, appointment_time, patient_name):
        self.appointments.append((appointment_time, patient_name))
        self.appointments.sort(key=lambda x: x[0])

    def cancel_appointment(self, appointment_time, patient_name):
        self.appointments = [(time, name) for time, name in self.appointments if time != appointment_time or name != patient_name]

    def next_appointment(self):
        if self.appointments:
            return self.appointments[0]
        else:
            return None
        



class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, item, priority):
        self.queue.append((priority, item))
        self.queue.sort(key=lambda x: x[0])

    def pop(self):
        if self.queue:
            return self.queue.pop(0)[1]
        else:
            return None

    def peek(self):
        if self.queue:
            return self.queue[0][1]
        else:
            return None

    def remove(self, item):
        self.queue = [(priority, value) for priority, value in self.queue if value != item]
