# this is an example of loading and iterating over a single file

import zstandard
import os
import json
import sys
from datetime import datetime
import logging.handlers


log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

#!!!!!!
location = ""
#!!!!!!


def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
	chunk = reader.read(chunk_size)
	bytes_read += chunk_size
	if previous_chunk is not None:
		chunk = previous_chunk + chunk
	try:
		return chunk.decode()
	except UnicodeDecodeError:
		if bytes_read > max_window_size:
			raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
		log.info(f"Decoding error with {bytes_read:,} bytes, reading another chunk")
		return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)


def read_lines_zst(file_name):
	with open(file_name, 'rb') as file_handle:
		buffer = ''
		reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
		#reader.read(40000000000)
		while True:
			chunk = read_and_decode(reader, 2**27, (2**29) * 2)

			if not chunk:
				break
			lines = (buffer + chunk).split("\n")

			for line in lines[:-1]:
				yield line, file_handle.tell()

			buffer = lines[-1]

		reader.close()


if __name__ == "__main__":
    year = sys.argv[1]
    file_lines = 0
    file_bytes_processed = 0
    created = None
    field = "subreddit"
    values = ["trans", "MtF", "ftm", "NonBinary", "truscum", "transgender"]
    results = []
    bad_lines = 0
    read_file_name = "RS_"+year+"-"
    file_index = 0
	# try:
    for x in range(12): 
        file_index += 1
        string_file_index = str(file_index)
        if file_index < 10: string_file_index = "0" + str(file_index)
        file_path = location + read_file_name + string_file_index + ".zst"
        results = []
        print("processing month: ", string_file_index)
        bad_lines = 0
        file_lines = 0
        file_size = os.stat(file_path).st_size
        for line, file_bytes_processed in read_lines_zst(file_path):
            try:
                obj = json.loads(line)
                created = datetime.utcfromtimestamp(int(obj['created_utc']))
                temp = obj[field] in values
                if temp: results.append(obj)
            except (KeyError, json.JSONDecodeError) as err:
                bad_lines += 1
            file_lines += 1
            if file_lines % 100000 == 0:
                log.info(f"{created.strftime('%Y-%m-%d %H:%M:%S')} : {file_lines:,} : {bad_lines:,} : {file_bytes_processed:,}:{(file_bytes_processed / file_size) * 100:.0f}%  : Results: {len(results)}")
        with open(location+year+"/"+string_file_index+".json", 'w') as json_file:
            json_result = {"data": results}
            json.dump(json_result, json_file)
            json_file.close()
        results = []
        # except Exception as err:
        # 	log.info(err)
        log.info(f"Complete : {file_lines:,} : {bad_lines:,}")
