FROM gitpod/workspace-full:latest

USER gitpod

RUN pip3 install poetry

## Fix while we can't add our own plugin
ENV GITPOD_STATIC_PLUGINS=/var/vsix
USER root
RUN mkdir -p /var/vsix/ && cd /var/vsix/ && \
    wget -q https://open-vsx.org/api/littlefoxteam/vscode-python-test-adapter/0.6.6/file/littlefoxteam.vscode-python-test-adapter-0.6.6.vsix && \
    chown gitpod:gitpod -R /var/vsix/
USER gitpod
