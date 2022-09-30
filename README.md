# Vespa - Biochip Design Verification Algorithm 
<!-- # Standard Readme -->

<!--[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
-->

## Table of Contents

- [Overview](#overview)
- [Install](#install)
- [Usage](#usage)
	- [Random Benchmarks](#random)
    - [Literature Benchmarks](#literature)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
    - [Contributors](#contributors)
- [License](#license)

## Overview
Microfluidic devices, also known as biochips, are a cost-effective, 
highly automated alternative to traditional biomolecular analysis in life science 
applications. Recently, biochips increasingly incorporate ideas from traditional 
electronic design paradigms like VLSI (Very Large Scale Integration) to increase 
their complexity in multi-step biological experiments. This complexity requires a 
carefully ordered control sequence and an optimally designed layout of microfluidic 
components responsible for moving fluids and materials for correct operations. 
Many design algorithms propose a solution by generating novel microfluidic architectures 
or specializing in identifying conflicts for a limited set of design topologies. 
However, they only identify layout conflicts, not those conflicts caused by operation 
constraints during the design process. This limitation potentially introduces much 
higher post-fabrication costs due to the design iterations. Thus, a framework for 
generalizable control and fluid path verification is necessary. In this paper, we 
present a biochip logic verification algorithm based on constrained path searches. 
According to over 900 real-world and synthetic benchmark results, given a two-layer 
continuous-flow biochip, liquid entries and exits, a set of transportation logic 
constraints, our novel approach can identify the fluid path and predict the 
corresponding valve states for execution with a 0\% error rate ignoring time 
constraints, in contrast to an average of 62.7\% for A* and 62.5\% for Dijkstra. We 
also provide the first generalized problem formalization, a corresponding open-source 
software package, and a community collection of over 900 real-world, synthetic 
benchmarks. Finally, experimental results demonstrate that our approach can give 
the correct flow pathway and control instructions for real-world biochip experiments 
and identify conflicts.

## Install

Download the repository from GitHub, create a venv environment, and install the necessary packages. Here we use python3.8 as the python interpreter.

```sh
$ git clone https://github.com/zyrrron/VeSpA-Algorithm.git
$ cd Vespa-Algorithm
$ python3 -m venv venv/
$ venv/bin/pip3 install -r requirements.txt
```

After you install all the packages, you are able to run the algorithm.

## Usage


### Random Benchmarks
You can run this algorithm to test the given random benchmarks with this command:
```sh
$ venv/bin/python3 TestAlgorithm.py
```

If you want to generate random benchmarks by your self, you can use this command to generate random designs:
```sh
$ venv/bin/python3 RandomCaseGenerator.py
```

If it is the first time to test the random benchmarks, this command can automatically generate Constraints by calling [ConstraintMaker.py](ConstraintMaker.py) and save it for the next time:
```sh
$ venv/bin/python3 TestAlgorithm.py
```

All User Requirements for Random Constraints are set to ['F1', 'F2']. User can edit it in [TestAlgorithm.py](TestAlgorithm.py).

### Literature Benchmarks
You can run this algorithm to test the given literature review benchmarks with this command:
```sh
$ venv/bin/python3 lrbtest.py
```

You can also create your own biochip design by editing [LRB_new.py](Literature_Review_Benchmarks_Generator/LRB_new.py).
And Create Constraint and User Requirements in [Constraint_UR_lrb_new.csv](TestCaseFiles/lrb/URC/Constraint_UR_lrb_new.csv).

## Maintainers

[@zyrrron](https://github.com/zyrrron).

## Contributing

Feel free to dive in! [Open an issue](https://github.com/zyrrron/VeSpA-Algorithm/issues/new) or submit PRs.

### Contributors

This project exists thanks to all the people who contribute. 

## License