# This is an example FastScore 1.6.1 deployment utilizing the Docker Swarm ochestrator.

## Requirements

#### The lasest version of [Docker](www.docker.com) is required:

Docker installation instructions may be found here: [https://docs.docker.com/engine/installation/](https://docs.docker.com/engine/installation/)

#### Ensure the utility ```make``` is installed. To install ```make``` on Ubuntu execute:

```sudo apt-get install build-essential```

For RedHat/CentOS:

```yum install make```

For Mac OSX using brew:

```brew install make```

#### The FastScore 1.6.1 Command Line Interface (CLI) utility must be installed

[http://docs.opendatagroup.com/docs/getting-started-with-fastscore#installing-the-fastscore-cli](http://docs.opendatagroup.com/docs/getting-started-with-fastscore#installing-the-fastscore-cli)


# To launch a FastScore system with Docker Swarm:

1. To build any custom model environments and launch the swarm simply type

```
% make
```
2. To configure FastScore fleet:
```
% make config
```
which should give an output like this:

```
bash ./utils/config.sh
Configuring FastScore...
fastscore connect https://<hostname of machine or vm or container running Swarm>:8000
fastscore config set config.yaml
Checking fleet status...
fastscore fleet
Name            API           Health
--------------  ------------  --------
engine-1        engine        ok
engine-2        engine        ok
engine-3        engine        ok
engine-4        engine        ok
model-manage-1  model-manage  ok
bash ./utils/get_urls.sh
=======FastScore URLs=======
Dashboard URL:
https://<hostname of machine or vm or container running Swarm>:8000
Model Deploy URL:
http://<hostname of machine or vm or container running Swarm>:8888/?token=<token>
============================
```

3. When the build/deploy/config sequency is finished, view the Swarm visualizer by pointing a browser at:

```
http://<hostname of machine or vm or container running Swarm>:8080/
```
4. To look at FastScore Dashboard, point a browser at:

```
https://<hostname of machine or vm or container running Swarm>:8000/
```

5. Then point a browser to the URL with the token for exmaple:
WARNING: you MUST change "localhost" to the build machine name or IP.
```
http://<hostname of machine or vm or container running Swarm>:8888/?token=<token>
```
# Exporting and Importing the contents of Model Manage:

Sometimes it is useful to export the contents of Model Manage for example as a backup or to share/import with other instances of Model Manage.  

## To export the contents of Model Manage for importing later:

```% make export```

That will create a file called ```db-data-volume-export.tgz``` in the ```./mysql``` directory.

## To import a previous export of Model Manage contents:

Ensure there is a valid Model Manage export file name ```./msql/db-data-volume-export.tgz``` and execute:

```% make import```

NOTE: That both importing and exporting Model Manage state will automatically stop Swarm if it is runnning.

# FastScore Composer:

Composer requires the use of the Frontman Proxy at port 8000, so the Dashboard is now
accessible at 7999 instead.

First-time setup of Designer:
visit https://localhost:8000 and https://localhost:8000/api/1/service
and make sure that security certificate exemptions are set.

Then go to https://localhost:8012

The TensorFlow workflow should look like this (see Composer/workflow.yaml)

```yaml
Assets:
    Models:
    - Name: tf_sp500_lstm
      Environment: localrepo/engine:tensorflow
    - Name: preprocessor
    - Name: postprocessor
    - Name: alerter
    Streams:
    - Name: rest
Workflow:
    preprocessor:
        Inputs:
            0: rest
            2: rest
        Outputs:
            1: tf_sp500_lstm
            3: postprocessor
            5: alerter

    tf_sp500_lstm:
        Inputs:
            0: preprocessor
        Outputs:
            1: postprocessor

    postprocessor:
        Inputs:
            0: tf_sp500_lstm
            2: preprocessor
        Outputs:
            1: alerter

    alerter:
        Inputs:
            0: postprocessor
            2: preprocessor
        Outputs:
            1: rest
```

It can be helpful to observe the Composer logs (`docker logs -f fastscore_composer...`)
when deploying the workflow.

Note that the LSTM model **requires the environment `localrepo/engine:tensorflow`**
(set this in Designer from the edit window).

The workflow can also be deployed directly, using the REST API.

The preprocessor model uses two inputs: `close_prices.jsons` in slot 0 and
`cpi.jsons` in slot 2.

## To Score:

Use Dashboard to see which model is running on which engine, and then, in one
terminal window, do:
```
fastscore use [alerter engine]
fastscore model output -c
```

This will wait for any REST output received.

Next, in another window, do:
```
fastscore use [preprocessor engine]
head -60 data/close_prices.json | fastscore model input 0
head -60 data/cpi.jsons | fastscore model input 2
```

Check on the first terminal---you should see the scores produced by the model.
