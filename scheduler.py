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
        self.queue = [(priority, value)
                      for priority, value in self.queue if value != item]


class AppointmentScheduler:
    def __init__(self):
        self.appointments = PriorityQueue()

    def schedule_appointment(self, appointment_time, patient_name):
        self.appointments.push(
            (appointment_time, patient_name), appointment_time)

    def cancel_appointment(self, appointment_time, patient_name):
        self.appointments.remove((appointment_time, patient_name))

    def next_appointment(self):
        return self.appointments.peek()
