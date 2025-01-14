import csv
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from sqlalchemy.orm import Session
from pymongo.database import Database
from typing import List
import logging
import subprocess

from routers.test.delete import delete_gestures_func
from routers.test.insert import insert_gestures_func
from routers.test.update import update_gestures_func
from schemas.test import SamplesAndRowsCount, SamplesCount, ExecutionTime

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


def perform_test_database_set(database_func, mongo_db, postgresql_db, key_name="smallDB_insert_gestures",
                              test_samples: int = 10):
    execution_times = database_func(SamplesCount(samples_count=test_samples), mongo_db, postgresql_db)
    # execution_times.mongo_execution_times = [2,3,4,5]
    # execution_times.postgres_execution_times = [2,3,6,1]
    save_to_csv(f"/data/{key_name}.csv", execution_times)


def save_to_csv(file_path: str, execution_times: ExecutionTime):
    with open(file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write header row
        writer.writerow(["mongo", "postgres"])

        # Write execution times
        for mongo_time, postgres_time in zip(execution_times.mongo_execution_times,
                                             execution_times.postgres_execution_times):
            writer.writerow([mongo_time, postgres_time])


def perform_tests_database_set(mongo_db: Database, postgresql_db: Session, db_size="small", test_samples: int = 10):
    perform_test_database_set(insert_gestures_func, mongo_db, postgresql_db, key_name=f"{db_size}DB_insert_gestures",
                              test_samples=test_samples)
    perform_test_database_set(update_gestures_func, mongo_db, postgresql_db, key_name=f"{db_size}DB_update_gestures",
                              test_samples=test_samples)
    perform_test_database_set(delete_gestures_func, mongo_db, postgresql_db, key_name=f"{db_size}DB_delete_gestures",
                              test_samples=test_samples)
    return 1


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


def plot_create(x_categories, mongo_execution_times, postgres_execution_times, output_path: str = None):
    # Prepare data for the boxplot
    execution_data = []
    row_labels = []
    means = []

    # Loop through each x_categories and prepare data for both MongoDB and PostgreSQL
    for x_category in x_categories:
        mongo_times = mongo_execution_times[x_category]
        postgres_times = postgres_execution_times[x_category]

        execution_data.append(mongo_times)
        execution_data.append(postgres_times)
        row_labels.append(f"{x_category} wierszy (MongoDB)")
        row_labels.append(f"{x_category} wierszy (PostgreSQL)")

        # Calculate means
        means.append(np.mean(mongo_times))
        means.append(np.mean(postgres_times))

    # Plot results
    plt.figure(figsize=(12, 8))  # Zwiększ wysokość figury
    ax = plt.gca()

    # Add background colors for each x_categories
    colors = ['#f0f8ff', '#e6ffe6', '#fff2cc', '#ffe6e6', '#e6e6ff']  # Kolory tła dla poszczególnych kolumn
    for i in range(len(x_categories)):
        start = i * 2 - 0.5
        end = i * 2 + 1.5
        ax.axvspan(start, end, facecolor=colors[i % len(colors)], alpha=0.3)

    # Create the boxplot
    sns.boxplot(data=execution_data, palette=["blue", "orange"] * len(x_categories), width=0.5, notch=False)

    # Set x-ticks to match the x_categories, and format the labels
    xticks_pos = np.arange(len(row_labels))
    plt.xticks(xticks_pos, row_labels, rotation=45)

    # Add mean values above each boxplot
    for i, mean in enumerate(means):
        plt.text(i, mean + 0.18 * max(means), f"{mean:.2f}", ha='center', va='bottom', fontsize=9, color='black')

    # Labeling
    plt.xlabel("Liczba wierszy")
    plt.ylabel("Czas wykonania zapytania (milisekundy)")
    plt.title("Porównanie czasu wykonania zapytania w MongoDB i PostgreSQL")

    # Move legend to the upper left corner
    plt.legend(labels=["MongoDB", "PostgreSQL"], loc='upper left', frameon=False)

    plt.tight_layout()  # Adjust layout to avoid overlap
    plt.savefig(output_path)
    logger.info(f"Plot saved to {output_path}")


def plot_create_gestures_separate_old(csv_files, output_dir: str):
    """
    Create and save separate boxplots for each operation comparing execution times for MongoDB and PostgreSQL.

    :param csv_files: Dictionary of CSV file paths grouped by operation and database size.
    :param output_dir: Directory to save the plots.
    """
    # Define operations and database sizes
    operations = ['insert', 'update', 'delete']
    db_sizes = ['small', 'medium', 'large']

    # Colors for background categories
    colors = ['#f0f8ff', '#e6ffe6', '#fff2cc']

    for operation in operations:
        execution_data = []
        row_labels = []
        means = []

        # Process each database size for the current operation
        for db_size in db_sizes:
            file_key = f"{db_size}DB_{operation}_gestures.csv"
            if file_key not in csv_files:
                logger.warning(f"File {file_key} is missing in input data.")
                continue

            # Load data
            df = pd.read_csv(csv_files[file_key])
            mongo_times = df['mongo']
            postgres_times = df['postgres']

            # Append data for boxplot
            execution_data.append(mongo_times)
            execution_data.append(postgres_times)

            # Append labels
            row_labels.append(f"{db_size.capitalize()} DB (MongoDB)")
            row_labels.append(f"{db_size.capitalize()} DB (PostgreSQL)")

            # Calculate means
            means.append(np.mean(mongo_times))
            means.append(np.mean(postgres_times))

        # Plot setup
        plt.figure(figsize=(16, 10))  # Increased size for better spacing
        ax = plt.gca()

        # Add background colors
        for i, db_size in enumerate(db_sizes):
            start = i * 2 - 0.5
            end = i * 2 + 1.5
            ax.axvspan(start, end, facecolor=colors[i % len(colors)], alpha=0.2)

        # Create the boxplot
        sns.boxplot(data=execution_data, palette=["blue", "orange"] * len(db_sizes), width=0.5, notch=False)

        # Set x-ticks and labels
        xticks_pos = np.arange(len(row_labels))
        plt.xticks(xticks_pos, row_labels, rotation=45, fontsize=12)  # Adjusted for better readability

        # Add mean values above each box
        for i, mean in enumerate(means):
            plt.text(i, mean * 1.1, f"{mean:.2f}", ha='center', va='bottom', fontsize=10)

        # Labels and title
        plt.xlabel("Database Size", fontsize=14)
        plt.ylabel("Execution Time (ms)", fontsize=14)
        plt.title(f"Query Execution Time Comparison: MongoDB vs PostgreSQL ({operation.capitalize()})", fontsize=16)
        plt.tight_layout()

        # Save plot
        output_path = f"{output_dir}/{operation}_execution_times_fixed.png"
        plt.savefig(output_path)
        plt.close()
        logger.info(f"Plot for {operation} with improved layout saved to {output_path}")


def process_files(file_paths):
    averages = {"mongo": [], "postgres": []}
    sizes = ["small", "medium", "large"]
    for size in sizes:
        df = pd.read_csv(file_paths[size])
        averages["mongo"].append(df["mongo"].mean())
        averages["postgres"].append(df["postgres"].mean())
    return averages


# Funkcja do rysowania wykresów
def plot_operation(operation_name, averages, output_dir):
    sizes = ["mały", "średni", "duży"]
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, averages["mongo"], label="MongoDB", marker='o', linestyle='--', color='blue')
    plt.plot(sizes, averages["postgres"], label="PostgreSQL", marker='o', linestyle='--', color='orange')
    plt.title(f"Operacja {operation_name.capitalize()} - Średni czas wykonania")
    plt.xlabel("Rozmiar bazy danych")
    plt.ylabel("Średni czas wykonania [ms]")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{output_dir}/{operation_name}_operation_times.png")
    plt.show()


def plot_create_gestures_separate(files, output_dir):
    for operation in files.keys():
        averages = process_files(files[operation])
        plot_operation(operation, averages, output_dir)
