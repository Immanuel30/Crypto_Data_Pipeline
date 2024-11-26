# Crypto-Solutions Data Streaming Pipeline

This repository contains the implementation of a real-time data streaming pipeline for Crypto-Solutions, a company focused on extracting live cryptocurrency data from Binance and loading it into BigQuery in real time. The project leverages Google Cloud Platform (GCP) and several tools to achieve this goal.

## Business Introduction

Crypto-Solutions is a company specializing in cryptocurrency market analytics. It provides real-time insights and historical data analysis to help traders and financial analysts make informed decisions. With the rapid and volatile nature of the cryptocurrency market, Crypto-Solutions aims to offer up-to-date data to its users, ensuring they have the latest information at their fingertips.

## Problem Statement

Crypto-Solutions relies on up-to-the-minute data from various cryptocurrency exchanges to provide accurate and timely analytics. The challenge is to collect and process this data in real-time, ensuring that it is always available for analysis without any delays. Manual data collection methods and batch processing are inadequate for this purpose due to the high-frequency nature of cryptocurrency price changes and the need for immediate access to data.

## Proposed Solution

To maintain a competitive edge and deliver real-time insights, Crypto-Solutions requires a scalable, robust, and real-time data streaming solution. This solution must be capable of ingesting live data from Binance, processing it with minimal latency, and storing it in BigQuery for instant querying and analysis. Additionally, the solution should be able to handle high volumes of data efficiently and reliably.

## Project Workflow

### Data Extraction from Binance
The project uses `Asyncio` to handle asynchronous data streaming from the Binance cryptocurrency exchange. This allows us to capture live data feeds without blocking operations.

### Data Ingestion with PubSub
Google Cloud PubSub is used for real-time message ingestion. The streamed data from Binance is published to a PubSub topic, ensuring that messages are reliably queued for processing.

### Data Storage in Google Cloud Storage
Google Cloud Storage acts as a temporary storage layer, where raw data can be stored before further processing. This provides a buffer to handle spikes in data volume and ensures that no data is lost.

### Data Loading into BigQuery
The processed data is then loaded into BigQuery, which serves as the central data warehouse. BigQuery’s powerful analytics capabilities allow users to perform complex queries on the data with minimal latency.

### Pipeline Orchestration with Dataflow
Google Cloud Dataflow is used to orchestrate the entire data streaming pipeline. Dataflow pipelines are set up to automate the data flow from extraction, through transformation, to loading into BigQuery. The pipelines are designed to be scalable and fault-tolerant, ensuring seamless data processing even during high loads.
