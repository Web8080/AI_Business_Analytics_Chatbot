"""
Predictive Analytics Module - Forecasting with Prophet/XGBoost, anomaly prediction
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class PredictiveAnalytics:
    """Predictive analytics for forecasting and future trend prediction"""
    
    def __init__(self):
        """Initialize predictive analytics engine"""
        self.models = {}
    
    def forecast_time_series(self, df: pd.DataFrame, date_column: str, 
                            value_column: str, periods: int = 30,
                            model_type: str = 'prophet') -> Dict[str, Any]:
        """
        Time series forecasting using Prophet or statistical methods
        
        Args:
            df: Input DataFrame
            date_column: Date column name
            value_column: Value column to forecast
            periods: Number of periods to forecast
            model_type: 'prophet' or 'statistical'
            
        Returns:
            Dictionary containing forecast results
        """
        if date_column not in df.columns or value_column not in df.columns:
            return {'status': 'error', 'message': 'Required columns not found'}
        
        logger.info(f"Forecasting {value_column} for {periods} periods using {model_type}")
        
        try:
            # Prepare data
            forecast_df = df[[date_column, value_column]].copy()
            forecast_df = forecast_df.dropna()
            forecast_df[date_column] = pd.to_datetime(forecast_df[date_column])
            forecast_df = forecast_df.sort_values(date_column)
            
            if model_type == 'prophet':
                forecast_result = self._forecast_prophet(forecast_df, date_column, value_column, periods)
            else:
                forecast_result = self._forecast_statistical(forecast_df, date_column, value_column, periods)
            
            return forecast_result
            
        except Exception as e:
            logger.error(f"Forecasting error: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def _forecast_prophet(self, df: pd.DataFrame, date_column: str, 
                         value_column: str, periods: int) -> Dict[str, Any]:
        """Forecast using Prophet"""
        try:
            from prophet import Prophet
            
            # Prepare data in Prophet format
            prophet_df = df[[date_column, value_column]].rename(columns={
                date_column: 'ds',
                value_column: 'y'
            })
            
            # Initialize and fit model
            model = Prophet(
                daily_seasonality=False,
                weekly_seasonality=True,
                yearly_seasonality=True,
                changepoint_prior_scale=0.05
            )
            model.fit(prophet_df)
            
            # Make future dataframe
            future = model.make_future_dataframe(periods=periods)
            forecast = model.predict(future)
            
            # Extract forecast results
            forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
            
            # Calculate accuracy metrics on historical data
            historical_forecast = forecast[forecast['ds'].isin(prophet_df['ds'])]
            mae = np.mean(np.abs(historical_forecast['yhat'].values - prophet_df['y'].values))
            mape = np.mean(np.abs((prophet_df['y'].values - historical_forecast['yhat'].values) / prophet_df['y'].values)) * 100
            
            return {
                'model_type': 'prophet',
                'forecast': forecast_data.to_dict('records'),
                'historical_performance': {
                    'mae': float(mae),
                    'mape': float(mape)
                },
                'trend_components': {
                    'trend': forecast['trend'].tail(periods).tolist(),
                    'weekly': forecast.get('weekly', pd.Series([0] * periods)).tail(periods).tolist(),
                    'yearly': forecast.get('yearly', pd.Series([0] * periods)).tail(periods).tolist()
                },
                'status': 'success'
            }
            
        except ImportError:
            logger.warning("Prophet not available, falling back to statistical method")
            return self._forecast_statistical(df, date_column, value_column, periods)
        except Exception as e:
            logger.error(f"Prophet forecasting error: {str(e)}")
            return self._forecast_statistical(df, date_column, value_column, periods)
    
    def _forecast_statistical(self, df: pd.DataFrame, date_column: str, 
                             value_column: str, periods: int) -> Dict[str, Any]:
        """Forecast using statistical methods (moving average, exponential smoothing)"""
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing
            
            # Prepare time series
            ts = df.set_index(date_column)[value_column]
            
            # Fit exponential smoothing model
            model = ExponentialSmoothing(
                ts,
                seasonal_periods=7 if len(ts) > 14 else None,
                trend='add',
                seasonal='add' if len(ts) > 14 else None
            )
            fitted_model = model.fit()
            
            # Forecast
            forecast = fitted_model.forecast(steps=periods)
            
            # Generate future dates
            last_date = df[date_column].max()
            freq = pd.infer_freq(df[date_column]) or 'D'
            future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods, freq=freq)
            
            # Calculate confidence intervals (simple approximation)
            std_error = np.std(fitted_model.fittedvalues - ts)
            lower_bound = forecast - 1.96 * std_error
            upper_bound = forecast + 1.96 * std_error
            
            forecast_data = []
            for date, pred, lower, upper in zip(future_dates, forecast, lower_bound, upper_bound):
                forecast_data.append({
                    'ds': str(date),
                    'yhat': float(pred),
                    'yhat_lower': float(lower),
                    'yhat_upper': float(upper)
                })
            
            # Calculate accuracy metrics
            mae = np.mean(np.abs(fitted_model.fittedvalues - ts))
            mape = np.mean(np.abs((ts - fitted_model.fittedvalues) / ts)) * 100
            
            return {
                'model_type': 'exponential_smoothing',
                'forecast': forecast_data,
                'historical_performance': {
                    'mae': float(mae),
                    'mape': float(mape)
                },
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Statistical forecasting error: {str(e)}")
            # Simple moving average fallback
            return self._forecast_moving_average(df, date_column, value_column, periods)
    
    def _forecast_moving_average(self, df: pd.DataFrame, date_column: str, 
                                value_column: str, periods: int) -> Dict[str, Any]:
        """Simple moving average forecast"""
        window = min(7, len(df) // 2)
        last_values = df[value_column].tail(window).mean()
        
        last_date = df[date_column].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods, freq='D')
        
        forecast_data = []
        for date in future_dates:
            forecast_data.append({
                'ds': str(date),
                'yhat': float(last_values),
                'yhat_lower': float(last_values * 0.9),
                'yhat_upper': float(last_values * 1.1)
            })
        
        return {
            'model_type': 'moving_average',
            'forecast': forecast_data,
            'status': 'success'
        }
    
    def predict_with_xgboost(self, df: pd.DataFrame, target_column: str, 
                            feature_columns: List[str], test_size: float = 0.2) -> Dict[str, Any]:
        """
        Predictive modeling using XGBoost
        
        Args:
            df: Input DataFrame
            target_column: Target variable to predict
            feature_columns: Feature columns for prediction
            test_size: Proportion of data for testing
            
        Returns:
            Dictionary containing model results
        """
        try:
            import xgboost as xgb
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
            
            logger.info(f"Training XGBoost model to predict {target_column}")
            
            # Prepare data
            X = df[feature_columns].copy()
            y = df[target_column].copy()
            
            # Handle categorical variables
            for col in X.select_dtypes(include=['object', 'category']).columns:
                X[col] = pd.Categorical(X[col]).codes
            
            # Handle missing values
            X = X.fillna(X.mean())
            y = y.fillna(y.mean())
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
            
            # Train model
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            # Feature importance
            feature_importance = dict(zip(feature_columns, model.feature_importances_))
            feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
            
            return {
                'model_type': 'xgboost',
                'target': target_column,
                'features': feature_columns,
                'performance': {
                    'mae': float(mae),
                    'rmse': float(rmse),
                    'r2_score': float(r2)
                },
                'feature_importance': {k: float(v) for k, v in feature_importance.items()},
                'predictions_sample': [
                    {'actual': float(a), 'predicted': float(p)} 
                    for a, p in zip(y_test[:10], y_pred[:10])
                ],
                'status': 'success'
            }
            
        except ImportError:
            return {'status': 'error', 'message': 'XGBoost not available'}
        except Exception as e:
            logger.error(f"XGBoost prediction error: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def predict_churn(self, df: pd.DataFrame, activity_column: str, 
                     user_column: str, date_column: str, threshold_days: int = 30) -> Dict[str, Any]:
        """
        Predict customer churn based on activity patterns
        
        Args:
            df: Input DataFrame
            activity_column: Column indicating activity
            user_column: User/customer identifier
            date_column: Date column
            threshold_days: Days of inactivity to consider churn
            
        Returns:
            Dictionary containing churn predictions
        """
        logger.info("Predicting customer churn")
        
        try:
            df[date_column] = pd.to_datetime(df[date_column])
            max_date = df[date_column].max()
            
            # Calculate days since last activity for each user
            last_activity = df.groupby(user_column)[date_column].max().reset_index()
            last_activity['days_since_activity'] = (max_date - last_activity[date_column]).dt.days
            
            # Calculate activity frequency
            activity_freq = df.groupby(user_column).size().reset_index(name='total_activities')
            
            # Merge
            churn_data = last_activity.merge(activity_freq, on=user_column)
            
            # Predict churn
            churn_data['churn_risk'] = churn_data['days_since_activity'].apply(
                lambda x: 'high' if x > threshold_days else 'medium' if x > threshold_days/2 else 'low'
            )
            churn_data['churned'] = churn_data['days_since_activity'] > threshold_days
            
            # Statistics
            total_users = len(churn_data)
            churned_users = churn_data['churned'].sum()
            churn_rate = (churned_users / total_users * 100) if total_users > 0 else 0
            
            risk_distribution = churn_data['churn_risk'].value_counts().to_dict()
            
            return {
                'total_users': int(total_users),
                'churned_users': int(churned_users),
                'churn_rate': round(float(churn_rate), 2),
                'risk_distribution': risk_distribution,
                'high_risk_users': churn_data[churn_data['churn_risk'] == 'high'][user_column].tolist()[:50],
                'threshold_days': threshold_days,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Churn prediction error: {str(e)}")
            return {'status': 'error', 'message': str(e)}

