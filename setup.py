from setuptools import setup

setup(
    name= "couleurwest",
    version='1.0.0',
    packages=['home'],

    setup_requires=['libsass >= 0.21.0'],
    sass_manifests={'.': ('.sources/sass', 'static/xwork', 'static/css')}

)



"""
Copiright fonts : <div>Font made from <a href="http://www.onlinewebfonts.com">oNline a11y-atkinson</a>is licensed by CC BY 3.0</div>
 Copyright (c) 2011 by Santiago Orozco (hi@typemade.mx) with reserved name Italiana 
"""