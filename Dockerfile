FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY knowledge ./knowledge
COPY agent ./agent
COPY docs ./docs
ENV PYTHONUNBUFFERED=1
ENV AGENTESAP_MCP_SERVER_TRANSPORT=streamable-http
ENV AGENTESAP_MCP_SERVER_HOST=0.0.0.0
ENV AGENTESAP_MCP_SERVER_PORT=8000
ENV AGENTESAP_MCP_SERVER_PATH=/mcp
EXPOSE 8000
CMD ["python","-m","src.mcp.consultant_server"]
