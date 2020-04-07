FROM supervisely/base-py:latest
##############################################################################
# Additional project libraries
##############################################################################

RUN pip install --no-cache-dir \
        numpy \
        scikit-image

############### copy code ###############
ARG MODULE_PATH
COPY $MODULE_PATH /workdir
COPY supervisely_lib /workdir/supervisely_lib

ENV PYTHONPATH /workdir:/workdir/src:/workdir/supervisely_lib/worker_proto:$PYTHONPATH
WORKDIR /workdir/src