#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Define el punto de entrada
from nonmouse import *
import os, glob
from .interfaz import main_interfaz
from .selector import main_selector

def main():
    main_interfaz()  # Muestra la pantalla de bienvenida
    #main_selector()    # Luego ejecuta la ventana principal

if __name__ == "__main__":
     main_selector()


__copyright__    = 'Copyright (C) 2023 Yuki TAKEYAMA'
__version__      = '2.7.0'
__license__      = 'Apache-2.0'
__author__       = 'Yuki TAKEYAMA'
__author_email__ = 'namiki.takeyama@gmail.com'
__url__          = 'http://github.com/takeyamayuki/NonMouse'

__all__ = [
    os.path.split(os.path.splitext(file)[0])[1]
    for file in glob.glob(os.path.join(os.path.dirname(__file__), '[a-zA-Z0-9]*.py'))
]