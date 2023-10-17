#!/usr/bin/env python3

def __virtualenv ():
	import os
	import pathlib
	import site
	import sys

	# ----

	DEFAULT_ASCEND = "0"

	# ----

	venv_verbose = os.environ.get ("VENV_VERBOSE", "0")
	if venv_verbose.lower () in ["y", "yes", "true", "on", "1"]:
		venv_verbose = True
	else:
		venv_verbose = False

	# ----

	def vprint (*args, force:bool = False, **kwargs):
		if venv_verbose is True or force is True:
			print ("VENV: ", file = sys.stderr, end = "", **kwargs)
			print (*args, file = sys.stderr, **kwargs)

	# ----

	venv_ascend = os.environ.get ("VENV_ASCEND", DEFAULT_ASCEND)
	try:
		venv_ascend = int (venv_ascend)
	except ValueError:
		vprint ("Invalid value for VENV_ASCEND: Must be base10 integer", force = True)
		venv_ascend = 0

	if venv_ascend < 0:
		venv_ascend = -1

	# ----

	# Start searching using the path to the directory containing this file
	try:
		base_dir = pathlib.Path (__file__).parent.resolve ()
	except NameError:
		base_dir = pathlib.Path ().absolute ()

	while True:
		if (base_dir / "pyvenv.cfg").is_file () and (base_dir / "bin" / "activate").is_file ():
			vprint (f"Found virtual environment: {base_dir}")

			# Pretty straight-forward
			bin_dir = base_dir / "bin"

			# Prepend virtual environment's bin directory to PATH
			os.environ ["PATH"] = os.pathsep.join ([str (bin_dir)] + os.environ.get ("PATH", "").split (os.pathsep))
			# Save the base pat of the virtual environment to VIRTUAL_ENV
			os.environ ["VIRTUAL_ENV"] = str (base_dir)

			# Save the number of sys.path items so it can be re-ordered after additions are made
			prev_length = len (sys.path)

			# Add each package directory to the site so libraries can be found
			for lib_path in [base_dir / "lib" / ("python%i.%i" % sys.version_info [0:2]) / "site-packages"]:
				vprint (f"Adding package directory: {lib_path}")
				site.addsitedir (path.decode ("utf-8") if "" else str (lib_path))

			# Move newly added package directories to the beginning of sys.path
			sys.path [:] = sys.path [prev_length:] + sys.path [0:prev_length]

			# Save the current sys.prefix
			sys.real_prefix = sys.prefix

			# Now override the prefix so that it's the base of the virtual environment
			sys.prefix = str (base_dir)

			vprint ("Active")
			break

		elif venv_ascend == 0:
			vprint ("Ran out of ascensions before finding a virtual environment")
			break

		elif base_dir == base_dir.parent:
			vprint ("Reached the top-level directory before finding a virtual environment")
			break

		else:
			# Scratch one off
			venv_ascend -= 1
			# Ascend
			base_dir = base_dir.parent
			vprint (f"Ascending to {base_dir}")

__virtualenv ()
del __virtualenv

# ==============================================================================
