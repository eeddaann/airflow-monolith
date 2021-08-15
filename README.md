# airflow-monolith

## Run airflow inside a single container
Since the default deployment of airflow involves multiple containers and we have limited quota of pods we wanted to run airflow in a single container for testing purposes.

**Don't use it at production...**

### usage
- building the image:
```bash
docker build . -t monoairflow
```
- running a container:
```bash
docker run -p 8080:8080 monoairflow
```

### remarks
- In case of ```permission denied``` while building the image, check ```run.sh``` permissions
- The docker image contains a script instead of chained commands to allow better handlling of errors. currently we implemented basic test to verify that the proccess is up but it can be extanded...