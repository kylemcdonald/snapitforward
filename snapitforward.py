# queue
# add friends

import glob
import json
import time
import os.path
from datetime import datetime
from snapchat import Snapchat

def log(msg):
	print ("{0}\t{1}".format(datetime.now(), msg))

def date_serializer(obj):
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial

s = None
previous_snaps = None
credentials = json.load(open('credentials.json'))

try:
	while True:
		time.sleep(5)

		if not s or not s.logged_in:
			log ('Logging in to {0}'.format(credentials['username']))
			s = Snapchat(credentials['username'], credentials['password'])	
			log ('Logged in')

		snaps = s.get_snaps()
		if previous_snaps == snaps:
			log ('No new snaps')
			continue
		previous_snaps = snaps

		for snap in snaps:
			sender = snap['sender']

			if snap['status'] == 2:
				# log ('Status is 2, ignoring')
				continue 
			if not sender:
				# log ('Snap has no sender, ignoring')
				continue
			if sender == credentials['username']:
				# log ('Snap is a sent message, ignoring')
				continue
			if snap['media_type']:
				# log ('Snap is not an image, ignoring')
				continue

			log ('Processing snap {0} from {1}'.format(snap['id'], snap['sender']))

			media_path = 'cache/' + snap['id']

			if os.path.isfile(media_path):
				log ('Already downloaded ' + snap['id'])
				continue

			log ('Writing history')
			try:
				with open('history.json'.format(datetime.now()), 'w') as f:
					f.write(json.dumps(snaps, default=date_serializer, indent=2))
			except TypeError as e:
				log ('Error saving history: {0}'.format(e))

			log ('Downloading ' + snap['id'])
			media = s.get_media(snap['id'])

			# log ('Marking {0} as seen'.format(snap['id']))
			# s.mark_seen(snap['id'])

			if media == None:
				log ('Cannot download ' + snap['id'])
				continue

			log ('Successfully downloaded ' + snap['id'])

			try:
				with open(media_path, 'w') as f:
					log ('Writing to cache from ' + snap['id'])
					f.write(media)
			except TypeError as e:
				log ('Error saving file: {0}'.format(e))

			queue = glob.glob('queue/*')
			if len(queue):
				queue_file = queue[0]
				log ('Uploading item from {0}'.format(queue_file))
				# possible that the media did not upload
				media_id = s.upload(Snapchat.MEDIA_IMAGE, queue_file)
				log ('Sending {0}'.format(media_id))
				# possible that the media did not send
				s.send(media_id, sender)
				log ('Deleting ' + queue_file)
				os.remove(queue_file)

			try:
				with open('queue/' + snap['id'], 'w') as f:
					log ('Writing to queue from ' + snap['id'])
					f.write(media)
			except TypeError as e:
				log ('Error saving file: {0}'.format(e))

except KeyboardInterrupt:
	s.logout()
	log('Logging out')