# Jupyter Book

This repository builds a Jupyter Book environment that we can use to compile Duckietown books v2+.

## How to build

**NOTE:** these are instructions on how to use this image directly. While this is possible, we encourage
you to use the wrapper `dts` command, `dts docs build` instead.

Move to the root of a repository based on `template-book` of version `v2+`. 
For example, `https://github.com/duckietown/book-devmanual-docs`.

### Build HTML

Run the following command to run the jupyter-book environment and have it compile our book into HTML:

```shell
docker run -it --rm --user ${UID} -v ./src:/book -v ./html:/out/html duckietown/dt-jupyter-book:daffy
```

### Build PDF

Run the following command to run the jupyter-book environment and have it compile our book into PDF:

```shell
docker run -it --rm --user ${UID} -v ./src:/book -v ./pdf:/out/pdf duckietown/dt-jupyter-book:daffy
```

