import discord
import pytz
from datetime import datetime, timedelta

client = discord.Client()
attendance_channel_id = 1234567890  # Replace with the ID of your attendance channel
report_channel_id = 1234567890  # Replace with the ID of the channel you want to send the report to
admin_role_id = 1234567890  # Replace with the ID of your admin role

# Replace these with the appropriate emojis
yes_emoji = '✅'
no_emoji = '❌'
tentative_emoji = '❔'

attendance_start_time = None
attendance_end_time = None

# Set up the attendance grid
class AttendanceGrid:
    def __init__(self):
        self.users = {}
        self.yes_count = 0
        self.no_count = 0
        self.tentative_count = 0
        self.not_responded_count = 0

    def add_user(self, user_id):
        self.users[user_id] = {
            'response': None,
            'late': False,
            'attended': False,
            'sign_on_time': None,
            'sign_off_time': None
        }

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]

    def set_response(self, user_id, response):
        if response == yes_emoji:
            self.yes_count += 1
        elif response == no_emoji:
            self.no_count += 1
        elif response == tentative_emoji:
            self.tentative_count += 1
        else:
            self.not_responded_count += 1
        self.users[user_id]['response'] = response

    def set_late(self, user_id, late):
        self.users[user_id]['late'] = late

    def set_attended(self, user_id, attended):
        self.users[user_id]['attended'] = attended

    def set_sign_on_time(self, user_id, sign_on_time):
        self.users[user_id]['sign_on_time'] = sign_on_time

    def set_sign_off_time(self, user_id, sign_off_time):
        self.users[user_id]['sign_off_time'] = sign_off_time

    def get_response_count(self, response):
        if response == yes_emoji:
            return self.yes_count
        elif response == no_emoji:
            return self.no_count
        elif response == tentative_emoji:
            return self.tentative_count
        else:
            return self.not_responded_count

    def get_user_responses(self):
        response_list = []
        for user_id, data in self.users.items():
            response_list.append(f"{client.get_user(user_id).mention}: {data['response']}")
        return response_list

    def get_user_attendance(self):
        attendance_list = []
        for user_id, data in self.users.items():
            if data['response'] == yes_emoji and not data['attended']:
                if data['late']:
                    late = "Yes"
                else:
                    late = "No"
                if data['sign_on_time'] and data['sign_off_time']:
                    sign_on_time = data['sign_on_time'].strftime('%m/%d/%Y %I:%M %p')
                    sign_off_time = data['sign_off_time'].strftime('%m/%d/%Y %I:%M %p')
                    attendance_list.append(f"{client.get_user(user_id).mention}: Yes (Late: {late}, Sign On: {sign_on_time}, Sign Off: {sign_off_time})
