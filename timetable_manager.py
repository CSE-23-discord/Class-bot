import csv
from datetime import datetime, timedelta, date
import calendar

filename = 'timetable.csv'

def get_timetable():

	timetable = {}

	times = []

	with open(filename, 'r') as FPtr: 
		
		reader = csv.reader(FPtr)
		
		for row in reader:

			if not times and not row[0]:
				for i in range(1, len(row)):
					times.append(row[i])

			if row[0] and row [0] not in timetable:

				timetable[row[0]] = {}

				for i in range(len(row)):
					
					if i == 0:
						continue
					
					timetable[row[0]][times[i - 1]] = row[i]

	return {
		'timetable': timetable, 
		'times': times
	}

def get_time_diff(time_list):

	start_time = datetime.strptime(time_list[0], '%H:%M').time()
	end_time = datetime.strptime(time_list[1], '%H:%M').time()
	
	date_time1 = datetime.combine(date.today(), start_time)
	date_time2 = datetime.combine(date.today(), end_time)
	# Get the difference between datetimes (as timedelta)
	
	return int((date_time2 - date_time1).total_seconds() / 60)

def check_class(now):

	today = calendar.day_abbr[now.weekday()]

	if today == 'Sat' or today == 'Sun':

		next_monday_date = now + timedelta(days =- today.weekday(), weeks=1)

		start_time = datetime.strptime('10:15', '%H:%M').time()

		next_monday = datetime.combine(next_monday_date, start_time)

		diff = next_monday - today

		sleep_time = int(diff.total_seconds() / (60))
		
		return {
			'content': 'Enjoy your weekend.',
			'sleep_time': sleep_time
		}

	elif now.hour >= 16:
		
		tomorrow_date = now + timedelta(days = 1)
		start_time = datetime.strptime('10:15', '%H:%M').time()
		tomorrow = datetime.combine(tomorrow_date, start_time)
		diff = tomorrow - today

		sleep_time = int(diff.total_seconds() / (60))

		return {
			'content' : "That's the end for all the lectures. Enjoy the rest of you day :)",
			'sleep_time': sleep_time
		}

	else:

		timetable_data = get_timetable()

		# print(datetime.now().time())

		for time_str in timetable_data['times']:
			
			class_times = time_str.split('-')
			# start_time = datetime.strptime(class_times[0], '%H:%M').time()

			cur_time_diff = get_time_diff(['{}:{}'.format(now.hour, now.minute), class_times[0]])

			if cur_time_diff <= 0:
				continue

			# TODO: handle index out of range

			elif cur_time_diff <= 15:

				print('Time left for next class: {} min'.format(cur_time_diff))

				lec_data = timetable_data['timetable'][today][time_str]
				sleep_time = get_time_diff(['{}:{}'.format(now.hour, now.minute), class_times[0]])

				sleep_time -= 15

				print("Next class: {}".format(lec_data))
				print("Sleep for {} beacause {}".format(sleep_time, class_times))

				return {
					'content': lec_data, 
					'sleep_time': sleep_time
				}
			
			else:

				lec_data = timetable_data['timetable'][today][time_str]
				sleep_time = get_time_diff(['{}:{}'.format(now.hour, now.minute), class_times[0]])
				sleep_time -= 15

				print('Chill, lot of time left for the next class at {}'.format(class_times[0]))
				print("Sleep for {} beacause {}".format(sleep_time, class_times[0]))

				return {
					'content': 'More than 30 mins left for next class. I will remind 15 mins before class',
					'sleep_time': sleep_time
				}

	# TODO: return class text and sleep time


if __name__ == "__main__":
	
	check_class(datetime.now())
	# print(get_timetable()['timetable'])