ARG BASE_IMAGE=ghcr.io/agent-infra/sandbox:latest
FROM ${BASE_IMAGE}
ENV USER_UID=1000 \
    USER_GID=1000 \
    DISABLE_VNC=true \
    VNC_SERVER_PORT=-1 \
    DISABLE_BROWSER=true \
    DISABLE_CODE_SERVER=true \
    DISABLE_JUPYTER=true \
    DISABLE_NODEJS_REPL=true \
    JUPYTER_POOL_SIZE=0 \
    OPENCODE_SERVER_USERNAME=opencode \
    OPENCODE_DISABLE_AUTOUPDATE=true
LABEL com.pig4cloud.sandbox.runtime-defaults="1"

COPY --chmod=0755 start-opencode /usr/local/bin/pigx-start-opencode
COPY opencode-config.jq /opt/pigx/opencode-config.jq
LABEL com.pig4cloud.sandbox.opencode-launcher="2"

COPY --chmod=0555 workspace/ /opt/pigx/workspace/
LABEL com.pig4cloud.sandbox.workspace-tools="3"
