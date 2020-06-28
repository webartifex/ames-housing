# Ames Housing

This repository is a case study of applying various machine learning models to
the problem of predicting house prices.

The dataset is publicly available and can be downloaded, for example, at
[Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques).

The case study is based on this [research paper](paper.pdf).

The analyses are presented in four notebooks that may be interactively worked
with by following these links:
- [Data Cleaning](https://mybinder.org/v2/gh/webartifex/ames-housing/master?urlpath=lab/tree/01_data_cleaning.ipynb)
- [Correlations](https://mybinder.org/v2/gh/webartifex/ames-housing/master?urlpath=lab/tree/02_pairwise_correlations.ipynb)
- [Visualizations](https://mybinder.org/v2/gh/webartifex/ames-housing/master?urlpath=lab/tree/03_descriptive_visualizations.ipynb)
- [Predictions](https://mybinder.org/v2/gh/webartifex/ames-housing/master?urlpath=lab/tree/04_predictive_models.ipynb)


## Installation

The project can be cloned and may be worked with under the MIT open source
license.
Python 3.7 was used to prepare and test the provided code.
Albeit the [poetry](https://python-poetry.org/) tool was used to manage the
dependencies, a [requirements.txt](requirements.txt) file is also provided as
an alternative.

On a Unix system, run:
- `git clone https://github.com/webartifex/ames-housing.git` (or use HTTPS
   instead)
- either `poetry install` or `pip install -r requirements.txt` (in the latter
  case, it is suggested that a virtual environment be used)
- after installation, `jupyter lab` opens a new tab in one's web browser where
  the notebooks and data files may be opened

Alternatively, the project should also be runnable with the
[Anaconda Distribution](https://www.anaconda.com/products/individual).


## About the Author

Alexander Hess is a PhD student at the Chair of Logistics Management at the
[WHU - Otto Beisheim School of Management](https://www.whu.edu) where he
conducts research on urban delivery platforms and teaches an introductory
course on Python (cf., [Fall Term 2019](https://vlv.whu.edu/campus/all/event.asp?objgguid=0xE57C2715B01B441AAFD3E79AA05CACCF&from=vvz&gguid=0x6A2B0ED5B2B949E69957A2099E7DE2F1&mode=own&tguid=0x3980A9BBC3BF4A638E977F2DC163F44B&lang=en),
[Spring Term 2020](https://vlv.whu.edu/campus/all/event.asp?objgguid=0x3354F4C108FF4E959CDD692A325D9AFE&from=vvz&gguid=0x262E29795DD742CFBDE72B12B69CEFD6&mode=own&lang=en&tguid=0x2E4A7D1FF3C34AD08FF07685461781C9)).

Connect him on [LinkedIn](https://www.linkedin.com/in/webartifex).

