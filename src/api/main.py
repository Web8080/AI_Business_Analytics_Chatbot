"""
FastAPI Backend - Main API application
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from pathlib import Path
import os
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from config import get_settings, setup_directories
from src.data_ingestion.pdf_parser import PDFParser
from src.data_ingestion.csv_parser import CSVParser
from src.data_cleaning.cleaner import DataCleaner
from src.analytics.descriptive import DescriptiveAnalytics
from src.analytics.diagnostic import DiagnosticAnalytics
from src.analytics.predictive import PredictiveAnalytics
from src.analytics.prescriptive import PrescriptiveAnalytics
from src.visualization.charts import ChartGenerator
from src.conversational.agent import ConversationalAgent
from src.reports.generator import ReportGenerator

# Initialize settings and directories
settings = get_settings()
setup_directories()

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Analytics Intelligence System",
    description="Automated analytics system with conversational AI interface",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
pdf_parser = PDFParser()
csv_parser = CSVParser()
data_cleaner = DataCleaner()
descriptive_analytics = DescriptiveAnalytics()
diagnostic_analytics = DiagnosticAnalytics()
predictive_analytics = PredictiveAnalytics()
prescriptive_analytics = PrescriptiveAnalytics()
chart_generator = ChartGenerator()
report_generator = ReportGenerator()

# Initialize conversational agent
conversational_agent = ConversationalAgent(
    api_key=settings.openai_api_key,
    model=settings.openai_model
)

# In-memory storage for processed data (use database in production)
data_store = {}


# Pydantic models
class QueryRequest(BaseModel):
    """Request model for natural language queries"""
    question: str
    dataset_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class AnalyticsRequest(BaseModel):
    """Request model for analytics operations"""
    dataset_id: str
    analysis_type: str
    parameters: Optional[Dict[str, Any]] = None


class ReportRequest(BaseModel):
    """Request model for report generation"""
    dataset_id: str
    report_type: str = "comprehensive"
    include_visualizations: bool = True


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Analytics Intelligence System",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "api": "operational",
            "conversational_agent": "operational",
            "analytics_engine": "operational"
        }
    }


@app.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload and parse CSV file
    """
    try:
        logger.info(f"Received CSV upload: {file.filename}")
        
        # Save file
        file_path = Path("data/uploads") / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse CSV
        parse_result = csv_parser.parse_csv(str(file_path))
        
        if parse_result['status'] == 'error':
            raise HTTPException(status_code=400, detail=parse_result.get('error'))
        
        # Clean data
        df = parse_result['dataframe']
        cleaned_df, cleaning_report = data_cleaner.clean_dataframe(df)
        
        # Generate dataset ID
        dataset_id = file.filename.replace('.csv', '').replace('.', '_')
        
        # Store in memory
        data_store[dataset_id] = {
            'dataframe': cleaned_df,
            'metadata': {
                'filename': file.filename,
                'rows': len(cleaned_df),
                'columns': len(cleaned_df.columns),
                'column_names': cleaned_df.columns.tolist()
            },
            'parsing_report': parse_result,
            'cleaning_report': cleaning_report
        }
        
        return {
            'dataset_id': dataset_id,
            'filename': file.filename,
            'rows': len(cleaned_df),
            'columns': len(cleaned_df.columns),
            'column_names': cleaned_df.columns.tolist(),
            'cleaning_report': cleaning_report,
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Error uploading CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and parse PDF file
    """
    try:
        logger.info(f"Received PDF upload: {file.filename}")
        
        # Save file
        file_path = Path("data/uploads") / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Parse PDF
        parse_result = pdf_parser.parse_pdf(str(file_path))
        
        if parse_result['status'] == 'error':
            raise HTTPException(status_code=400, detail=parse_result.get('error'))
        
        # Extract tables and clean
        datasets = {}
        for i, table_info in enumerate(parse_result.get('tables', [])):
            df = table_info['dataframe']
            cleaned_df, cleaning_report = data_cleaner.clean_dataframe(df)
            
            dataset_id = f"{file.filename.replace('.pdf', '')}_{i}"
            datasets[dataset_id] = {
                'dataframe': cleaned_df,
                'metadata': {
                    'filename': file.filename,
                    'table_number': i + 1,
                    'page': table_info['page'],
                    'rows': len(cleaned_df),
                    'columns': len(cleaned_df.columns)
                },
                'cleaning_report': cleaning_report
            }
            
            data_store[dataset_id] = datasets[dataset_id]
        
        return {
            'filename': file.filename,
            'tables_extracted': len(datasets),
            'datasets': list(datasets.keys()),
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/datasets")
async def list_datasets():
    """List all available datasets"""
    return {
        'datasets': [
            {
                'dataset_id': ds_id,
                'metadata': data['metadata']
            }
            for ds_id, data in data_store.items()
        ],
        'total': len(data_store)
    }


@app.get("/datasets/{dataset_id}")
async def get_dataset_info(dataset_id: str):
    """Get information about a specific dataset"""
    if dataset_id not in data_store:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    data = data_store[dataset_id]
    df = data['dataframe']
    
    # Generate summary
    summary = descriptive_analytics.generate_summary_statistics(df)
    
    return {
        'dataset_id': dataset_id,
        'metadata': data['metadata'],
        'summary': summary,
        'status': 'success'
    }


@app.post("/query")
async def natural_language_query(request: QueryRequest):
    """
    Process natural language query
    """
    try:
        logger.info(f"Processing query: {request.question}")
        
        # Get dataset context if provided
        context = request.context or {}
        if request.dataset_id and request.dataset_id in data_store:
            context['dataset'] = data_store[request.dataset_id]['metadata']
        
        # Process query
        response = conversational_agent.query(request.question, context)
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analytics/descriptive")
async def descriptive_analysis(request: AnalyticsRequest):
    """
    Perform descriptive analytics
    """
    try:
        if request.dataset_id not in data_store:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        df = data_store[request.dataset_id]['dataframe']
        params = request.parameters or {}
        
        if request.analysis_type == "summary":
            result = descriptive_analytics.generate_summary_statistics(df)
        elif request.analysis_type == "trends":
            result = descriptive_analytics.analyze_trends(
                df,
                params.get('date_column'),
                params.get('value_columns', [])
            )
        elif request.analysis_type == "correlation":
            result = descriptive_analytics.correlation_analysis(
                df,
                params.get('method', 'pearson')
            )
        else:
            raise HTTPException(status_code=400, detail="Unknown analysis type")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in descriptive analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analytics/predictive")
async def predictive_analysis(request: AnalyticsRequest):
    """
    Perform predictive analytics
    """
    try:
        if request.dataset_id not in data_store:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        df = data_store[request.dataset_id]['dataframe']
        params = request.parameters or {}
        
        if request.analysis_type == "forecast":
            result = predictive_analytics.forecast_time_series(
                df,
                params.get('date_column'),
                params.get('value_column'),
                params.get('periods', 30),
                params.get('model_type', 'prophet')
            )
        elif request.analysis_type == "predict_xgboost":
            result = predictive_analytics.predict_with_xgboost(
                df,
                params.get('target_column'),
                params.get('feature_columns', [])
            )
        else:
            raise HTTPException(status_code=400, detail="Unknown analysis type")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in predictive analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/report/generate")
async def generate_report(request: ReportRequest, background_tasks: BackgroundTasks):
    """
    Generate comprehensive analytics report
    """
    try:
        if request.dataset_id not in data_store:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        df = data_store[request.dataset_id]['dataframe']
        metadata = data_store[request.dataset_id]['metadata']
        
        # Generate report
        report_path = report_generator.generate_comprehensive_report(
            df,
            metadata,
            report_type=request.report_type,
            include_visualizations=request.include_visualizations
        )
        
        return {
            'report_path': str(report_path),
            'dataset_id': request.dataset_id,
            'status': 'success'
        }
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/visualizations/{dataset_id}/time_series")
async def create_time_series_viz(dataset_id: str, date_column: str, value_columns: str):
    """
    Create time series visualization
    """
    try:
        if dataset_id not in data_store:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        df = data_store[dataset_id]['dataframe']
        value_cols = value_columns.split(',')
        
        result = chart_generator.create_time_series_chart(
            df, date_column, value_cols
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )

