# Victor.I - Django API views; uses existing src/ for parsing and agent.
import sys
import logging
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import os
import pandas as pd
from django.http import JsonResponse

logger = logging.getLogger(__name__)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status

# In-memory store for uploaded datasets (dev only; use DB/cache in production)
_data_store = {}


def _infer_column_types(df):
    out = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        if "int" in dtype or "float" in dtype:
            out.append({"name": col, "type": "Numeric"})
        elif "object" in dtype or "str" in dtype:
            out.append({"name": col, "type": "Text"})
        else:
            out.append({"name": col, "type": dtype})
    return out


def _suggested_questions(column_names, column_types):
    """Build example questions from column names so users can click to ask."""
    cols = column_names or []
    types = {t["name"]: t["type"] for t in (column_types or []) if isinstance(t, dict)}
    suggestions = []
    numeric = [c for c in cols if types.get(c) == "Numeric"]
    text = [c for c in cols if types.get(c) == "Text"]
    name_col = next((c for c in text if "product" in c.lower() or "item" in c.lower() or "name" in c.lower()), text[0] if text else None)
    qty_col = next((c for c in numeric if "quantity" in c.lower() or "qty" in c.lower()), None)
    rev_col = next((c for c in numeric if "revenue" in c.lower() or "sales" in c.lower()), None)
    date_col = next((c for c in cols if "date" in c.lower()), None)
    cat_col = next((c for c in text if "category" in c.lower() or "region" in c.lower()), None)
    if name_col and qty_col:
        suggestions.append(f"Which {name_col.replace('_', ' ')} has the highest {qty_col.replace('_', ' ')}?")
    if rev_col:
        suggestions.append(f"What is the total {rev_col.replace('_', ' ')}?")
    if name_col and rev_col:
        suggestions.append(f"Show me the top 5 {name_col.replace('_', ' ')} by {rev_col.replace('_', ' ')}")
    if date_col and numeric:
        suggestions.append(f"Show me a chart of {numeric[0].replace('_', ' ')} over time")
    if cat_col and numeric:
        suggestions.append(f"Compare {cat_col.replace('_', ' ')} by {numeric[0].replace('_', ' ')}")
    if numeric:
        suggestions.append(f"What is the average {numeric[0].replace('_', ' ')}?")
    if len(suggestions) < 3:
        suggestions.extend(["Show me a chart of the data", "Give me a summary of the data"])
    return suggestions[:6]


@api_view(["POST"])
def upload_csv(request):
    parser_classes = (MultiPartParser,)
    if "file" not in request.FILES:
        return Response(
            {"error": "No file provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    file = request.FILES["file"]
    if not file.name.lower().endswith(".csv"):
        return Response(
            {"error": "Only CSV files are allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    upload_dir = REPO_ROOT / "data" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / file.name
    try:
        with open(file_path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        from src.data_ingestion.csv_parser import CSVParser
        from src.data_cleaning.cleaner import DataCleaner

        csv_parser = CSVParser()
        data_cleaner = DataCleaner()
        parse_result = csv_parser.parse_csv(str(file_path))
        if parse_result.get("status") == "error":
            return Response(
                {"error": parse_result.get("error", "Parse failed")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        df = parse_result.get("dataframe")
        if df is None:
            return Response(
                {"error": "Parser returned no dataframe"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cleaned_df, _ = data_cleaner.clean_dataframe(df)
        dataset_id = file.name.replace(".csv", "").replace(".", "_")
        _data_store[dataset_id] = {
            "dataframe": cleaned_df,
            "metadata": {
                "filename": file.name,
                "rows": len(cleaned_df),
                "columns": len(cleaned_df.columns),
                "column_names": cleaned_df.columns.tolist(),
            },
        }
        column_types = _infer_column_types(cleaned_df)
        suggested_questions = _suggested_questions(
            cleaned_df.columns.tolist(), column_types
        )
        return Response(
            {
                "dataset_id": dataset_id,
                "filename": file.name,
                "rows": len(cleaned_df),
                "columns": len(cleaned_df.columns),
                "column_names": cleaned_df.columns.tolist(),
                "column_types": column_types,
                "suggested_questions": suggested_questions,
                "status": "success",
            }
        )
    except Exception as e:
        logger.exception("Upload CSV failed")
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def query(request):
    data = request.data
    dataset_id = data.get("dataset_id")
    question = data.get("question")
    if not dataset_id or not question:
        return Response(
            {"error": "dataset_id and question are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if dataset_id not in _data_store:
        return Response(
            {"error": "Dataset not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    df = _data_store[dataset_id]["dataframe"]
    try:
        from src.conversational.openai_agent import OpenAIAnalyticsAgent

        agent = OpenAIAnalyticsAgent()
        agent.load_data(df)
        result = agent.ask(question)
        out = {
            "answer": result.get("answer", ""),
            "chart_data": result.get("chart_data"),
        }
        if "confidence" in result:
            out["confidence"] = result["confidence"]
        return Response(out)
    except Exception as e:
        return Response(
            {"error": str(e), "answer": None, "chart_data": None},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def list_datasets(request):
    datasets = [
        {
            "dataset_id": ds_id,
            "metadata": data["metadata"],
        }
        for ds_id, data in _data_store.items()
    ]
    return Response({"datasets": datasets, "total": len(datasets)})


@api_view(["GET"])
def get_preview(request, dataset_id):
    if dataset_id not in _data_store:
        return Response(
            {"error": "Dataset not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    df = _data_store[dataset_id]["dataframe"]
    n = min(10, len(df))
    rows = df.head(n).fillna("").to_dict(orient="records")
    return Response({"rows": rows, "columns": df.columns.tolist()})


@api_view(["GET"])
def health(request):
    return Response({"status": "healthy", "service": "django"})
