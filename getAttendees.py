#!/usr/bin/python3
# Get attendee list, output as csv 

# Imports
import argparse
import csv
from eventbrite import Eventbrite
import os
import sys

# Parameters
oauth = os.environ['EB']
event = 139076564749

# get eventbrite object

def get_attendees(oauth, event):
    """
    get attendees object
    """
    e = Eventbrite(oauth)
    return e.get_event_attendees(event)

def parse_attendees(attendees):
    """
    parse attendee object
    """
    attendee_list = []
    for attendee in attendees['attendees']:
        if attendee['status'] == 'Attending':
            attendee_list.append([attendee['profile']['first_name'], 
                                  attendee['profile']['last_name'],
                                  attendee['profile']['email']])
            if 'job_title' in attendee['profile']:
                attendee_list[-1].append(attendee['profile']['job_title'])
            else:
                attendee_list[-1].append("")
            attendee_list[-1].append(attendee['answers'][0]['answer'])
            attendee_list[-1].append(attendee['answers'][1]['answer'])
            if 'answer' in attendee['answers'][2]:
                attendee_list[-1].append(attendee['answers'][2]['answer'])
    return attendee_list


def write_attendee_csv(attendee_list):
    """
    Write attendees list to CSV file
    """
    att_writer = csv.writer(sys.stdout, quotechar='"')
    att_writer.writerow(['first_name', 'last_name', 'email', 'title', 'afilliation', 'presenter', 'pres_title'])
    for row in attendee_list:
        att_writer.writerow(row)

def main(args):
    """Run the CLI program"""
    at = get_attendees(oauth, event)
    attendee_list = parse_attendees(at)
    write_attendee_csv(attendee_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('event', type=str, default=event,
                        help='Eventbrite event ID')
    parser.add_argument('-o', '--oauth', type=str,
                        default=oauth,
                        help='Eventbrite oauth key')
    args = parser.parse_args()
    main(args) 
