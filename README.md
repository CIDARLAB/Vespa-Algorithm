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
Continuous-Flow Microfluidic Devices (CFMDs), also known as biochips, provide automated and cost-effective solutions for biomolecular analysis in life science applications. Multi-step biochemical reactions have required incorporating microfluidic components into CFMDs, which may raise their design complexity and lead to Design-Objective-Constraint Compatibility (DOCC) conflicts. Existing validation methods excel in optimizing Control-Layer Pressurization Protocol (CLPP) for small networks. However, they face challenges in describing operation constraints for microfluidic large-scale integration (mLSI) experiments and addressing the leakage risk. For that, we developed Vespa, an open-source validation framework using logic expressions to describe operation constraints on a lower human labor cost. For each operation, taking an objective list, a constraint list, a design netlist, and a super-parameter as inputs, Vespa validates the DOCC by constructing a target fluid transportation path. In addition, it introduces a leakage risk mitigation mechanism, issuing warnings for incorrect constraints and potential fluid leakage risks. The work includes over 900 real-world and synthetic benchmarks in three complexity ranges to support researchers in the field. As a result, more than 85\% of benchmark experiments yield correct results within 0.3 seconds, enabling Vespa for real-time validation and integration into interactive CFMD design tools. Finally, to show Vespa's practical efficacy and real-world impact, we created case studies using a real-world CFMD. We demonstrated that Vespa eliminates over 90\% of DOCC-related wet lab tests by detecting issues and making updates before fabrication.

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

If it is the first time to test the random benchmarks, this command can automatically generate random Constraints by calling [ConstraintMaker.py](ConstraintMaker.py) and save it for the next time:
```sh
$ venv/bin/python3 TestAlgorithm.py
```

All Experiment objectives for Random Constraints are set to ['F1', 'F2']. User can edit it in [TestAlgorithm.py](TestAlgorithm.py).

### Literature Benchmarks
You can run this algorithm to test the given literature review benchmarks with this command:
```sh
$ venv/bin/python3 lrbtest.py
```

You can also create your own biochip design by editing [LRB_new.py](Literature_Review_Benchmarks_Generator/LRB_new.py).
And Create Constraint and Experiment objectives in [Constraint_UR_lrb_new.csv](TestCaseFiles/lrb/URC/Constraint_UR_lrb_new.csv).

## Maintainers

[@zyrrron](https://github.com/zyrrron).

## Contributing

Feel free to dive in! [Open an issue](https://github.com/zyrrron/VeSpA-Algorithm/issues/new) or submit PRs.

### Contributors

This project exists thanks to all the people who contribute. 

## License
