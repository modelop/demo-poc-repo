# Based on Jupyter data science stack notebook.
FROM jupyter/base-notebook

USER root

# R pre-requisites
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    vim \
    nano \
    fonts-dejavu \
    gfortran \
    libxrender1 \
    libcairo2 \
    build-essential \
    gcc && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER $NB_USER

# Install Python2

RUN conda create --quiet --yes -p $CONDA_DIR/envs/python2 python=2.7 \
    'nomkl' \
    'ipython=5.3*' \
    'ipywidgets=6.0*' \
    'pandas=0.19*' \
    'numexpr=2.6*' \
    'matplotlib=2.0*' \
    'scipy=0.19*' \
    'seaborn=0.7*' \
    'scikit-learn=0.18*' \
    'scikit-image=0.12*' && \
    conda remove -n python2 --quiet --yes --force qt pyqt && \
    conda clean -tipsy

# Install Python 3 libraries
RUN conda install --quiet --yes \
    'nomkl' \
    'ipywidgets=6.0*' \
    'pandas=0.19*' \
    'numexpr=2.6*' \
    'matplotlib=2.0*' \
    'scipy=0.19*' \
    'seaborn=0.7*' \
    'scikit-learn=0.18*' \
    'scikit-image=0.12*' && \
    conda remove --quiet --yes --force qt pyqt && \
    conda clean -tipsy

# Add shortcuts to distinguish pip for python2 and python3 envs
RUN ln -s $CONDA_DIR/envs/python2/bin/pip $CONDA_DIR/bin/pip2 && \
    ln -s $CONDA_DIR/bin/pip $CONDA_DIR/bin/pip3

# Some libraries not in conda
RUN pip2 install quickavro==0.1.21 --quiet
RUN pip3 install quickavro==0.1.21 --quiet

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /home/$NB_USER/.cache/
RUN MPLBACKEND=Agg $CONDA_DIR/envs/python2/bin/python -c "import matplotlib.pyplot"

# Install R

RUN conda config --system --add channels r && \
    conda install --quiet --yes \
    'rpy2' \
    'r-base=3.4.*' \
    'r-irkernel' \
    'r-plyr' \
    'r-devtools' \
    'r-tidyverse' \
    'r-shiny' \
    'r-rmarkdown' && conda clean -tipsy

# Install Python 2 kernel spec globally to avoid permission problems when NB_UID
# switching at runtime and to allow the notebook server running out of the root
# environment to find it. Also, activate the python2 environment upon kernel
# launch.
USER root

RUN pip install kernda --no-cache && \
    $CONDA_DIR/envs/python2/bin/python -m ipykernel install && \
    kernda -o -y /usr/local/share/jupyter/kernels/python2/kernel.json && \
    pip uninstall kernda -y

WORKDIR /fastscore/sdk/
# install fastscore SDK
COPY fastscore-dev.tar.gz /fastscore/sdk/
RUN tar xvf fastscore-dev.tar.gz
COPY fastscore-sdk/R /fastscore/sdk/R
COPY install.R /fastscore/

WORKDIR /fastscore/deploy/
COPY fastscoredeploy/python/ /fastscore/deploy/

# switch to Python2 SDK
# and install requirements
RUN /bin/bash -c "source /opt/conda/bin/activate python2 \
    && cd /fastscore/sdk/fastscore-dev/ \
    && python setup.py install \
    && cd /fastscore/deploy/ \
    && python setup.py install \
    && source /opt/conda/bin/deactivate python2"

# install Python3 SDK
RUN /bin/bash -c "cd /fastscore/sdk/fastscore-dev/ \
    && pip install avro-python3 \
    && python setup.py install \
    && cd /fastscore/deploy/ \
    && python setup.py install"

# install R SDK
RUN /bin/bash -c "Rscript /fastscore/install.R"

# Google Drive
RUN /bin/bash -c "pip2 install --upgrade google-api-python-client && \
    pip2 install --upgrade python-gflags && \
    pip3 install --upgrade google-api-python-client && \
    pip3 install --upgrade python-gflags"

RUN /bin/bash -c "pip2 install git+https://github.com/jupyter/jupyter-drive.git && \
    pip3 install git+https://github.com/jupyter/jupyter-drive.git"

# MySQL Client

RUN apt-get update && apt-get install -y mysql-client-5.7

USER $NB_USER

WORKDIR $HOME/work
COPY ["Python2 Example Usage.ipynb", "./"]
COPY ["R Example Usage.ipynb", "./"]
COPY ["Python3 Example Usage.ipynb", "./"]
# COPY ["PFA Example Usage.ipynb", "./"]
