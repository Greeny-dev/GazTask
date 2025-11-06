from . import http

TemplateTypes = (
    http.client.RequestToServer
    | http.client.ResponseFromServer
    | http.server.RequestFromClient
    | http.server.ResponseToClient
)
