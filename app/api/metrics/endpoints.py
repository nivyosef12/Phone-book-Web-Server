import json
import time

from fastapi import APIRouter, HTTPException, Response, Query, Request, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.db import get_db
from app.common.logger import logger
from prometheus_client import generate_latest, REGISTRY
from prometheus_client.parser import text_string_to_metric_families


headers = {
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
}

router = APIRouter()


@router.get("/get_readable_metrics", tags=["metrics"])
async def readable_metrics():
    try:
        # get and parse the raw metrics
        logger.info("Getting raw metrics")
        raw_metrics = generate_latest(REGISTRY).decode("utf-8")

        logger.info("Parsing raw metrics")
        parsed_metrics = text_string_to_metric_families(raw_metrics)

        # format the metrics for readability
        logger.info("Formmating")
        formatted_metrics = []
        for family in parsed_metrics:
            for sample in family.samples:
                metric_name = sample.name
                metric_value = sample.value
                metric_labels = ", ".join(f"{k}={v}" for k, v in sample.labels.items())
                formatted_metrics.append(f"{metric_name}{{{metric_labels}}}: {metric_value}")

        readable_output = "\n".join(formatted_metrics)
        return Response(content=readable_output, media_type="text/plain")

    except Exception as e:
        logger.error(f"Error while getting metrics - {e}")
        return Response(content=f"Error while getting metrics - {e}", media_type="text/plain")