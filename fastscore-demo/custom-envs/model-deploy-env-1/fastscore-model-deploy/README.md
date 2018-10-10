# fastscore-model-deploy

FastScore Model Deploy is a containerized version of the FastScore SDK with built-in 
tools to make model development and deployment easier for data scientists. 

## The Model Deploy Docker Container

The Model Deploy container is based on the Jupyter
Data Science Notebook stack (DockerHub: `jupyter/datascience-notebook`).

### Building

Build the Docker container with:
```
docker build --tag fastscore/model-deploy:dev .
```
(Note: it may take a while to pull `jupyter/datascience-notebook`, as the image
  is quite large)

### Usage

Run it with the following command:
```
docker run -it --rm -p 8888:8888 --net="host" fastscore/model-deploy:dev
```
Note that the `--net="host"` option is optional; it just makes it more convenient
to access other FastScore containers using `localhost`.

The working directory of the user is `/home/jovyan/work`. There are example
notebooks in this directory demonstrating the functionality:

* `Python2 Example Usage.ipynb` - Create and deploy an example Python2 model.
* `Python3 Example Usage.ipynb` - Create and deploy an example Python3 model.
* `R Example Usage.ipynb`       - Create and deploy an example R model.
* `PFA Example Usage.ipynb`     - Create and deploy PFA and PrettyPFA models.
