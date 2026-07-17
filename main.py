import logging
from transform.preprocess_data import get_transformed_data
from load.load_bigquery import create_if_staging_not_exists, load_dataframe_to_staging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("Starting ETL Pipeline...")

    try:
        df = get_transformed_data()

        create_if_staging_not_exists()

        upload_info = load_dataframe_to_staging(df)

        logger.info(
            f"Loaded {upload_info['rows_loaded']} rows into "
            f"{upload_info['table']}"
        )

        logger.info("ETL Pipeline completed successfully.")

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        raise

if __name__ == '__main__':
    run_pipeline()