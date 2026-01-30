# Build stage
FROM ghcr.io/astral-sh/uv:0.9.21 AS uv
FROM public.ecr.aws/lambda/python:3.12 AS builder

ENV UV_COMPILE_BYTECODE=1 UV_NO_INSTALLER_METADATA=1 UV_LINK_MODE=copy
WORKDIR /app

RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv export --frozen --no-emit-workspace --no-dev --no-editable -o requirements.txt && \
    uv pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Run stage
FROM public.ecr.aws/lambda/python:3.12 AS runner

COPY --from=builder ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}
COPY ./app ${LAMBDA_TASK_ROOT}/app

CMD ["app.lambda.handler"]