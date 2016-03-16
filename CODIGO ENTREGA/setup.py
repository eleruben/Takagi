from distutils.core import setup 
import py2exe 
import numpy
 
setup(name="Nombre ejecutable", 
 version="1.0", 
 description="Breve descripcion", 
 author="autor", 
 author_email="email del autor", 
 url="url del proyecto", 
 license="tipo de licencia", 
 scripts=["appLista.py"], 
 console=["appLista.py"], 
 options={"py2exe": {"bundle_files": 3}}, 
 zipfile=None,
)