import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sqlalchemy.orm import Session
from pymongo.database import Database
from typing import List
import logging
import subprocess
from schemas.test import SamplesAndRowsCount

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def count_lines(file_path) -> int:
    result = subprocess.run(['wc', '-l', file_path], stdout=subprocess.PIPE, text=True)
    total_lines = int(result.stdout.split()[0])
    return max(0, total_lines - 1)


def count_users() -> int:
    return count_lines("/data/csv/users.csv")


def count_devices() -> int:
    return count_lines("/data/csv/devices.csv")


def perform_tests(row_test_query_counts: List[int], test_samples: int, database_func, mongo_db, postgresql_db):
    mongo_execution_times = {}
    postgres_execution_times = {}

    for row_count in row_test_query_counts:
        execution_times = database_func(SamplesAndRowsCount(samples_count=test_samples, rows_count=row_count),
                                        mongo_db, postgresql_db)
        mongo_execution_times[row_count] = execution_times.mongo_execution_times
        postgres_execution_times[row_count] = execution_times.postgres_execution_times

    return mongo_execution_times, postgres_execution_times


def execute_and_plot(mongo_db: Database, postgresql_db: Session, max_rows, database_func, test_samples: int = 10,
                     plot_filename: str = "query_execution_times_with_means.png"):
    row_test_query_counts = [row_count for row_count in range(10, max_rows, max_rows // 5)]
    mongo_execution_times, postgres_execution_times = perform_tests(row_test_query_counts, test_samples=test_samples,
                                                                    database_func=database_func,
                                                                    mongo_db=mongo_db, postgresql_db=postgresql_db)

    logger.info(f"Mongo execution times: {mongo_execution_times}")
    logger.info(f"Postgres execution times: {postgres_execution_times}")

    output_path = os.path.join("/data", plot_filename)
    plot_create(row_test_query_counts, mongo_execution_times, postgres_execution_times, output_path)

    return 1


def plot_create(row_test_query_counts, mongo_execution_times, postgres_execution_times, output_path: str = None):
    # Prepare data for the boxplot
    execution_data = []
    row_labels = []
    means = []

    # Loop through each row count and prepare data for both MongoDB and PostgreSQL
    for row_count in row_test_query_counts:
        mongo_times = mongo_execution_times[row_count]
        postgres_times = postgres_execution_times[row_count]

        execution_data.append(mongo_times)
        execution_data.append(postgres_times)
        row_labels.append(f"{row_count} wierszy (MongoDB)")
        row_labels.append(f"{row_count} wierszy (PostgreSQL)")

        # Calculate means
        means.append(np.mean(mongo_times))
        means.append(np.mean(postgres_times))

    # Plot results
    plt.figure(figsize=(12, 8))  # Zwiększ wysokość figury
    ax = plt.gca()

    # Add background colors for each row count
    colors = ['#f0f8ff', '#e6ffe6', '#fff2cc', '#ffe6e6', '#e6e6ff']  # Kolory tła dla poszczególnych kolumn
    for i in range(len(row_test_query_counts)):
        start = i * 2 - 0.5
        end = i * 2 + 1.5
        ax.axvspan(start, end, facecolor=colors[i % len(colors)], alpha=0.3)

    # Create the boxplot
    sns.boxplot(data=execution_data, palette=["blue", "orange"] * len(row_test_query_counts), width=0.5, notch=False)

    # Set x-ticks to match the row counts, and format the labels
    xticks_pos = np.arange(len(row_labels))
    plt.xticks(xticks_pos, row_labels, rotation=45)

    # Add mean values above each boxplot
    for i, mean in enumerate(means):
        plt.text(i, mean + 0.18 * max(means), f"{mean:.2f}", ha='center', va='bottom', fontsize=9, color='black')

    # Adjust Y-axis limit to add more space above the highest boxplot
    # plt.ylim(0, max(means) * 1.2)  # 20% więcej przestrzeni powyżej najwyższej wartości średniej

    # Labeling
    plt.xlabel("Liczba wierszy")
    plt.ylabel("Czas wykonania zapytania (milisekundy)")
    plt.title("Porównanie czasu wykonania zapytania w MongoDB i PostgreSQL")

    # Move legend to the upper left corner
    plt.legend(labels=["MongoDB", "PostgreSQL"], loc='upper left', frameon=False)

    plt.tight_layout()  # Adjust layout to avoid overlap
    plt.savefig(output_path)
    logger.info(f"Plot saved to {output_path}")
