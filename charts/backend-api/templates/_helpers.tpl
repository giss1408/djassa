{{- define "backend-api.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "backend-api.fullname" -}}
{{- printf "%s-%s" (include "backend-api.name" .) .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
