
from __future__ import print_function
import argparse
import urllib
import sys
import json
from gooey import Gooey
from gooey import GooeyParser
@Gooey      
def main():
  parser = argparse.ArgumentParser(description='Get OMDb data for a movie')
  parser.add_argument("-t", help="Movie title")
  parser.add_argument("-y", help="Year of release", type=int)
  parser.add_argument("-i", help="IMDb movie id")
  parser.add_argument("-r", help="Return raw XML/JSON response", choices=['JSON','XML'])
  parser.add_argument("--plot", help="Length of plot summary", choices=['short','full'])
  parser.add_argument("--tomatoes", help="Include Rotten Tomatoes data too", action="store_true")
  parser.add_argument("--type", help="movie, series, episode", choices=['movie','series','episode'])
  parser.add_argument("--season", help="season number", type=int)
  parser.add_argument("--episode", help="episode number", type=int)
  parser.add_argument("--format", help="Output formated in html, markdown or csv, leave out for text", choices=['html','markdown','csv'])
  args = parser.parse_args()

  params = {}
  keys = ['t', 'y', 'i', 'plot', 'r', 'tomatoes','type','season','episode']

  for k in keys:
    if args.__getattribute__(k): params[k] = args.__getattribute__(k)

  if len(params) == 0:
    parser.print_usage()
    sys.exit()


  ### call OMDb API

  apicall = urllib.urlopen('https://www.omdbapi.com/?%s' % urllib.urlencode(params))
  result = apicall.read()
  apicall.close()

  # print raw output and exit, if raw output was requested
  if args.r:
    print result
    sys.exit()
  if args.format == 'csv':
    result = result.replace('","', ',')
    chars_to_remove = ['"','[',']','{','}']
    result = result.translate(None, ''.join(chars_to_remove))
    print(result)
    sys.exit()
  # formats data as html
  elif args.format == 'html':
    result = result.replace('",', '<br>')
    result = result.replace('{','<br><br><br><p>')
    chars_to_remove = ['"','[',']']
    result = result.translate(None, ''.join(chars_to_remove))
    result = result.replace('}','</p>')
    print(result)
    sys.exit()

  # formats the data as markdown
  if args.format == 'markdown':
    result = result.replace('",', '\n')
    result = result.replace('{','##')
    chars_to_remove = ['"','[',']','}']
    result = result.translate(None, ''.join(chars_to_remove))
    print(result)
    sys.exit()
  
  # Encoding the data from --season option crashs the program this prints the data with out having to encode it
  if args.season:
    chars_to_remove = ['"', '[', ']','}']
    result = result.translate(None, ''.join(chars_to_remove))
    result = result.replace(',', '\n')
    result = result.replace('{','\n\n\n')
    print(result)
    sys.exit()
  # print requested info

  data = json.loads(result)
  for k in data:
    print(k.lower() + ":")
    print(data[k].encode('utf-8'))
    print("\n")

if __name__ == '__main__':
  main()
