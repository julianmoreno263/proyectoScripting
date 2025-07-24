#!/bin/bash

LOG_DIARIO="log_diario.log"
MAILTRAP_TOKEN="dd0cb78a8fbef788439f8a439a494175"
TO_EMAIL="osorto345@gmail.com"
FROM_EMAIL="hello@demomailtrap.co"

curl --ssl-reqd \
  --url 'smtp://live.smtp.mailtrap.io:587' \
  --user "api:$MAILTRAP_TOKEN" \
  --mail-from "$FROM_EMAIL" \
  --mail-rcpt "$TO_EMAIL" \
  --upload-file - <<EOF
From: Sistema Facturación <$FROM_EMAIL>
To: Administrador <$TO_EMAIL>
Subject: Log diario del sistema de facturación
Content-Type: text/plain; charset="utf-8"

Estimado administrador,

Adjunto el contenido del log generado hoy:

$(cat "$LOG_DIARIO")

Saludos,
Sistema de Facturación Automático

EOF
