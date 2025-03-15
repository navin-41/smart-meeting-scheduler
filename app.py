# Application

from datetime import datetime, timedelta
import calendar

class Smart_Meeting_Scheduler:
    def _init_(self):
        self.working_hours = []
        self.holidays = {"2025-01-01", "2025-12-25"}
        self.schedules = {}
    
    def is_working_day(self, date):
        weekday = date.weekday()
        return weekday < 5 and date.strftime("%Y-%m-%d") not in self.holidays
    
    def schedule_meeting(self, user, date_str, start_time, end_time):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if not self.is_working_day(date):
            return "Cannot schedule on weekends or holidays."
        
        start_dt = datetime.strptime(start_time, "%H:%M").time()
        end_dt = datetime.strptime(end_time, "%H:%M").time()
        
        if not (self.working_hours[0] <= start_dt.hour < self.working_hours[1] and 
                self.working_hours[0] < end_dt.hour <= self.working_hours[1] and 
                start_dt < end_dt):
            return "Invalid time slot. Must be within working hours."
        
        self.schedules.setdefault(user, {}).setdefault(date_str, [])
        for existing_start, existing_end in self.schedules[user][date_str]:
            if not (end_dt <= existing_start or start_dt >= existing_end):
                return "Time slot overlaps with an existing meeting."
        
        self.schedules[user][date_str].append((start_dt, end_dt))
        self.schedules[user][date_str].sort()
        return "Meeting scheduled successfully."
    
    def check_available_slots(self, user, date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if not self.is_working_day(date):
            return "No available slots on weekends or holidays."
        
        booked = self.schedules.get(user, {}).get(date_str, [])
        available_slots = []
        start = datetime.strptime(f"{self.working_hours[0]}:00", "%H:%M").time()
        
        for end in [slot[0] for slot in booked] + [datetime.strptime(f"{self.working_hours[1]}:00", "%H:%M").time()]:
            if start < end:
                available_slots.append((start, end))
            start = booked.pop(0)[1] if booked else end
        
        return available_slots or ["No available slots"]
    
    def view_meetings(self, user, date_str):
        return self.schedules.get(user, {}).get(date_str, "No meetings scheduled.")

scheduler = Smart_Meeting_Scheduler()
print(scheduler.schedule_meeting("Vicky", "2025-03-18", "10:00", "11:00"))
print(scheduler.check_available_slots("Vicky", "2025-03-18"))
print(scheduler.view_meetings("Vicky", "2025-03-18"))
