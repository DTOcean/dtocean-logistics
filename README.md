[![appveyor](https://ci.appveyor.com/api/projects/status/github/DTOcean/dtocean-logistics?branch=master&svg=true)](https://ci.appveyor.com/project/DTOcean/dtocean-logistics)
[![codecov](https://codecov.io/gh/DTOcean/dtocean-logistics/branch/master/graph/badge.svg)](https://codecov.io/gh/DTOcean/dtocean-logistics)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bb34506cc82f4df883178a6e64619eaf)](https://www.codacy.com/project/H0R5E/dtocean-logistics/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DTOcean/dtocean-logistics&amp;utm_campaign=Badge_Grade_Dashboard&amp;branchId=8410911)
[![release](https://img.shields.io/github/release/DTOcean/dtocean-logistics.svg)](https://github.com/DTOcean/dtocean-logistics/releases/latest)

# DTOcean Logistics Module

The DTOcean Logistics Module is a library for calculating optimal marine 
logistics, including port, vessel and equipment selection, and weather window 
analysis, in conjunction with the [dtocean-installation]( 
https://github.com/DTOcean/dtocean-installation) and [dtocean-maintenance]( 
https://github.com/DTOcean/dtocean-maintenance) DTOcean modules. Each operation 
is optimised either for minimum cost or for minimum duration. 

See [dtocean-app](https://github.com/DTOcean/dtocean-app) or [dtocean-core](
https://github.com/DTOcean/dtocean-app) to use this package within the DTOcean
ecosystem.

* For python 2.7 only.

## Installation

Installation and development of dtocean-logistics uses the [Anaconda 
Distribution](https://www.anaconda.com/distribution/) (Python 2.7)

### Conda Package

To install:

```
$ conda install -c dataonlygreater dtocean-logistics
```

### Source Code

Conda can be used to install dependencies into a dedicated environment from
the source code root directory:

```
conda create -n _dtocean_logis python=2.7 pip
```

Activate the environment, then copy the `.condrc` file to store installation  
channels:

```
$ conda activate _dtocean_logis
$ copy .condarc %CONDA_PREFIX%
```

Install [polite](https://github.com/DTOcean/polite) into the environment. For 
example, if installing it from source:

```
$ cd \\path\\to\\polite
$ conda install --file requirements-conda-dev.txt
$ pip install -e .
```

Finally, install dtocean-logistics and its dependencies using conda and pip:

```
$ cd \\path\\to\\dtocean-logistics
$ conda install --file requirements-conda-dev.txt
$ pip install -e .
```

To deactivate the conda environment:

```
$ conda deactivate
```

### Tests

A test suite is provided with the source code that uses [pytest](
https://docs.pytest.org).

If not already active, activate the conda environment set up in the [Source 
Code](#source-code) section:

```
$ conda activate _dtocean_logis
```

Install packages required for testing to the environment (one time only):

```
$ conda install -y pytest pytest-mock
```

Run the tests:

``` 
$ py.test tests
```

### Uninstall

To uninstall the conda package:

```
$ conda remove dtocean-logistics
```

To uninstall the source code and its conda environment:

```
$ conda remove --name _dtocean_logis --all
```

## Usage

Example scripts are available in the "examples" folder of the source code.

```
cd examples
python example.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

See [this blog post](
https://www.dataonlygreater.com/latest/professional/2017/03/09/dtocean-development-change-management/)
for information regarding development of the DTOcean ecosystem.

Please make sure to update tests as appropriate.

## Credits

This package was initially created as part of the [EU DTOcean project](
https://www.dtoceanplus.eu/About-DTOceanPlus/History) by:

 * Boris Teillant at [WavEC](https://www.wavec.org/)
 * Paulo Chainho at [WavEC](https://www.wavec.org/)
 * Pedro Vicente at [WavEC](https://www.wavec.org/)
 * Mathew Topper at [TECNALIA](https://www.tecnalia.com)
 * Adam Collin at [the University of Edinburgh](https://www.ed.ac.uk/)

It is now maintained by Mathew Topper at [Data Only Greater](
https://www.dataonlygreater.com/).

## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
