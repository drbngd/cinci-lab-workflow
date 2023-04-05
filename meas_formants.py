
#!/usr/bin/env python

# Measure formants. Read input textgrids, call ifcformant on associated audio file,
# and output measurements to a .meas file.

Usage = 'meas_formants speaker file1.TextGrid [file2.TextGrid] ... [fileN.TextGrid]'

# You can also type *.TextGrid instead of naming them all in a list.

import audiolabel
import os, sys, subprocess
import re
import numpy as np
import psutil
import platform
from datetime import datetime
import datetime
import time

# Calculating processing time
start_time = time.time()

# For displaying system specifications
specs = ""

# Do minimal checking to ensure the script was called with appropriate
# arguments.
try:
    if not (sys.argv[1] == 'male' or
            sys.argv[1] == 'female' or
            sys.argv[1] == 'child'): raise
    sys.argv[2] != None
except:
    raise Exception('Usage: ' + Usage)

# Regular expression used to identify vowels.
vre = re.compile(
         "(?P<vowel>AA|AE|AH|AO|AW|AX|AXR|AY|EH|ER|EY|IH|IX|IY|OW|OY|UH|UW|UX)(?P<stress>\d)?"
      )

# The output header line.
head = '\t'.join(('t1 t2 lintime ifctime idx vowel stress \
                   rms f1 f2 f3 f4 f0 word'
                 ).split()) + '\n'

# Format string used for output.
fmt = '\t'.join(["{t1:0.4f}", "{t2:0.4f}", "{lintime:0.4f}", "{ifctime:0.4f}",
                "{idx:d}", "{vowel}", "{stress}", "{rms}", "{f1}", "{f2}",
                "{f3}", "{f4}", "{f0}", "{word}\n"
               ])

# Name to use for ifcformant output file.
tempifc = '__temp.ifc'

speaker = sys.argv[1]

ifc_args = ['ifcformant',
           '--speaker=' + speaker,
           '-e', 'gain -n -3 sinc -t 10 60 contrast',
           '--print-header',
           '--output=' + tempifc]

# Loop over all the input files specified on the command line.
for tg in sys.argv[2:]:
    fname = os.path.splitext(tg)[0]  # get filename without extension
    with open(fname + '.meas', 'w') as out:
    
        # Praat LabelManager.
        pm = audiolabel.LabelManager(from_file=tg, from_type='praat')
    
        # Create ifcformant results and read into ifc LabelManager.
        proc = subprocess.Popen(ifc_args + [fname + '.wav'], stderr=subprocess.PIPE)
        proc.wait()
        if proc.returncode != 0:
            for line in proc.stderr:
                sys.stderr.write(line + '\n')
            raise Exception("ifcformant exited with status: {0}".format(proc.returncode))
        ifc = audiolabel.LabelManager(from_file=tempifc, from_type='table', t1_col='sec')
        
        out.write(head)
    
        # Loop over all the vowel labels in the tier named 'phone'.
        for v, m in pm.tier('phone').search(vre, return_match=True):
            if v.duration > 1 and v.t1 != 0:
                continue
        
            # Safer to use center of a label as reference point than an edge.
            word = pm.tier('word').label_at(v.center)

         
            # Take measurements at start and end of vowel and at five
            # equally-spaced intervals in between them.
            for idx, t in enumerate(np.linspace(v.t1, v.t2, num=7)):
                meas = ifc.labels_at(t)
                out.write(fmt.format(t1=v.t1, t2=v.t2, lintime=t, ifctime=meas.f1.t1,
                                 idx=idx, vowel=m.group('vowel'), stress=m.group('stress'),
                                 rms=meas.rms.text, f1=meas.f1.text,
                                 f2=meas.f2.text, f3=meas.f3.text, f4=meas.f4.text,
                                 f0=meas.f0.text, word=word.text)#, 
#                                 context=context.text) #it is commented as we dont generate that field
                )

os.unlink(tempifc)		
