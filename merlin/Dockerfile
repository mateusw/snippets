FROM gcr.io/deeplearning-platform-release/pytorch-gpu.2-0.py310

USER root
WORKDIR /root

ENV PIP_ROOT_USER_ACTION=ignore
SHELL ["/bin/bash", "-c"]

#RUN pip install --no-dependencies jupyterlab-nvdashboard && jupyter labextension install jupyterlab-nvdashboard

RUN . /root/.bashrc && \
    conda create -n merlin python=3.10 -y && \
    conda install -n base conda-libmamba-solver -y && \
    conda config --set solver libmamba
 
SHELL ["conda", "run", "-n", "merlin", "/bin/bash", "-c"]
RUN conda install ipykernel -y && conda install -c rapidsai -c conda-forge -c nvidia cudf=23.06.01 dask-cudf -y

#REF:. https://github.com/NVIDIA-Merlin/Merlin
RUN pip install --no-cache-dir --upgrade pip && pip install "transformers4rec[pytorch,nvtabular]>=23.6.0" "fsspec>=2022.7.1" faiss-gpu "dask>=2022.11.1" "distributed>=2022.3.0" "merlin-core>=23.6.0" "nvtabular>=23.6.0" "merlin-systems>=23.6.0" "requests>=2.10" treelite==2.4.0 treelite_runtime==2.4.0 "torchmetrics>=0.10.0" pytorch-lightning lightning-utilities "merlin-dataloader>=23.6.0" "tensorflow>=2.9" "transformers>=4.23" "implicit>=0.5.2" "lightfm>=1.0.0" "merlin-models>=23.6.0" tritonclient[all]==2.33.* tensorrt

SHELL ["/bin/bash", "-c"]

# Copy and install requirements.in onto image
COPY requirements.in .
RUN pip install pip-tools
RUN pip-compile requirements.in --resolver=backtracking
RUN pip install -r requirements.txt

