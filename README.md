# `gpx_reader`
  
A tool to read GPX files and rename the files according to the location and time of the track.

# usage
## to rename your .gpx files

import the function rename: `from gpx_reader import rename`.  
call the function, with the argument the folder containing the files as the first argument, and the folder where to write the new files as second argument:  
`rename('input_files', 'output_folder')`

optionally, set the keyword argument `move=True` in order to delete the files after being processed:  
`rename('input_files', 'output_folder', move=True)`
