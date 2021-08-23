# An Apollo entry guidance implementation in Python

This repository shows how to implement the Apollo entry guidance algorithm in Python. This is the version of the algorithm that was used by the NASA Mars Science Laboratory mission that landed the Curiosity rover on Mars. The code can be found in the `notebooks` folder in the form of some [jupyter notebooks](https://jupyter.org/) and associated python scripts.

This project is described in more detail in the video linked below and at this [blog post](https://www.thomasantony.com/2021/msl-apollo-guidance/).

[![How the Apollo Entry Guidance Algorithm Landed MSL on Mars - Simulated in Python](http://img.youtube.com/vi/3hf2--gw4Xk/0.jpg)](https://www.youtube.com/watch?v=3hf2--gw4Xk)

## Requirements

The Jupyter notebooks in the `notebooks` folder assumes that you have the packages specified in `requirements.txt` installed. If you do not have a working python environment installed, please use something like [Anaconda](https://www.anaconda.com/products/individual) to install one. Then install the dependencies in `requirements.txt` by running

```
pip install -r requirements.txt
```

## manim animations

The source code for generating the animations that are used in the video can be found in the `manim` folder. The notebook in that folder was run in a [Google Colab](https://colab.research.google.com) environment. Please see the [manim community edition](https://www.manim.community/) website for more information.
