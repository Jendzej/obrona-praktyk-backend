#!/bin/bash
docker run --env-file ./.env -p 5432:5432 -p 15432:15432 --name backend_db -d postgres