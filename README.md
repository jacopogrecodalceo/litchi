# Litchi

Litchi is a Python package designed to create scores using Abjad (Lilypond) and read them with Csound. 

# Intall

`pip install git+https://github.com/jacopogrecodalceo/litchi.git`

# Exemple

```python
import threading
import abjad

from litchi import Litchi

def craft():
  

def run_litchi():
	litchi = Litchi()
  
  # load a lilypond file
	litchi.lilypond.load(file_path=path.build_ly, log_path=path.log)
  
	# here litchi analyse nodes
	node_events, node_tempi = litchi.lilypond.analyse()

	# load a file or a directory for csound orchestra
	litchi.csound.load(path.csound_dir)
  
 	# here it will play
	litchi.csound.process_events(node_events, node_tempi)
	litchi.csound.play(export_score=path.build_sco, export_orchestra=path.build_orc)

def main():
	craft()
	thread = threading.Thread(target=run_litchi)
	thread.start()

main()
```

