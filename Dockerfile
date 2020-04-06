FROM python:3
##############################################################################
# Additional project libraries
##############################################################################

RUN pip install --no-cache-dir \
        numpy \
        scikit-image

############### copy code ###############
COPY . /workdir

ENV PYTHONPATH /workdir:/workdir/src:/workdir/supervisely_lib/worker_proto:$PYTHONPATH