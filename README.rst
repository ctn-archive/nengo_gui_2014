*********
nengo_gui
*********

HTML5 graphical interface for `Nengo <https://github.com/nengo/nengo>`_.  This
lets you see a Nengo model while you are constructing it.  It also integrates 
`Nengo Viz <https://github.com/nengo/nengo_viz>`_, a tool for visualizing and
interacting with a running Nengo model. 

Requirements
============

 - Python (tested with Python 2.7 and Python 3.4)
 - Nengo

Installation
============

To install the GUI, you need to download and install the code in this 
repository.  For most operating systems, here are the commands needed:

.. code:: shell

   git clone https://github.com/nengo/nengo_gui
   cd nengo_gui
   python setup.py develop --user
   cd ..
   
Note that this assumes you already have `Nengo <https://github.com/ctn-waterloo/nengo/>`_ installed.

The GUI will work on its own, but it is more useful with the visualizer as
well, so you can actually see what is going on.  Full instructions are
available `here <https://github.com/nengo/nengo_viz>`_, but these are the
basics:

.. code:: shell

   git clone https://github.com/nengo/nengo_viz
   cd nengo_viz
   python setup.py develop --user
   cd ..
   

Running Nengo GUI
=================

We run the Nengo GUI using the command ``nengo_gui``.  You can run this 
from the command prompt, or by double-clicking on the ``nengo_gui`` executable.  
On Windows, this is likely in a directory such as
``C:\Python27\Scripts\nengo_gui.exe``.  


Optional Alternate Visualizer
=============================

For backwards compatibility, Nengo GUI also supports the old Java-based
visualizer.  To install this, we need to download the old Java-based version
of Nengo.  Here are the instructions:

 - Download `this file <http://ctnsrv.uwaterloo.ca:8080/jenkins/job/Nengo/lastSuccessfulBuild/artifact/nengo-latest.zip>`_.
 - Unzip the file

Note that you do have to have `Java <http://java.com/>`_ installed on your computer for this to work.  Finally, you
need to install `RPyC <http://rpyc.readthedocs.org/>`_, which allows the editor and the visualizer to communicate.

.. code:: shell

   pip install rpyc
   
To use this visualizer, you must start the javaviz-server before starting
Nengo GUI.  This is a program that will sit in the background and handle the
visualization system.  Do this by going to the directory where you unzipped the old Java-based version
of nengo and running ``javaviz-server.bat`` (on Windows) or ``./javaviz-server`` (on Unix/Mac). 

A text window should pop up and a line like ``INFO:SLAVE/18812:server started on [127.0.0.1]:18812`` should appear.
Now you can run nengo_gui as discussed above.


Basic usage
===========

To view a Nengo model, run ``nengo_gui`` from the command line.  You can load scripts from the nengo_gui/scripts
folder from within the gui.

Using ``nengo_gui``
-------------------

If you're using ``nengo_gui``, then click the top right button to run
the interactive visualizer. (You can do this right away with the default network that loads, 
as a quick example).  If you don't
see the visualizer window, it may be hidden in the background; find it
in your OS's window bar.

For the new Nengo Viz visualizer, see the usage instructions
available `here <https://github.com/nengo/nengo_viz>`_.

For the old Java visualizer, right click on the background of the
visualizer to pick things to see; right click on the things to pick
data to plot. Items can be dragged to be moved around and resized
by the edges.  Plots can be customized by right-clicking on them.
The play button in the bottom-right starts the simulation.

Alternative usage
-----------------
You can pass nengo_gui a script to visualize, if desired.

.. code:: shell

   nengo_gui my_nengo_script.py
