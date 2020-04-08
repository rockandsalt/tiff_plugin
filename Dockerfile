FROM supervisely/base-py:latest

ENV PYTHONPATH /workdir:/workdir/src:/workdir/supervisely_lib/worker_proto:$PYTHONPATH

##############################################################################
# Additional project libraries
##############################################################################

RUN pip install --no-cache-dir \
        numpy \
        scikit-image

############### copy code ###############

COPY . /workdir