#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

# PyGSM setup.py -- adapted from Django's with our heartfelt thanks

from __future__ import with_statement

from distutils.core import setup
from distutils.command.build_py import build_py as _build_py
from distutils.command.install import INSTALL_SCHEMES
import os
import sys
import commands
import traceback

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
wd = os.getcwd()
os.chdir('lib')
packages = [ 
    dir
    for dir,dirs,files
    in os.walk('pygsm')
    if '__init__.py' in files
    ]
os.chdir(wd)

# Dynamically calculate the version based on get_rapidsms_version()
# ... this way releases automagically get shipped with the version
# stored in the git tag, and installations (whether from releases or not)
# are tagged with a reasonably exact git version.
#
# removing this since it requires pyserial to be installed in order to be
# able to run python setup.py, doing it manually here instead
# 
#sys.path = ["lib"] + sys.path
#version = __import__("pygsm").get_version()
#
# copied over from pygsm.__init__
def get_version():
    # if not, can we figure it out from the git tag?
    import commands
    try:
        # see http://stackoverflow.com/questions/62264/#72874
        version = commands.getoutput("git describe --tags --always")
    except:
        # otherwise, give up!
        version = "unknown"
version = get_version()

class build_py (_build_py):
    def run (self):
        _build_py.run(self)
        if version == "unknown":
            print "PyGSM version unknown! Is git in your path?"
        else:
            vstring = "VERSION = '%s'" % version 
            vfilename = os.path.join(self.build_lib,
                        "pygsm", "__version__.py")
            try:
                with open(vfilename, 'w') as f:
                    f.write(vstring)
            except:
                traceback.print_exc()
            print "setting %s in %s" % (vstring, vfilename)

setup(
    name = "pygsm",
    version = version,
    maintainer = "RapidSMS development community",
    maintainer_email = "rapidsms@googlegroups.com",
    description = "Library for interfacing with GSM modems",
    url = "http://www.rapidsms.org/",
    package_dir = {'': 'lib'},
    packages = packages,
    # data_files = data_files,
    # package_data = {'rapidsms': ['skeleton/project/*.ini',
    #                             'skeleton/project/manage.py']},
    scripts = ['pygsm_demo'],
    cmdclass={'build_py': build_py},
    requires=["pyserial"],
    long_description = """
PyGSM is a Free and Open Source library for interfacing with
GSM modems and handsets to send and receive SMS messages.
"""
)
